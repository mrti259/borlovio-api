from notion_client import Client

from .user_schema import UserSchema
from .gasto_schema import GastoSchema
from .compra_schema import CompraSchema

class Schemas:
    def __init__(self, client):
        res = client.databases.list()

        if res["object"] == "error":
            raise Exception(res["message"])

        dbs = {}

        for r in res["results"]:
            title: str = r["title"][0]["plain_text"]
            database_id: str = r["id"]
            dbs[title] = database_id

        self.users = UserSchema(client, dbs["Users"])
        self.gastos = GastoSchema(client, dbs["Gastos compartidos"])
        self.compras = CompraSchema(client, dbs["Compras"])