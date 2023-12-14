from typing import List

from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Stores(models.Model):
    id = fields.UUIDField(pk=True)
    id_ms = fields.CharField(max_length=100)
    archived = fields.BooleanField(default=False)
    externalCode = fields.CharField(max_length=100)
    name = fields.CharField(max_length=200)
    updated = fields.DatetimeField()


StorePydantic = pydantic_model_creator(Stores, name="Store")
StorePydanticList = pydantic_queryset_creator(Stores)
