from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.customerorder.models import CustomerOrderInPydantic, CustomerOrderPydantic, CustomerOrders, \
    CustomerOrderPydanticList
from src.customerorder.service import OrderLoader, params_order_loader

router = APIRouter()


@router.get("/customerorders", response_model=List[CustomerOrderPydantic])
async def get_customerorders():
    return await CustomerOrderInPydantic.from_queryset(CustomerOrders.all())


@router.get("/customerorders/{order_code}", response_model=CustomerOrderPydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_customerorder(order_code: str):
    return await CustomerOrderPydantic.from_queryset_single(CustomerOrders.get(code=order_code))


@router.post("/customerorder", response_model=CustomerOrderPydantic)
async def create_customerorder(order: CustomerOrderInPydantic):
    order_obj = await CustomerOrders.create(**order.dict(exclude_unset=True))
    return await CustomerOrderInPydantic.from_tortoise_orm(order_obj)


@router.post("/customerorders", response_model=CustomerOrderPydanticList)
async def create_customerorder():
    order_obj = OrderLoader(params=params_order_loader)
    orders_data = order_obj.formation_full_dataset(test_iteration=True)

    # Добавляются записи в БД
    await CustomerOrders.bulk_create([CustomerOrders(**order) for order in orders_data])

    # формируется Pydantic схема для ответа пользователю
    orders_schema = await CustomerOrderPydanticList.from_queryset(CustomerOrders.all())

    return orders_schema

