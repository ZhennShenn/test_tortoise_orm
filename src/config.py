from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

db_url = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

moysklad_login = os.environ.get("MOYSKLAD_LOGIN")
moysklad_password = os.environ.get("MOYSKLAD_PASS")
moysklad_token = os.environ.get("MOYSKLAD_TOKEN")

TORTOISE_ORM = {
    "connections": {
        "default": db_url
    },
    "apps": {
        "models": {
            "models": ["src.app.models", "src.customerorder.models", "src.product.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
