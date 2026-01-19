import gc
from app.models.feeding import FeedingModel
from app.models.jar import JarModel
from app.utils.decorators import timeit
import config
from lib import urequests


class DBService(object):
    def __init__(self):
        pass

    def _get_url(self, table, query=None):
        url = f"{config.BASE_URL}{config.BASE_ID}/{table}"
        if query:
            url += f"?{query}"
        return url

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {config.AIRTABLE_TOKEN}",
            "Content-Type": "application/json",
        }

    def _prepare_dict(self, item):
        result = {"id": item["id"]}
        result.update(item["fields"])
        return result

    @timeit
    def create_jar(self, model, retries=3):
        headers = self._get_headers()
        url = self._get_url(config.TABLE_JARS)
        data = {"fields": model.to_dict()}

        try:
            gc.collect()
            print(f"Free mem: {gc.mem_free() / 1000}Kb")
            response = urequests.post(url, headers=headers, json=data)
            response.close()
        except OSError as e:
            print(f"Error posting jar: {e}")
            if retries > 0:
                print(f"Retries: {retries}")
                self.create_jar(model, retries=retries - 1)

    @timeit
    def get_feedings(self, number=2, retries=3):
        headers = self._get_headers()
        url = self._get_url(config.TABLE_FEEDINGS, query=f"pageSize={number}")
        try:
            response = urequests.get(url, headers=headers)
        except Exception as e:
            print(f"Error getting feedings: {e}")
            if retries > 0:
                print(f"Retries: {retries}")
                self.get_feedings(number, retries=retries - 1)

        data = response.json()

        models = []
        for item in data["records"]:
            prepared_item = self._prepare_dict(item)
            model = FeedingModel.from_dict(prepared_item)
            models.append(model)
        return models

    @timeit
    def create_feeding_progress(self, model, retries=3):
        headers = self._get_headers()
        url = self._get_url(config.TABLE_FEEDINGS_PROGRESS)
        data = {"fields": model.to_dict()}

        try:
            gc.collect()
            print(f"Free mem: {gc.mem_free() / 1000}Kb")
            response = urequests.post(url, headers=headers, json=data)
            response.close()
        except OSError as e:
            print(f"Error posting progress: {e}")
            if retries > 0:
                print(f"Retries: {retries}")
            self.create_feeding_progress(model, retries=retries - 1)
