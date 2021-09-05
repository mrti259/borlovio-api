from .schema import Model,Schema

class Gasto(Model):
    def __init__(self, name="", amount=0, paid=""):
        super().__init__()
        self.name = name
        self.amount = amount
        self.paid = paid

    @property
    def name(self):
        return self.properties["Name"]["title"][0]["text"]["content"]

    @name.setter
    def name(self, _name):
        self.properties.update({"Name": {"title": [{"text": {"content": _name }}]}})

    @property
    def amount(self):
        return self.properties["Amount"]["number"]

    @amount.setter
    def amount(self, _amount):
        self.properties.update({"Amount": {"number": int(_amount)}})

    @property
    def paid(self):
        return self.properties["Paid"]["select"]["name"]

    @paid.setter
    def paid(self, _paid):
        self.properties.update({"Paid": {"select": {"name": _paid}}})

    @property
    def date(self):
        return self.properties["Date"]["created_at"]

    def __str__(self):
        return f"{self.name}: $ {self.amount} - ({self.paid}) - ({self.date})"

class GastoSchema(Schema):
    def __init__(self, client, database_id):
        super().__init__(client, database_id, Gasto)