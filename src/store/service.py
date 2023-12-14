from src.service import Loader

class StoreLoader(Loader):
    def formation_part_dataset(self, response_rows):
        part_dataset = []
        for store in response_rows:
            part_dataset.append({
                'id': store.get('id'),
                'name': store.get('name'),
                'externalCode': store.get('externalCode'),
                'archived': store.get('archived', False),
                'updated': store.get('updated')})
        return part_dataset

params_store_loader = {
    'entity': 'store',
    'expand': []
}

from pprint import  pprint
store_loader_object = StoreLoader(params=params_store_loader)
result = store_loader_object.formation_full_dataset(test_iteration=True)
pprint(result[2])
print(len(result))
for i in result:
    print(i['name'])