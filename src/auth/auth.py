from passlib.context import CryptContext 
import jwt
from datetime import datetime, timedelta, timezone 
from src.schemas.users import UsersFilters
from src.config import settings
from src.api.dependencies import users_service 
from src.services.users import UsersService 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str: 
    return pwd_context.hash(password) 


def verify_password(plain_password: str, hashed_password: str) -> bool: 
    return pwd_context.verify(plain_password, hashed_password) 


def create_access_token(data: dict): 
    to_encode = data.copy() 
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.EXPIRE_TOKEN) 
    to_encode.update({"exp": expire}) 
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt 


async def authenticate_user(username: str, password: str, users_service: UsersService = users_service()): 
    user = await users_service.get_by_filters(UsersFilters(username=username)) 
    if not user: 
        return None 
    if not verify_password(password, user[0].hashed_password): 
        return None 
    return user 


