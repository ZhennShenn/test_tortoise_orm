from src.service import Loader
from pprint import pprint

params = {
    'entity': 'customerorder',
    'expand': ["positions", "positions.assortment", "state", "store", "agent"]

}

class OrderLoader(Loader):

    def formation_part_dataset(self, response_rows):
        part_dataset = []
        for order in response_rows:
            positions_list = self.formation_positions_list(order)
            part_dataset.append({
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
        return part_dataset

    def formation_positions_list(self, order):
        positions_list = []
        for position in order['positions']['rows']:
            positions_list.append(position['assortment']['id'])
        return positions_list

params_order_loader = {
    'entity': 'customerorder',
    'expand': ["positions", "positions.assortment", "state", "store", "agent"]

}


# import time
#
#
# start_time = time.time()
#
#
# order_obj = OrderLoader(params=params)
# result = order_obj.formation_full_dataset(test_iteration=True)
# pprint(result)
# print(len(result))
#
#
# end_time = time.time()
# duration = end_time - start_time
# print(f'Duration: {duration} seconds')