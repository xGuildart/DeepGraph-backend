import os

from ast import For
from typing import Optional
from email.policy import default
from textwrap import indent
from unittest import skip
from black import logging
from fastapi import FastAPI, Body, HTTPException, status, Query, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from typing import Optional, List
from logger.log import logging
from odmantic import ObjectId

from app.db import get_engine
from app.models import Genz, Young
from app.oath2 import get_current_user, User

app = FastAPI()


logging.info("log debug################    ")


@app.get("/")
async def home(current_uer: User = Depends(get_current_user)):
    logging.info("log debug################    ")

    #verify_response(response, token)

    return {" this page is web service; add /docs to see the api"}


@app.get(
    "/genz", response_description="List all genz collection", response_model=List[Genz]
)
async def list_genz(response: Response, engine=Depends(get_engine), offset: int = 0, limit: int = Query(default=10, lte=1000),
                    current_uer: User = Depends(get_current_user)):
    #verify_response(response, token)

    genz = await engine.find(Genz, Genz.id > offset, Genz.id < limit)
    return genz


@app.get(
    "/young", response_description="List all young collection", response_model=List[Young]
)
async def list_young(response: Response, engine=Depends(get_engine), offset: int = 0, limit: int = Query(default=10, lte=70),
                     current_uer: User = Depends(get_current_user)):
    #verify_response(response, token)

    young = await engine.find(Young, Young.id > offset, Young.id < limit)
    return young


@app.get(
    "/genz/{id}", response_description="Get a single genz", response_model=Genz)
async def show_genz(id: int, response: Response, engine=Depends(get_engine), current_uer: User = Depends(get_current_user)):
    #verify_response(response, token)

    if (genz := await engine.find_one(Genz, Genz.id == id)) is not None:
        return genz

    raise HTTPException(status_code=404, detail=f"Genz {id} not found")


@app.get(
    "/young/{id}", response_description="Get a single young", response_model=Young)
async def show_young(id: int, response: Response, engine=Depends(get_engine), current_uer: User = Depends(get_current_user)):
    # verify_response(response, token)

    if (young := await engine.find_one(Young, Young.id == id)) is not None:
        return young

    raise HTTPException(status_code=404, detail=f"Young {id} not found")


# def verify_response(response: Response, token: str = Depends(token_auth_scheme)):
#     """A valid access token is required to access this route"""

#     result = VerifyToken(token.credentials).verify()

#     if result.get("status"):
#         response.status_code = status.HTTP_400_BAD_REQUEST
#         return result

#     getlog().debug(result)
