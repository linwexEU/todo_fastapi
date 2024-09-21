from src.utils.repository import SQLAlchemyRepository 
from src.models.models import Tasks, Users
from src.db.db import async_session_maker 
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload


class TasksRepository(SQLAlchemyRepository): 
    model = Tasks 

    async def get_existed_tasks(self): 
        async with async_session_maker() as session: 
            query = select(self.model.task) 
            result = await session.execute(query) 
            return result.scalars().all() 
    
    async def update_task_to_complete(self, task_id: int): 
        async with async_session_maker() as session: 
            query = update(self.model).where(self.model.id == task_id).values(status="Done")
            await session.execute(query) 
            await session.commit() 

    async def get_tasks_with_assignee(self, filters: dict): 
        async with async_session_maker() as session: 
            query = select(self.model).options(selectinload(self.model.assignee_user)).filter_by(**filters)
            result = await session.execute(query) 
            return result.scalars().all() 
