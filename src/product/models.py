from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Products(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200)


ProductPydantic = pydantic_model_creator(Products, name="Product")
ProductInPydantic = pydantic_model_creator(Products, name="Product")
ProductPydanticList = pydantic_queryset_creator(Products)