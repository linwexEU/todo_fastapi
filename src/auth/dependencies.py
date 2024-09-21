from fastapi import Depends, Request, HTTPException, status
from typing import Annotated
from src.api.dependencies import users_service
from src.services.users import UsersService
from src.config import settings
from datetime import datetime, timezone
import jwt

from src.utils.exceptions import TokenHasBeenExpired, UserNotFound


def get_token(request: Request):
    token = request.cookies.get("auth_token")
    if not token: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: Annotated[str, Depends(get_token)], users_service: Annotated[UsersService, Depends(users_service)]): 
    try: 
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: str = payload.get("exp") 
    if not expire or int(expire) < datetime.now(timezone.utc).timestamp():
        raise TokenHasBeenExpired
    user_id: str = payload.get("sub")
    if not user_id: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await users_service.get_by_id(int(user_id))
    if not user: 
        raise UserNotFound
    return user 
