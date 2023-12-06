from typing import List

from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

from app.models import UserPydantic, UserInPydantic, Users
from config import TORTOISE_ORM, db_url

from app.routers import router as app_router
from customerorder.routers import router as customerorder_router
from product.routers import router as product_router

app = FastAPI()


app.include_router(app_router, prefix="/api/v1", tags=['User'])
app.include_router(customerorder_router, prefix="/api/v1", tags=['CustomerOrder'])
app.include_router(product_router, prefix="/api/v1", tags=['Product'])



register_tortoise(
    app,
    db_url=db_url,
    modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)