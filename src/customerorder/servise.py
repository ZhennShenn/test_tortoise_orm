from moysklad.exceptions import ApiResponseException
from src.utils import init_ms
from moysklad.queries import Query, Filter, Expand, Select
from pprint import pprint

# Инициализация клиента
client, methods = init_ms()

def get_orders(limit, offset, date_start, date_end):
    """
    Функция для получения списка заказов с использованием Moysklad API.

    Returns:
        moysklad.response.ApiResponse: Объект ответа от Moysklad API.
    """
    try:
        return client.get(
            method=methods.get_list_url("customerorder"),
            query=Query(
                Select(limit=limit, offset=offset),
                Filter().gte("created", date_start) + Filter().lte("created", date_end),
                Expand("positions", "positions.assortment")
            )
        )
    except ApiResponseException as ex:
        print(f"Error fetching orders: {ex}")
        return None

def form_positions_list(order):
    """
    Функция для формирования списка позиций заказа.

    Args:
        order (dict): Заказ из Moysklad API.

    Returns:
        list: Список идентификаторов продуктов в заказе.
    """
    positions_list = []
    for position in order['positions']['rows']:
        positions_list.append(position['assortment']['id'])
    return positions_list

def formation_order_data(date_start, date_end, limit=100, offset=0):
    """
    Функция для формирования датасета заказов для записи в БД.

    Returns:
        dict: Датасет заказов.
    """
    orders_result_dataset = []


    while True:
        orders = get_orders(limit=limit, offset=offset, date_start=date_start, date_end=date_end)

        if orders:
            for order in orders.rows:
                positions_list = form_positions_list(order)
                order_data_dict = {
                    'id': order['id'],
                    'code': order['name'],
                    'date': order['created'],
                    'products': positions_list
                }
                orders_result_dataset.append(order_data_dict)
        offset += limit
        if not ('nextHref' in orders.meta):
            break
    return orders_result_dataset




if __name__ == "__main__":
    result = formation_order_data(limit=100, offset=0, date_start='2023-08-14', date_end='2023-08-15')
    pprint(result)