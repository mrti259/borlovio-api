from .notionConnection import NotionConnection

class Notion:
    def __init__(self, secret_key, notion_version):
        if not secret_key:
            self.secret_key_should_be_supplied()
        if not notion_version:
            self.notion_version_should_be_supplied()

        self.connection = NotionConnection(secret_key, notion_version)

    def secret_key_should_be_supplied(self):
        raise Exception("Secret key should be supplied")

    def notion_version_should_be_supplied(self):
        raise Exception("Notion version should be supplied")

    def database(self, id):
        return self.connection.database(id)

    def page(self, id):
        return self.connection.page(id)

    def block(self, id):
        return self.connection.block(id)

    def user(self, id):
        return self.connection.user(id)