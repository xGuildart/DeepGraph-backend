import os
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from odmantic import AIOEngine
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.db import get_engine
from app.models import User
from jose import JWTError, jwt
from logger.log import EchoService

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="tokens")


# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
# the __name__ resolve to "main" since we are at the root of the project.
logger = logging.getLogger(__name__)
# This will get the root logger since no logger in the configuration has this name.


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    password: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user(token: str, engine: AIOEngine = get_engine()):
    user = await engine.find_one(User, User.username == token)
    if user is not None:
        return UserInDB(**user.to_dict())


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        print('token:::::::::::::: ' + token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print('username:' + username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
