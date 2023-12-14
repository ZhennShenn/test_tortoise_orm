import time

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse

from debug_toolbar.middleware import DebugToolbarMiddleware

from tortoise.contrib.fastapi import register_tortoise

from src.config import TORTOISE_ORM, db_url

from src.app.routers import router as app_router
from src.customerorder.routers import router as customerorder_router
from src.product.routers import router as product_router
from src.counterparty.routers import router as counterparty_router
from src.store.routers import router as store_router

description = """
App API helps you enrich the data in the database.

## Entities

You can **read or create one or more elements for each entity (eg product)**.

## Users

You can:

* **Create users**.
* **Get info about some user by id**.
* **Get users info**.
"""

tags_metadata = [
    {
        "name": "User",
        "description": "Operations with users.",
    },
    {
        "name": "Counterparty",
        "description": "Obtaining and adding information in data base.",
    },
    {
        "name": "CustomerOrder",
        "description": "Obtaining and adding information in data base.",
    },
    {
        "name": "Product",
        "description": "Obtaining and adding information in data base.",
    },
]

app = FastAPI(debug=True, description=description, openapi_tags=tags_metadata)

app.add_middleware(DebugToolbarMiddleware, panels=["debug_toolbar.panels.tortoise.TortoisePanel"])


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.include_router(app_router, prefix="/api/v1", tags=['User'])
app.include_router(customerorder_router, prefix="/api/v1", tags=['CustomerOrder'])
app.include_router(product_router, prefix="/api/v1", tags=['Product'])
app.include_router(counterparty_router, prefix="/api/v1", tags=['Counterparty'])
app.include_router(store_router, prefix="/api/v1", tags=['Store'])


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


register_tortoise(
    app,
    db_url=db_url,
    modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)