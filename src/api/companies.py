from fastapi import APIRouter, Depends, status
from src.schemas.users import User, UsersFilters
from src.schemas.companies import AllCompaniesResponse, CompaniesAdd, CompaniesAddExpected, CompaniesAddResponse, CompaniesAddUserResponse
from src.models.models import Users 
from src.api.dependencies import companies_service 
from src.services.companies import CompaniesService 
from src.api.dependencies import users_service 
from src.services.users import UsersService
from src.auth.dependencies import get_current_user
from fastapi_cache.decorator import cache
from sqlalchemy.exc import SQLAlchemyError 
from src.logger import config_logger
from typing import Annotated
import logging
from src.utils.exceptions import CompanyAlreadyExist, UserNotEmployer, CantAssigneeTaskToEmployer, CompanyNotFound


router = APIRouter(prefix="/companies", tags=["Companies"])


logger = logging.getLogger(__name__)
config_logger() 


@router.get("/", summary="Check all companies (All users)")
@cache(expire=15)
async def check_all_companies(
    companies_service: Annotated[CompaniesService, Depends(companies_service)]
) -> list[AllCompaniesResponse]:
    return [AllCompaniesResponse(name=company.name) for company in await companies_service.get_all()]


@router.get("/{company_id}/", summary="Get all employee from Company (All users)")
@cache(expire=15)
async def get_employee(
    company_id: int, 
    users_service: Annotated[UsersService, Depends(users_service)]
) -> list[User]: 
    return [User(username=user.username, email=user.email) for user in await users_service.get_by_filters(UsersFilters(company=company_id))]


@router.post("/create/", summary="Create company (Employer)", status_code=status.HTTP_201_CREATED)
async def create_company(
    data: CompaniesAddExpected,
    current_user: Annotated[Users, Depends(get_current_user)], 
    companies_service: Annotated[CompaniesService, Depends(companies_service)]
) -> CompaniesAddResponse: 
    companies_name = [comp.name for comp in await companies_service.get_all()] 
    if data.name in companies_name: 
        raise CompanyAlreadyExist

    if current_user.status != "Employer": 
        raise UserNotEmployer
    
    try: 
        await companies_service.add(
            CompaniesAdd(
                name=data.name, 
                creator=current_user.id
            )
        ) 
        return CompaniesAddResponse(CompanyHasCreated=True)
    except (SQLAlchemyError, Exception) as ex: 
        if isinstance(ex, SQLAlchemyError): 
            logger.error("SQLAlchemyError: %s", ex) 
        else: 
            logger.error("Unknown Exc: %s", ex)
        return CompaniesAddResponse(CompanyHasCreated=False) 


@router.patch("/add/{user_id}/to/{company_id}", summary="Add employee to company (Employer)")
async def add_user_to_company(
    user_id: int, company_id: int, 
    current_user: Annotated[Users, Depends(get_current_user)],
    companies_service: Annotated[CompaniesService, Depends(companies_service)],
    users_service: Annotated[UsersService, Depends(users_service)]
) -> CompaniesAddUserResponse:
    companies_id = [comp.id for comp in await companies_service.get_all()]
    if company_id not in companies_id:
        raise CompanyNotFound

    if current_user.status != "Employer": 
        raise UserNotEmployer

    if current_user.id == user_id: 
        raise CantAssigneeTaskToEmployer
    
    try: 
        await users_service.asign_to_company(user_id, company_id)
        return CompaniesAddUserResponse(UserHasBeenAdded=True)
    except (SQLAlchemyError, Exception) as ex: 
        if isinstance(ex, SQLAlchemyError): 
            logger.error("SQLAlchemyError: %s", ex) 
        else: 
            logger.error("Unknown Exc: %s", ex)
        return CompaniesAddUserResponse(UserHasBeenAdded=False)
