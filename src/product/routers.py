from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.product.models import ProductInPydantic, ProductPydantic, Products, ProductPydanticList
from src.product.service import ProductLoader, params_product_loader

router = APIRouter()


@router.get("/products", response_model=List[ProductPydantic])
async def get_products():
    return await ProductInPydantic.from_queryset(Products.all())


@router.get("/products/{product_code}", response_model=ProductPydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_product(product_code: str):
    return await ProductPydantic.from_queryset_single(Products.get(code=product_code))


@router.post("/product", response_model=ProductPydantic)
async def create_product(product: ProductInPydantic):
    product_obj = await Products.create(**product.dict(exclude_unset=True))
    return await ProductInPydantic.from_tortoise_orm(product_obj)


@router.post("/products", response_model=ProductPydanticList)
async def create_customerorder():
    product_obj = ProductLoader(params=params_product_loader)
    products_data = product_obj.formation_full_dataset(test_iteration=True)

    # Добавляются записи в БД
    await Products.bulk_create([Products(**product) for product in products_data])

    # формируется Pydantic схема для ответа пользователю
    products_schema = await ProductPydanticList.from_queryset(Products.all())

    return products_schema