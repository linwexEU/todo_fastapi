from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from src.schemas.users import UsersAdd, UsersAuthExpect, UsersAuthResponse, UsersFilters, UsersRegistationExpect, UsersRegistationResponse 
from typing import Annotated 
from src.services.users import UsersService 
from src.api.dependencies import users_service
from src.auth.auth import authenticate_user, create_access_token, get_password_hash
from src.config import settings
from src.logger import config_logger
from src.utils.exceptions import UserEmailHasAlreadyExist, UserNameHasAlreadyExist
import logging


router = APIRouter(prefix="/auth", tags=["Auth&Reg"])


logger = logging.getLogger(__name__)
config_logger() 


@router.post("/", summary="Authenticate user")
async def users_auth(response: Response, data: UsersAuthExpect) -> UsersAuthResponse: 
    user = await authenticate_user(data.username, data.password) 
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user[0].id)}) 
    response.set_cookie("auth_token", access_token, max_age=settings.EXPIRE_TOKEN, httponly=True) 
    return UsersAuthResponse(access_token=access_token)


@router.post("/registration/", summary="Register user", status_code=status.HTTP_201_CREATED)
async def users_registration(
    data: UsersRegistationExpect, users_service: Annotated[UsersService, Depends(users_service)]
) -> UsersRegistationResponse: 
    user = await users_service.get_by_filters(UsersFilters(username=data.username))
    if user:
        raise UserNameHasAlreadyExist
    existed_emails = await users_service.get_existed_emails() 
    if data.email in existed_emails: 
        raise UserEmailHasAlreadyExist
                    
    try:
        await users_service.add(UsersAdd(
            username=data.username, 
            email=data.email, 
            status=data.status, 
            hashed_password=get_password_hash(data.password)
        ))
        return UsersRegistationResponse(UserHasCreated=True)
    except (SQLAlchemyError, Exception) as ex:
        if isinstance(ex, SQLAlchemyError):
            logger.error("SQLAlchemyError: %s", ex) 
        else: 
            logger.error("Unknown Exc: %s", ex)
        return UsersRegistationResponse(UserHasCreated=False) 
