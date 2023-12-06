from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class CustomerOrders(models.Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=100, unique=True)
    date = fields.DatetimeField()
    products = fields.JSONField()


CustomerOrderPydantic = pydantic_model_creator(CustomerOrders, name="CustomerOrder")
CustomerOrderInPydantic = pydantic_model_creator(CustomerOrders, name="CustomerOrder")
CustomerOrderPydanticList = pydantic_queryset_creator(CustomerOrders)