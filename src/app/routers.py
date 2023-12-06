from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.app.models import UserInPydantic, UserPydantic, Users

router = APIRouter()


@router.get("/users", response_model=List[UserPydantic])
async def get_users():
    return await UserInPydantic.from_queryset(Users.all())


@router.get("/users/{user_id}", response_model=UserPydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_user(user_id: int):
    return await UserPydantic.from_queryset_single(Users.get(id=user_id))


@router.post("/users", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await UserPydantic.from_tortoise_orm(user_obj)