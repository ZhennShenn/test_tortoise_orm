from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Counterparties(models.Model):
    id = fields.UUIDField(pk=True)
    id_ms = fields.CharField(max_length=100)
    name = fields.CharField(max_length=255)
    inn = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=255)
    companyType = fields.CharField(max_length=255)
    created = fields.DatetimeField(null=True)
    externalCode = fields.CharField(max_length=255)
    group = fields.CharField(max_length=255, null=True)
    tags = fields.JSONField()
    updated = fields.DatetimeField(null=True)
    archived = fields.BooleanField(default=False)
    salesAmount = fields.FloatField(default=0.0)


class Counterparties_Attributes(models.Model):
    id = fields.UUIDField(pk=True)
    id_ms = fields.CharField(max_length=100)
    name = fields.CharField(max_length=255)
    type = fields.CharField(max_length=255)
    value = fields.CharField(max_length=255)

    counterparty = fields.ForeignKeyField(
        "models.Counterparties", related_name="attributes"
    )


CounterpartyPydantic = pydantic_model_creator(Counterparties, name="Counterparty")
CounterpartyInPydantic = pydantic_model_creator(Counterparties, name="Counterparty")
CounterpartyPydanticList = pydantic_queryset_creator(Counterparties)