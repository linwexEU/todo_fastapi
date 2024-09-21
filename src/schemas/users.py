from pydantic import BaseModel, EmailStr, Field 
from typing import Literal


class User(BaseModel): 
    username: str 
    email: EmailStr | None 


class UsersRegistationExpect(BaseModel): 
    username: str = Field(min_length=1)
    email: EmailStr | None
    status: Literal["Employee", "Employer"]
    password: str


class UsersAdd(BaseModel): 
    username: str = Field(min_length=1)
    email: EmailStr | None
    status: Literal["Employee", "Employer"] 
    hashed_password: str
    

class UsersAuthExpect(BaseModel): 
    username: str 
    password: str 


class UsersAuthResponse(BaseModel): 
    access_token: str


class UsersFilters(BaseModel): 
    id: int | None = None
    username: str | None = None 
    email: EmailStr | None = None
    status: Literal["Employee", "Employer", None] = None
    company: int | None = None


class UsersRegistationResponse(BaseModel): 
    UserHasCreated: bool
    