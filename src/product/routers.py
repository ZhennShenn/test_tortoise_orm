from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from .models import ProductInPydantic, ProductPydantic, Products

router = APIRouter()


@router.get("/products", response_model=List[ProductPydantic])
async def get_products():
    return await ProductInPydantic.from_queryset(Products.all())


@router.get("/products/{user_id}", response_model=ProductPydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_product(product_id: int):
    return await ProductPydantic.from_queryset_single(Products.get(id=product_id))


@router.post("/products", response_model=ProductPydantic)
async def create_product(product: ProductInPydantic):
    product_obj = await Products.create(**product.dict(exclude_unset=True))
    return await ProductInPydantic.from_tortoise_orm(product_obj)