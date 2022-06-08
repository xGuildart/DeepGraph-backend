import os
import rsa

from datetime import timedelta
from black import logging
from fastapi import FastAPI, Body, HTTPException, status, Query, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from logger.log import logging
from odmantic import AIOEngine, query

from app.db import get_engine
from app.models import Genz, Young, User
from app.oath2 import get_current_user, get_current_active_user, create_access_token, Token
from app.utils import string_to_key

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


private_key: rsa.PrivateKey = string_to_key(
    os.environ["private_key"], "private")
public_key: rsa.PublicKey = string_to_key(os.environ["public_key"], "pub")

pem = private_key.save_pkcs1("PEM")
print(pem)


@app.get("/")
async def home(current_uer: User = Depends(get_current_user)):
    logging.info("log debug################    ")
    return {" this page is web service; add /docs to see the api"}


async def authenticate_user(form_data: OAuth2PasswordRequestForm, engine=Depends(get_engine)):
    user = await engine.find_one(User, User.username == form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password = form_data.password
    dbpass = rsa.decrypt(user.password, private_key).decode('ascii')
    if not (password == dbpass and user.permission == "admin"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password, or no privileged user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@app.post("/tokens", response_model=Token)
async def login_for_access_token(engine=Depends(get_engine), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data, engine=engine)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    "/genz", response_description="List all genz collection", response_model=List[Genz]
)
async def list_genz(response: Response, engine=Depends(get_engine), offset: int = 0, limit: int = Query(default=10, lte=1000),
                    current_uer: User = Depends(get_current_user)):

    genz = await engine.find(Genz, Genz.id > offset, Genz.id < limit)
    return genz


@app.get(
    "/young", response_description="List all young collection", response_model=List[Young]
)
async def list_young(response: Response, engine=Depends(get_engine), offset: int = 0, limit: int = Query(default=10, lte=70),
                     current_uer: User = Depends(get_current_user)):

    young = await engine.find(Young, Young.id > offset, Young.id < limit)
    return young


@app.get(
    "/genz/{id}", response_description="Get a single genz", response_model=Genz)
async def show_genz(id: int, response: Response, engine=Depends(get_engine), current_uer: User = Depends(get_current_user)):

    if (genz := await engine.find_one(Genz, Genz.id == id)) is not None:
        return genz

    raise HTTPException(status_code=404, detail=f"Genz {id} not found")


@app.get(
    "/young/{id}", response_description="Get a single young", response_model=Young)
async def show_young(id: int, response: Response, engine=Depends(get_engine), current_uer: User = Depends(get_current_user)):

    if (young := await engine.find_one(Young, Young.id == id)) is not None:
        return young

    raise HTTPException(status_code=404, detail=f"Young {id} not found")


@app.post("/user", response_description="Add new User", response_model=User)
async def create_user(user: User = Body(...), engine: AIOEngine = Depends(get_engine), current_user: User = Depends(get_current_user)):
    user = jsonable_encoder(user)

    # check username and email unicity
    unicity = query.or_(
        User.username == user["username"], User.email == user["email"])
    user_db = await engine.find_one(User, unicity)
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,
            detail="Username or email already used!")
    else:

        #passw = rsa.encrypt(user['password'].encode(), public_key)
        user = User(username=user['username'],
                    password=user['password'], email=user['email'])
        new_user = await engine.save(user)
        created_user = await engine.find_one(User, User.id == new_user.id)
        JSONResponse(status_code=status.HTTP_201_CREATED,
                     content=created_user.to_dict())


@app.get(
    "/checkUser", response_description="Sign In", response_model=User)
async def check_user(user: User = Body(...), engine=Depends(get_engine), current_uer: User = Depends(get_current_user)):
    user = jsonable_encoder(user)

    credentials = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Username or password or both are incorrect!")

    if (dbuser := await engine.find_one(User, User.username == user['username'])) is not None:
        dbpass = rsa.decrypt(dbuser.password, private_key).decode('ascii')
        if dbpass == user['password']:
            JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                         content={"data": True})

        raise credentials

    raise credentials


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
