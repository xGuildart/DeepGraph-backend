import os
import rsa
from datetime import timedelta
from black import logging
from fastapi import FastAPI, Body, HTTPException, status, Query, Depends, Response, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from logger.log import logging
from odmantic import AIOEngine, query
from bson import Binary
from app.db import get_engine
from app.models import Genz, User_ch, UserUpdate, Young, User, User_up
from app.oath2 import get_current_user, get_current_active_user, create_access_token, Token
from app.utils import string_to_key

ACCESS_TOKEN_EXPIRE_MINUTES = 30
DEBUG = os.environ['DEBUG']

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*"
]

if(DEBUG):
    hosts = [
        "localhost",
        "127.0.0.1"
    ]
else:
    hosts = []


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


@app.get("/")
async def home(current_uer: User = Depends(get_current_user)):
    logging.info("log debug################    ")
    return {" this page is a web service; add /docs to see the api"}


async def authenticate_user(form_data: OAuth2PasswordRequestForm, request: Request, engine=Depends(get_engine)):
    cred = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if form_data.client_secret == "*secret*":
        client_host = request.client.host
        if(client_host in hosts):
            if(form_data.password == "*password*" and form_data.username == "*user*"):
                fuser = os.environ['APP_USER']
                fpswd = os.environ['APP_PSWD']
            else:
                raise cred
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Client not allowed",
                headers={"WWW-Authenticate": "Bearer"},
            )

    else:
        fuser = form_data.username
        fpswd = form_data.password

    user = await engine.find_one(User, User.username == fuser)
    if user is None:
        raise cred

    dbpass = rsa.decrypt(user.password, private_key).decode('ascii')
    if not (fpswd == dbpass and user.permission == "admin"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password, or no privileged user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@ app.post("/tokens", response_model=Token)
async def login_for_access_token(request: Request, engine=Depends(get_engine), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data, request, engine=engine)
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


@ app.get(
    "/genz", response_description="List all genz collection", response_model=List[Genz]
)
async def list_genz(response: Response, engine=Depends(get_engine), offset: int = 0, limit: int = Query(default=10, lte=1000),
                    current_uer: User = Depends(get_current_user)):

    genz = await engine.find(Genz, Genz.id >= offset, Genz.id < limit)
    return genz


@ app.get(
    "/young", response_description="List all young collection", response_model=List[Young]
)
async def list_young(response: Response, engine=Depends(get_engine), offset: int = 0, limit: int = Query(default=10, lte=70),
                     current_uer: User = Depends(get_current_user)):

    young = await engine.find(Young, Young.id >= offset, Young.id < limit)
    return young


@ app.get(
    "/genz/{id}", response_description="Get a single genz", response_model=Genz)
async def show_genz(id: int, response: Response, engine=Depends(get_engine), current_uer: User = Depends(get_current_user)):

    if (genz := await engine.find_one(Genz, Genz.id == id)) is not None:
        return genz

    raise HTTPException(status_code=404, detail=f"Genz {id} not found")


@ app.get(
    "/young/{id}", response_description="Get a single young", response_model=Young)
async def show_young(id: int, response: Response, engine=Depends(get_engine), current_uer: User = Depends(get_current_user)):

    if (young := await engine.find_one(Young, Young.id == id)) is not None:
        return young

    raise HTTPException(status_code=404, detail=f"Young {id} not found")


@ app.post("/user", response_description="Add new User", response_model=User)
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

        passw = rsa.encrypt(user['password'].encode(), public_key)
        user = User(username=user['username'],
                    password=passw, email=user['email'])
        new_user = await engine.save(user)
        created_user = await engine.find_one(User, User.id == new_user.id)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=created_user.to_dict())


@ app.patch("/users/{name}", response_model=User_up)
async def update_user_by_name(name: str, engine: AIOEngine = Depends(get_engine), current_user:  User = Depends(get_current_user)):
    queryUser = query.or_(User.username == name, User.email == name)
    user = await engine.find_one(User, queryUser)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username Not found! update failed")
    else:
        if user.limit:
            patchUser = UserUpdate()
            patchUser.connection = user.connection + 1
            user.update(patchUser)
            await engine.save(user)
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"identifier": user.username, "con": user.connection})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"identifier": "VIP", "con": 0})


@ app.post(
    "/checkUser", response_description="Sign In", response_model=User)
async def check_user(user: User_ch = Body(...), engine=Depends(get_engine), current_user: User = Depends(get_current_user)):
    user = jsonable_encoder(user)

    credentials = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Username or password or both are incorrect!")

    qUser = query.or_(
        User.username == user["identifier"], User.email == user["identifier"])
    if (dbuser := await engine.find_one(User, qUser)) is not None:
        print(dbuser.password)
        dbpass = rsa.decrypt(dbuser.password, private_key).decode('ascii')
        if dbpass == user['password']:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                                content=True)
        else:
            raise credentials
    else:
        raise credentials


@ app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
