from abc import ABC, abstractmethod
import requests

class NotionDocument(ABC):
    def __init__(self, headers):
        self._headers = headers

    @property
    @abstractmethod
    def _origin(self):
        pass

    def _url(self, endpoint=""):
        return f"https://api.notion.com/v1/{self._origin}/" + endpoint

    def _request(self, method, url, **kwargs):
        return requests.request(method, url, headers=self._headers, **kwargs)

class NotionObject(NotionDocument):
    def __init__(self, headers, id):
        super().__init__(headers)
        self._id = id

    def _url(self, endpoint=""):
        return super()._url(self._id + endpoint)

    def retrieve(self):
        return self._request("get", self._url())

class NotionDatabase(NotionObject):
    @property
    def _origin(self):
        return "databases"

    def query(self, body):
        return self._request("post", self._url("/query"), json=body)

    def list(self, query={}):
        return self._request("get", self._url(), params=query)

    def create(self, body):
        return self._request("post", self._url(), json=body)


class NotionPage(NotionObject):
    @property
    def _origin(self):
        return "pages"

    def create(self, body):
        return self._request("post", self._url(), json=body)

    def update(self, body):
        return self._request("patch", self._url(), json=body)


class NotionBlock(NotionObject):
    @property
    def _origin(self):
        return "blocks"

    def children(self, query):
        return self._request("get", self._url("/children"), params=query)

    def update(self, body):
        return self._request("patch", self._url(), json=body)

    def append(self, body):
        return self._request("patch", self._url("/children"), json=body)


class NotionUser(NotionObject):
    @property
    def _origin(self):
        return "users"

    def list(self, query):
        return self._request("get", self._url(), params=query)

class NotionSearch(NotionDocument):
    @property
    def _origin(self):
        return "search"

    def search(self, body):
        return self._request("post", self._url(), json=body)