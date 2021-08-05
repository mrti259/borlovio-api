from .notionObject import *

class NotionConnection:
    def __init__(self, secret_key, notion_version):
        self.config = {
            "authorization": secret_key,
            "notion-version": notion_version
        }

    def database(self, id):
        return NotionDatabase(self.config, id)

    def page(self, id):
        return NotionPage(self.config, id)

    def block(self, id):
        return NotionBlock(self.config, id)

    def user(self, id):
        return NotionUser(self.config, id)