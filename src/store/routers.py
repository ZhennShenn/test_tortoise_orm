from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.store.models import StorePydantic, StorePydanticList, Stores
from src.store.service import params_store_loader, StoreLoader

router = APIRouter()


@router.get("/stores", response_model=List[StorePydantic])
async def get_stores():
    return await StorePydantic.from_queryset(Stores.all())


@router.get("/stores/{store_id_ms}", response_model=StorePydantic,
            responses={404: {'model': HTTPNotFoundError}})
async def get_store(store_id_ms: str):
    return await StorePydantic.from_queryset_single(Stores.get(id_ms=store_id_ms))


@router.post("/store", response_model=StorePydantic)
async def create_store(store: StorePydantic):
    store_obj = await Stores.create(**store.dict(exclude_unset=True))
    return await StorePydantic.from_tortoise_orm(store_obj)


@router.post("/stores", response_model=StorePydanticList)
async def create_stores():
    store_obj = StoreLoader(params=params_store_loader)
    stores_data = store_obj.formation_full_dataset(test_iteration=True)

    # Добавляются записи в БД
    await Stores.bulk_create([Stores(**store) for store in stores_data])

    # формируется Pydantic схема для ответа пользователю
    stores_schema = await StorePydanticList.from_queryset(Stores.all())

    return stores_schema

