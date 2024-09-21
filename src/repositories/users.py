from src.utils.repository import SQLAlchemyRepository 
from src.models.models import Users
from src.db.db import async_session_maker 
from sqlalchemy import select, update


class UsersRepository(SQLAlchemyRepository): 
    model = Users 

    async def get_existed_emails(self): 
        async with async_session_maker() as session: 
            query = select(self.model.email) 
            result = await session.execute(query) 
            return result.scalars().all() 
    
    async def asign_to_company(self, user_id: int, company_id: int): 
        async with async_session_maker() as session: 
            query = update(self.model).where(self.model.id == user_id).values(company=company_id)
            await session.execute(query) 
            await session.commit() 
