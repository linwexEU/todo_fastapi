from pydantic import EmailStr
from src.models.models import Users
from src.schemas.users import UsersAdd, UsersFilters
from src.repositories.users import UsersRepository 


class UsersService: 
    def __init__(self, users_repo: UsersRepository): 
        self.users_repo: UsersRepository = users_repo()

    async def add(self, data: UsersAdd) -> None: 
        data_to_dict = data.model_dump() 
        await self.users_repo.add(data_to_dict) 

    async def get_by_filters(self, filters: UsersFilters) -> list[Users]: 
        filters_to_dict = filters.model_dump(exclude_none=True)
        result = await self.users_repo.get_by_filters(filters_to_dict) 
        return result

    async def get_by_id(self, id: int) -> Users: 
        result = await self.users_repo.get_by_id(id) 
        return result
    
    async def get_existed_emails(self) -> list[EmailStr]: 
        result = await self.users_repo.get_existed_emails() 
        return result 
    
    async def asign_to_company(self, user_id: int, company_id: int) -> None: 
        await self.users_repo.asign_to_company(user_id, company_id)
        