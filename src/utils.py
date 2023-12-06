"""Utils"""
from moysklad.api import ApiUrlRegistry, MoySklad, MoySkladHttpClient

import config


def init_ms() -> tuple[MoySkladHttpClient, ApiUrlRegistry]:
    """Initialize MoySklad Client

    Returns:
        tuple[MoySkladHttpClient, ApiUrlRegistry]: Return Client and Methods
    """
    sklad = MoySklad.get_instance(
        config.moysklad_login, config.moysklad_password, config.moysklad_token
    )
    client = sklad.get_client()
    methods = sklad.get_methods()
    return client, methods


