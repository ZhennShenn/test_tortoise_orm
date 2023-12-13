from src.service import Loader

class ProductLoader(Loader):

    def formation_part_dataset(self, response_rows):
        part_dataset = []
        for product in response_rows:

            part_dataset.append({
                    'id_ms': product.get('id'),
                    'name': product.get('name'),
                    'code': product.get('code'),
                    'description': product.get('description'),
                    'category': self.get_category_from_attributes(product.get('attributes', [])),
                    'barcodes': product.get('barcodes'),
                    'group': product.get('group', {}).get('name'),
                    'updated_info': product.get('updated'),
                    'supplier':product.get('supplier', {}).get('name')
                })
        return part_dataset

    def get_category_from_attributes(self, attributes):
        category_attribute_name = 'Категория'
        category_value = None

        for attribute in attributes:
            if attribute.get('name') == category_attribute_name:
                category_value = attribute.get('value')
                break

        return category_value

params_product_loader = {'entity': 'product',
    'expand': ["group", "supplier"]}

# from pprint import pprint
# product_loader_object = ProductLoader(params=params_product_loader)
# result = product_loader_object.formation_full_dataset(test_iteration=True)
# pprint(result[2])
# for i in result:
#     print(i['barcodes'])
# print(len(result))