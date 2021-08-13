from .notionObject import *

class NotionConnection:
    def __init__(self, secret_key, notion_version):
        self._headers = {
            "authorization": secret_key,
            "notion-version": notion_version
        }

    def database(self, id=""):
        return NotionDatabase(self._headers, id)

    def page(self, id=""):
        return NotionPage(self._headers, id)

    def block(self, id=""):
        return NotionBlock(self._headers, id)

    def user(self, id=""):
        return NotionUser(self._headers, id)

    def search(self, body):
        return NotionSearch(self._headers).search(body)