from .amorcitoObject import *
import dateutil.parser as dparser
from datetime import datetime

class Amorcito:
    def __init__(self, connection):
        self._compras = AmorcitoCompras(connection)
        self._gastos = AmorcitoGastos(connection)
        self._usuarios = AmorcitoUsuarios(connection)

    def agregar_compra(self, name, list):
        return self._compras.create({
            "name": name,
            "list": list
        })

    def marcar_compra(self, page_id):
        return self._compras.update(page_id, {
            "done": True
        })

    def ver_listas(self):
        return self._compras.lists()

    def ver_compras_pendientes(self, list):
        res = self._compras.query({
            "filter": {
                "and": [
                    {
                        "property": "Done",
                        "checkbox": {
                            "equals": False
                        }
                    },
                    {
                        "property": "List",
                        "select": {
                            "equals": list
                        }
                    }
                ]
            }
        })

        compras = {}

        for r in res.json()["results"]:
            compras[r["properties"]["Name"]["title"][0]["text"]["content"]] = r["id"]

        return compras

    def agregar_gasto(self, name, amount, paid):
        return self._gastos.create({
            "name": name,
            "amount": amount,
            "paid": paid
        })

    def ver_gastos(self):
        res = self._gastos.query({})

        gastos = []

        for r in res.json()["results"]:
            gasto = {
                "name": r["properties"]["Name"]["title"][0]["text"]["content"],
                "amount": r["properties"]["Amount"]["number"],
                "paid": r["properties"]["Paid"]["select"]["name"],
                "date": dparser.parse(r["properties"]["Date"]["created_time"]).strftime("%d/%m/%Y")
            }
            gastos.append(gasto)

        return gastos

    def ver_personas(self):
        return self._gastos.people()

    def agregar_usuario(self, name, cid):
        return self._usuarios.create({
            "name": name,
            "chat_id": cid
        })

    def buscar_usuario(self, chat_id):
        res = self._usuarios.query({
            "filter": {
                "property": "chat_id",
                "text": {
                    "equals": chat_id
                }
            }
        }).json()
        return res["results"]