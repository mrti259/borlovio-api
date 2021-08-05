from .notionConnection import NotionConnection

class Notion:
    def __init__(self, secret_key, notion_version):
        self.connection = NotionConnection(secret_key, notion_version)

    def database(self, id):
        return self.connection.database(id)

    def page(self, id):
        return self.connection.page(id)

    def block(self, id):
        return self.connection.block(id)

    def user(self, id):
        return self.connection.user(id)