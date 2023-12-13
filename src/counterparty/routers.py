from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.counterparty.models import CounterpartyInPydantic, CounterpartyPydantic, CounterpartyPydanticList, \
    Counterparties
from src.counterparty.service import CounterpartyLoader, params_counterparty_loader

router = APIRouter()


@router.get("/counterparties", response_model=List[CounterpartyPydantic])
async def get_counterparties():
    return await CounterpartyInPydantic.from_queryset(Counterparties.all())


@router.get("/counterparties/{counterparty_code}", response_model=CounterpartyPydantic,
            responses={404: {'model': HTTPNotFoundError}})
async def get_counterparty(counterparty_code: str):
    return await CounterpartyPydantic.from_queryset_single(Counterparties.get(code=counterparty_code))


@router.post("/counterparty", response_model=CounterpartyPydantic)
async def create_counterparty(counterparty: CounterpartyInPydantic):
    counterparty_obj = await Counterparties.create(**counterparty.dict(exclude_unset=True))
    return await CounterpartyInPydantic.from_tortoise_orm(counterparty_obj)


@router.post("/counterparties", response_model=CounterpartyPydanticList)
async def create_counterparties():
    counterparty_obj = CounterpartyLoader(params=params_counterparty_loader)
    counterparties_data = counterparty_obj.formation_full_dataset(test_iteration=True)

    # Добавляются записи в БД
    await Counterparties.bulk_create([Counterparties(**counterparty) for counterparty in counterparties_data])

    # формируется Pydantic схема для ответа пользователю
    counterparties_schema = await CounterpartyPydanticList.from_queryset(Counterparties.all())

    return counterparties_schema

