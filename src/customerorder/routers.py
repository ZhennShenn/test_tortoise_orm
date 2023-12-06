from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.customerorder.models import CustomerOrderInPydantic, CustomerOrderPydantic, CustomerOrders
from src.customerorder.servise import formation_order_data

router = APIRouter()


@router.get("/customerorders", response_model=List[CustomerOrderPydantic])
async def get_customerorders():
    return await CustomerOrderInPydantic.from_queryset(CustomerOrders.all())


@router.get("/customerorders/{order_id}", response_model=CustomerOrderPydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_customerorder(order_id: int):
    return await CustomerOrderPydantic.from_queryset_single(CustomerOrders.get(id=order_id))


@router.post("/customerorder", response_model=CustomerOrderPydantic)
async def create_customerorder(order: CustomerOrderInPydantic):
    order_obj = await CustomerOrders.create(**order.dict(exclude_unset=True))
    return await CustomerOrderInPydantic.from_tortoise_orm(order_obj)


@router.post("/customerorders", response_model=List[CustomerOrderPydantic])
async def create_customerorder(orders: List[CustomerOrderInPydantic]):
    orders = formation_order_data(limit=3, offset=0, date_start='2023-08-14', date_end='2023-08-15')
    order_objs = await CustomerOrders.bulk_create([CustomerOrders(**order.dict(exclude_unset=True)) for order in orders])
    return await CustomerOrderInPydantic.from_tortoise_orm(order_objs)