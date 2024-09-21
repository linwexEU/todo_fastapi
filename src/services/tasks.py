from src.models.models import Tasks
from src.schemas.tasks import TasksAdd, TasksFilters, TasksWithAssignee
from src.repositories.tasks import TasksRepository


class TasksService: 
    def __init__(self, tasks_repo: TasksRepository): 
        self.tasks_repo: TasksRepository = tasks_repo() 

    async def add(self, data: TasksAdd) -> None: 
        data_to_dict = data.model_dump() 
        await self.tasks_repo.add(data_to_dict) 

    async def get_all(self) -> list[Tasks]: 
        result = await self.tasks_repo.get_all() 
        return result 
    
    async def get_by_filters(self, filters: TasksFilters) -> list[Tasks]: 
        filters_to_dict = filters.model_dump(exclude_none=True) 
        result = await self.tasks_repo.get_by_filters(filters_to_dict)
        return result
    
    async def get_existed_tasks(self) -> list[str]: 
        result = await self.tasks_repo.get_existed_tasks() 
        return result

    async def update_task_to_complete(self, task_id: int) -> None: 
        await self.tasks_repo.update_task_to_complete(task_id) 

    async def delete_by_id(self, task_id: int) -> None: 
        await self.tasks_repo.delete_by_id(task_id) 

    async def get_tasks_with_assignee(self, filters: TasksFilters) -> list[Tasks]:
        filters_to_dict = filters.model_dump(exclude_none=True)
        result = await self.tasks_repo.get_tasks_with_assignee(filters_to_dict) 
        return result 
