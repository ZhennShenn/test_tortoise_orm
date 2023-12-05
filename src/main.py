from typing import List

from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

from app.models import UserPydantic, UserInPydantic, Users
from config import TORTOISE_ORM, db_url

from app.routers import router as app_router

app = FastAPI()


app.include_router(app_router, prefix="/api/v1", tags=['users'])



register_tortoise(
    app,
    db_url=db_url,
    modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)