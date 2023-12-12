from moysklad.exceptions import ApiResponseException
from moysklad.queries import Expand, Filter, Select, Query

from src.utils import init_ms

class Loader:
    def __init__(self, params={}):
        self.client, self.methods = init_ms()
        self.limit = 100
        self.offset = 0

        # Установка параметров, как атрибутов
        for key, value in params.items():
            setattr(self, key, value)

    def get_response(self):
        try:
            return self.client.get(
                method=self.methods.get_list_url(self.entity),
                query=Query(
                    Select(limit=self.limit, offset=self.offset),
                    Expand(*self.expand)
                )
            )
        except ApiResponseException as ex:
            print(f"Error fetching orders: {ex}")
            return None

    def formation_full_dataset(self, test_iteration=False):
        result = []
        while True:
            response = self.get_response()
            if not response:
                break

            part_dataset = self.formation_part_dataset(response.rows)
            result.extend(part_dataset)

            self.offset += self.limit

            if not ('nextHref' in response.meta) or test_iteration:
                break

        return result

    def formation_part_dataset(self, response_rows):
        pass


