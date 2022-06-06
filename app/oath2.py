from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="tokens")


class User(BaseModel):
    username: str
    password: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", password="password"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user
