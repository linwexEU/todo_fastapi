from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from src.schemas.companies import CompaniesFilters
from src.schemas.users import UsersFilters
from src.schemas.tasks import TasksAdd, TasksAddResponse, TasksEmployerAddExpect, TasksWithAssignee, TasksFilters, \
    TasksDelete, AssigneeInfo
from src.auth.dependencies import get_current_user 
from src.models.models import Users, Tasks
from src.api.dependencies import tasks_service, StoreDep
from src.services.tasks import TasksService 
from src.api.dependencies import users_service
from src.broker.send import send_task
from src.services.users import UsersService
from src.api.dependencies import companies_service
from src.services.companies import CompaniesService
from sqlalchemy.exc import SQLAlchemyError 
from src.logger import config_logger
from fastapi_cache.decorator import cache
from typing import Annotated
import logging
from src.utils.exceptions import UserNotEmployer, CompanyNotFound, CantCreateTaskForEmployee, TaskAlreadyExist, \
    TaskNotFound


router = APIRouter(prefix="/tasks/employer", tags=["Tasks Employer"])


logger = logging.getLogger(__name__)
config_logger() 


@router.get("/", summary="All tasks (Employer)")
@cache(15)
async def get_created_tasks(
    current_user: Annotated[Users, Depends(get_current_user)], 
    tasks_service: Annotated[TasksService, Depends(tasks_service)]
) -> list[TasksWithAssignee]: 
    if current_user.status != "Employer": 
        raise UserNotEmployer
    return [
        TasksWithAssignee(
            id=task.id,
            task=task.task,
            status=task.status,
            assignee_user=AssigneeInfo(
                id=task.assignee_user.id,
                username=task.assignee_user.username,
                status=task.assignee_user.status
            )
        )
        for task in await tasks_service.get_tasks_with_assignee(TasksFilters(creator=current_user.id))
    ]


@router.post("/create/", summary="Create task (Employer)", status_code=status.HTTP_201_CREATED)
async def employer_create_task(
    data: TasksEmployerAddExpect,
    store: StoreDep,
    current_user: Annotated[Users, Depends(get_current_user)], 
    users_service: Annotated[UsersService, Depends(users_service)],
    companies_service: Annotated[CompaniesService, Depends(companies_service)],
    tasks_service: Annotated[TasksService, Depends(tasks_service)]
) -> TasksAddResponse:
    if current_user.status != "Employer":
        raise UserNotEmployer

    companies = await companies_service.get_by_filters(CompaniesFilters(creator=current_user.id))
    if not companies:
        raise CompanyNotFound

    user = await users_service.get_by_filters(UsersFilters(id=data.assignee))
    if (not user) or (user[0].id == current_user.id) or (user[0].status == "Employer") or (user[0].company != companies[0].id):
        raise CantCreateTaskForEmployee

    tasks = await tasks_service.get_by_filters(TasksFilters(task=data.task)) 
    if tasks: 
        raise TaskAlreadyExist

    if user[0].email:
        await store.worker.send_email("Create", user[0].email, current_user.email, current_user.username, data.task)

    try:
        await tasks_service.add(
            TasksAdd(
                task=data.task,
                status="In Process",
                creator=current_user.id,
                assignee=data.assignee
            )
        )
        return TasksAddResponse(TaskHasCreated=True)
    except (SQLAlchemyError, Exception) as ex:
        if isinstance(ex, SQLAlchemyError):
            logger.error("SQLAlchemyError: %s", ex) 
        else: 
            logger.error("Unknown Exc: %s", ex) 
        return TasksAddResponse(TaskHasCreated=False)


@router.delete("/{task_id}/delete/", summary="Delete task (Employer)")
async def employer_delete_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[Users, Depends(get_current_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
    tasks_service: Annotated[TasksService, Depends(tasks_service)]
) -> TasksDelete:
    if current_user.status != "Employer":
        raise UserNotEmployer

    task: list[Tasks] = await tasks_service.get_by_filters(TasksFilters(id=task_id))
    if not task: 
        raise TaskNotFound

    user = await users_service.get_by_filters(UsersFilters(id=task[0].assignee))
    if user[0].email:
        await send_task("Delete", user[0].email, current_user.email, current_user.username, task[0].task)
    
    try: 
        await tasks_service.delete_by_id(task_id) 
        return TasksDelete(TaskHasDeleted=True)
    except (SQLAlchemyError, Exception) as ex:
        if isinstance(ex, SQLAlchemyError):
            logger.error("SQLAlchemyError: %s", ex) 
        else: 
            logger.error("Unknown Exc: %s", ex) 
        return TasksDelete(TaskHasDeleted=False)
