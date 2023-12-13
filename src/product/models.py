from typing import List

from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Products(models.Model):
    id = fields.UUIDField(pk=True)
    id_ms = fields.CharField(max_length=100)
    name = fields.CharField(max_length=200)
    code = fields.CharField(max_length=100, unique=True)
    description = fields.CharField(max_length=1000, null=True)
    category = fields.CharField(max_length=100, null=True)
    barcodes = fields.JSONField()
    group = fields.CharField(max_length=100)
    update_info = fields.DatetimeField(null=True)
    supplier = fields.CharField(max_length=100)


ProductPydantic = pydantic_model_creator(Products, name="Product")
ProductInPydantic = pydantic_model_creator(Products, name="Product")
ProductPydanticList = pydantic_queryset_creator(Products)