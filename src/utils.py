"""Utils"""
from moysklad.api import ApiUrlRegistry, MoySklad, MoySkladHttpClient

# import config
from .config import moysklad_login, moysklad_password, moysklad_token


def init_ms() -> tuple[MoySkladHttpClient, ApiUrlRegistry]:
    """Initialize MoySklad Client

    Returns:
        tuple[MoySkladHttpClient, ApiUrlRegistry]: Return Client and Methods
    """
    sklad = MoySklad.get_instance(
        moysklad_login, moysklad_password, moysklad_token
    )
    client = sklad.get_client()
    methods = sklad.get_methods()
    return client, methods


