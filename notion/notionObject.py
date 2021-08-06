from abc import ABC, abstractmethod
import requests

class NotionObject(ABC):
    def __init__(self, headers, id):
        self.headers = headers
        self.id = id

    @property
    @abstractmethod
    def origin(self):
        pass

    def get(self):
        return self.request("get", self.url())

    def url(self, endpoint=""):
        return f"https://api.notion.com/v1/{self.origin}/{self.id}" + endpoint

    def request(self, method, url, **kwargs):
        return requests.request(method, url, headers=self.headers, **kwargs)


class NotionDatabase(NotionObject):
    @property
    def origin(self):
        return "databases"

    def query(self, body):
        return self.request("post", self.url("/query"), json=body)

    def list(self, query):
        return self.request("get", self.url(), params=query)

    def create(self, body):
        return self.request("post", self.url(), json=body)


class NotionPage(NotionObject):
    @property
    def origin(self):
        return "pages"

    def create(self, body):
        return self.request("post", self.url(), json=body)

    def update(self, body):
        return self.request("patch", self.url(), json=body)


class NotionBlock(NotionObject):
    @property
    def origin(self):
        return "blocks"

    def children(self, query):
        return self.request("get", self.url("/children"), params=query)
    
    def update(self, body):
        return self.request("patch", self.url(), json=body)

    def append(self, body):
        return self.request("patch", self.url("/children"), json=body)


class NotionUser(NotionObject):
    @property
    def origin(self):
        return "users"

    def list(self, query):
        return self.request("get", self.url(), params=query)
