from abc import ABC, abstractmethod

class Model:
    def __init__(self):
        self.properties = {}
        self.id = ""

class Schema(ABC):
    def __init__(self, client, database_id, page):
        self.client = client
        self.database_id = database_id
        self.page = page

    "pages"

    def create(self, document, **kwargs) -> int:
        res = self.client.pages.create(parent={"database_id": self.database_id}, properties=document.properties, **kwargs)
        return 0 if len(res) else -1

    def update(self, document, **kwargs) -> int:
        res = self.client.pages.update(page_id=document.id, properties=document.properties, **kwargs)
        return 0 if len(res) else -1

    "databases"

    def retrieve(self):
        return self.client.databases.retrieve(database_id=self.database_id)

    def query(self, filter={}, sorts=[], **kwargs) -> list:
        pages = []

        for p in self.client.databases.query(database_id=self.database_id, filter=filter, sorts=sorts, **kwargs)["results"]:
            page = self.page()
            page.properties = p["properties"]
            page.id = p["id"]
            pages.append(page)

        return pages