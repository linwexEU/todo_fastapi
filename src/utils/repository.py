from abc import ABC, abstractmethod 
from sqlalchemy import select, insert, delete
from src.db.db import async_session_maker


class AbstractRepository(ABC): 
    @abstractmethod 
    async def add(self, values: dict): 
        pass 

    @abstractmethod 
    async def get_all(self): 
        pass 
    
    @abstractmethod 
    async def get_by_filters(self, filters: dict): 
        pass

    @abstractmethod 
    async def get_by_id(self, id: int): 
        pass 

    @abstractmethod 
    async def delete_by_id(self, id: int): 
        pass


class SQLAlchemyRepository(AbstractRepository): 
    model = None 

    async def get_all(self):
        async with async_session_maker() as session: 
            query = select(self.model)
            result = await session.execute(query) 
            return result.scalars().all() 

    async def add(self, data: dict):
        async with async_session_maker() as session: 
            query = insert(self.model).values(**data)
            await session.execute(query) 
            await session.commit()
        
    async def get_by_filters(self, filters: dict): 
        async with async_session_maker() as session: 
            query = select(self.model).filter_by(**filters) 
            result = await session.execute(query) 
            return result.scalars().all()

    async def get_by_id(self, id: int): 
        async with async_session_maker() as session: 
            query = select(self.model).where(self.model.id == id)
            result = await session.execute(query) 
            return result.scalar()
    
    async def delete_by_id(self, id: int): 
        async with async_session_maker() as session: 
            query = delete(self.model).where(self.model.id == id)
            await session.execute(query) 
            await session.commit() 
        