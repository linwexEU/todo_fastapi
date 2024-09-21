from fastapi import Depends
from typing import Annotated

from src.services.users import UsersService
from src.repositories.users import UsersRepository 

from src.services.tasks import TasksService 
from src.repositories.tasks import TasksRepository

from src.services.companies import CompaniesService 
from src.repositories.companies import CompaniesRepository
from src.store import Store, get_store


def users_service(): 
    return UsersService(UsersRepository)


def tasks_service(): 
    return TasksService(TasksRepository) 


def companies_service(): 
    return CompaniesService(CompaniesRepository)


StoreDep = Annotated[Store, Depends(get_store)]