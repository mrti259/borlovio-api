import requests

class NotionObject:
    OBJECT = ""

    def __init__(self, headers, id):
        self.headers = headers
        self.id = id

    def get(self):
        return self.request("get", self.url())

    def url(self, endpoint=""):
        return f"https://api.notion.com/v1/{self.OBJECT}/{self.id}" + endpoint

    def request(self, method, url, **kwargs):
        return requests.request(method, url, headers=self.headers, **kwargs)

class NotionDatabase(NotionObject):
    OBJECT = "databases"

    def query(self, params):
        return self.request("post", self.url("/query"), params)

    def list(self, params):
        return self.request("get", self.url(), params)

    def create(self, params):
        return self.request("post", self.url(), params)

class NotionPage(NotionObject):
    OBJECT = "pages"

    def create(self, params):
        return self.request("post", self.url(), params)

    def update(self, params):
        return self.request("patch", self.url(), params)

class NotionBlock(NotionObject):
    OBJECT = "blocks"

    def get(self):
        return self.request("get", self.url("/children"))
    
    def append(self, params):
        return self.request("patch", self.url("/children"), params)

class NotionUser(NotionObject):
    OBJECT = "users"
    
    def list(self, params):
        return self.request("get", self.url(), params)