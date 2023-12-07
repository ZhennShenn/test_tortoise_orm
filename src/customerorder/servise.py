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
                Expand("positions", "positions.assortment", "state", "store", "agent")
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
                orders_result_dataset.append({
                    'id_ms': order.get('id'),
                    'code': order.get('name'),
                    'created': order.get('created'),
                    'positions': positions_list,
                    'delivery_date': order.get('deliveryPlannedMoment'),
                    'sum': order.get('sum', 0) / 100,
                    'update_date': order.get('updated'),
                    'state': order.get('state', {}).get('name'),
                    'store': order.get('store', {}).get('name'),
                    'agent': order.get('agent', {}).get('name')
                })
        offset += limit

        if not ('nextHref' in orders.meta):
            break
    return orders_result_dataset


# if __name__ == "__main__":
#     result = formation_order_data(limit=100, offset=0, date_start='2023-08-14 12:00', date_end='2023-08-16 15:00')
#     pprint(result[1:10])

# result = get_orders(limit=3, offset=0, date_start='2023-08-14', date_end='2023-08-15')
# print(result.rows[1])