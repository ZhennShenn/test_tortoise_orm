from src.service import Loader
from pprint import pprint

class CounterpartyLoader(Loader):

    def formation_part_dataset(self, response_rows):
        part_dataset = []

        for counterparty in response_rows:
            part_dataset.append({
                'id_ms': counterparty.get('id'),
                'name': counterparty.get('name'),
                'inn': counterparty.get('inn'),
                'phone': counterparty.get('phone'),
                'companyType': counterparty.get('companyType'),
                'created': counterparty.get('created'),
                'externalCode': counterparty.get('externalCode'),
                'group': counterparty.get('group', {}).get('name'),
                'tags': counterparty.get('tags', []),
                'updated': counterparty.get('updated'),
                'archived': counterparty.get('archived', False),
                'salesAmount': counterparty.get('salesAmount', 0.0),
                'attributes': [
                    {
                        'id_ms': attribute['id'],
                        'name': attribute['name'],
                        'type': attribute['type'],
                        'value': attribute['value']
                    }
                    for attribute in counterparty.get('attributes', [])
                ]
            })
        return part_dataset
params_counterparty_loader = {
    'entity': 'counterparty',
    'expand':[],
                              }

# counterparty = CounterpartyLoader(params=params_counterparty_loader)
# result = counterparty.formation_full_dataset(test_iteration=True)
# print(len(result))
# pprint(result[1])