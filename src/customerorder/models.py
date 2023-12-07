from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class CustomerOrders(models.Model):
    id = fields.UUIDField(pk=True)
    id_ms = fields.CharField(max_length=100)
    code = fields.CharField(max_length=100, unique=True)
    created = fields.DatetimeField()
    positions = fields.JSONField()
    delivery_date = fields.DatetimeField()
    state = fields.CharField(max_length=100)
    update_date = fields.DatetimeField()
    store = fields.CharField(max_length=100)
    sum = fields.FloatField()
    agent = fields.CharField(max_length=100)


CustomerOrderPydantic = pydantic_model_creator(CustomerOrders, name="CustomerOrder")
CustomerOrderInPydantic = pydantic_model_creator(CustomerOrders, name="CustomerOrder")
CustomerOrderPydanticList = pydantic_queryset_creator(CustomerOrders)