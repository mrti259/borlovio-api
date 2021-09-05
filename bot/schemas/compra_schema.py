from .schema import Model, Schema

class Compra(Model):
    def __init__(self, name="", category=""):
        super().__init__()
        self.name = name
        self.category = category

    @property
    def name(self):
        return self.properties["Name"]["title"][0]["text"]["content"]

    @name.setter
    def name(self, _name):
        self.properties.update({"Name": {"title": [{"text": {"content": _name}}]}})

    @property
    def category(self):
        return self.properties["Category"]["select"]["name"]

    @category.setter
    def category(self, _category):
        self.properties.update({"Category": {"select": {"name": _category}}})

    @property
    def done(self):
        return self.properties["Done"]["checkbox"]

    @done.setter
    def done(self, _done):
        self.properties.update({"Done": {"checkbox": _done}})

class CompraSchema(Schema):
    def __init__(self, client, database_id):
        super().__init__(client, database_id, Compra)