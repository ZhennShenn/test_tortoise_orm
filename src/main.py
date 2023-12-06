from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse

from tortoise.contrib.fastapi import register_tortoise

from src.config import TORTOISE_ORM, db_url

from src.app.routers import router as app_router
from src.customerorder.routers import router as customerorder_router
from src.product.routers import router as product_router

app = FastAPI()


app.include_router(app_router, prefix="/api/v1", tags=['User'])
app.include_router(customerorder_router, prefix="/api/v1", tags=['CustomerOrder'])
app.include_router(product_router, prefix="/api/v1", tags=['Product'])


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