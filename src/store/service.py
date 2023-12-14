from src.service import Loader
from src.store.models import Stores


class StoreLoader(Loader):
    def formation_part_dataset(self, response_rows):
        part_dataset = []
        for store in response_rows:
            part_dataset.append({
                'id_ms': store.get('id'),
                'name': store.get('name'),
                'externalCode': store.get('externalCode'),
                'archived': store.get('archived', False),
                'updated': store.get('updated')})
        return part_dataset

params_store_loader = {
    'entity': 'store',
    'expand': []
}

# from pprint import  pprint
# store_loader_object = StoreLoader(params=params_store_loader)
# result = store_loader_object.formation_full_dataset(test_iteration=True)
# Stores.bulk_create([Stores(**store) for store in result])