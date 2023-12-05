from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class User(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=1000)
    is_active = fields.BooleanField(default=True)

    async def save(self, *args, **kwargs) -> None:
        self.hashed_password = '123456'
        await super().save(*args, **kwargs)

    class PydanticMeta:
        exclude = ['hashed_password']

UserPydantic = pydantic_model_creator(User, name="User")
UserInPydantic = pydantic_model_creator(User, name='User', exclude_readonly=True)
UserPydanticList = pydantic_queryset_creator(User)