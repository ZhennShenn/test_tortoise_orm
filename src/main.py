from typing import List

from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

from app.models import UserPydantic, UserInPydantic, Users
from config import TORTOISE_ORM, db_url

app = FastAPI()


@app.get("/users", response_model=List[UserPydantic])
async def get_users():
    return await UserInPydantic.from_queryset(Users.all())


@app.get("/users/{user_id}", response_model=UserPydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_user(user_id: int):
    return await UserPydantic.from_queryset_single(Users.get(id=user_id))


@app.post("/users", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await UserPydantic.from_tortoise_orm(user_obj)


register_tortoise(
    app,
    db_url=db_url,
    modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)