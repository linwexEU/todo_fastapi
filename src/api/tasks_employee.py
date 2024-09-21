from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.tasks import TasksAddResponse, TasksEmployeeAddExpect, TasksAdd, TasksFilters, TasksDelete, TasksUpdate, TasksInfo
from src.auth.dependencies import get_current_user 
from src.models.models import Users 
from src.services.tasks import TasksService 
from src.api.dependencies import tasks_service
from sqlalchemy.exc import SQLAlchemyError
from fastapi_cache.decorator import cache
from src.logger import config_logger
from typing import Annotated
import logging
from src.utils.exceptions import UserNotEmployee, TaskAlreadyExist, TaskNotFound, NotYourTask


router = APIRouter(prefix="/tasks/employee", tags=["Tasks Employee"])


logger = logging.getLogger(__name__)
config_logger() 


@router.get("/", summary="All tasks (Employee)")
@cache(15)
async def employee_all_tasks(
    current_user: Annotated[Users, Depends(get_current_user)], 
    tasks_service: Annotated[TasksService, Depends(tasks_service)]
) -> list[TasksInfo]: 
    if current_user.status == "Employer": 
        raise UserNotEmployee
    return [TasksInfo(id=task.id, task=task.task, status=task.status) for task in await tasks_service.get_by_filters(TasksFilters(assignee=current_user.id))]


@router.post("/create/", summary="Create task (Employee)", status_code=status.HTTP_201_CREATED)
async def employee_add_task(
    data: TasksEmployeeAddExpect,
    current_user: Annotated[Users, Depends(get_current_user)], 
    tasks_service: Annotated[TasksService, Depends(tasks_service)]
) -> TasksAddResponse:
    if current_user.status != "Employee":
        raise UserNotEmployee

    tasks = await tasks_service.get_existed_tasks() 
    if data.task in tasks: 
        raise TaskAlreadyExist
    
    try:
        await tasks_service.add(
            TasksAdd(
                task=data.task,
                status="In Process",
                creator=current_user.id,
                assignee=current_user.id
            )
        )
        return TasksAddResponse(TaskHasCreated=True) 
    except (SQLAlchemyError, Exception) as ex:
        if isinstance(ex, SQLAlchemyError):
            logger.error("SQLAlchemyError: %s", ex) 
        else: 
            logger.error("Unknown Exc: %s", ex) 
        return TasksAddResponse(TaskHasCreated=False) 


@router.patch("/{task_id}/done/", summary="Complete task (Employee)")
async def employee_done_task(
    task_id: int,
    current_user: Annotated[Users, Depends(get_current_user)], 
    tasks_service: Annotated[TasksService, Depends(tasks_service)]
) -> TasksUpdate:
    if current_user.status != "Employee":
        raise UserNotEmployee

    task = await tasks_service.get_by_filters(TasksFilters(id=task_id))
    if not task: 
        raise TaskNotFound
    if task[0].assignee != current_user.id:
        raise NotYourTask
    
    try:
        await tasks_service.update_task_to_complete(task_id)
        return TasksUpdate(TaskHasUpdated=True)   
    except (SQLAlchemyError, Exception) as ex:
        if isinstance(ex, SQLAlchemyError):
            logger.error("SQLAlchemyError: %s", ex) 
        else: 
            logger.error("Unknown Exc: %s", ex) 
        return TasksUpdate(TaskHasUpdated=False)  


@router.delete("/{task_id}/delete/", summary="Delete task (Employee)")
async def employee_delete_task(
    task_id: int,
    current_user: Annotated[Users, Depends(get_current_user)], 
    tasks_service: Annotated[TasksService, Depends(tasks_service)]
): 
    task = await tasks_service.get_by_filters(TasksFilters(id=task_id))
    if not task: 
        raise TaskNotFound

    try: 
        await tasks_service.delete_by_id(task_id) 
        return TasksDelete(TaskHasDeleted=True) 
    except (SQLAlchemyError, Exception) as ex:
        if isinstance(ex, SQLAlchemyError):
            logger.error("SQLAlchemyError: %s", ex) 
        else: 
            logger.error("Unknown Exc: %s", ex) 
        return TasksDelete(TaskHasDeleted=False) 
    