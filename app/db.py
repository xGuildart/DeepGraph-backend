import os
import motor.motor_asyncio
from odmantic import AIOEngine

# from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = os.environ["MONGODB_URL"]
# engine = create_engine(DATABASE_URL, echo=True)
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)


def get_engine():
    return AIOEngine(motor_client=client, database="deeplabs")
