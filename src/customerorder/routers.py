from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from .models import CustomerOrderInPydantic, CustomerOrderPydantic, CustomerOrders

router = APIRouter()


@router.get("/customerorders", response_model=List[CustomerOrderPydantic])
async def get_customerorders():
    return await CustomerOrderInPydantic.from_queryset(CustomerOrders.all())


@router.get("/customerorders/{order_id}", response_model=CustomerOrderPydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_customerorder(order_id: int):
    return await CustomerOrderPydantic.from_queryset_single(CustomerOrders.get(id=order_id))


@router.post("/customerorders", response_model=CustomerOrderPydantic)
async def create_customerorder(order: CustomerOrderInPydantic):
    order_obj = await CustomerOrders.create(**order.dict(exclude_unset=True))
    return await CustomerOrderInPydantic.from_tortoise_orm(order_obj)