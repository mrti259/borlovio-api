from abc import ABC, abstractmethod
import os

class AmorcitoObject(ABC):
    def __init__(self, connection):
        self._connection = connection

    @property
    @abstractmethod
    def _origin(self):
        pass

    @abstractmethod
    def _map_props(self, properties):
        pass

    def query(self, body):
        return self._connection.database(self._origin).query(body)

    def create(self, properties):
        return self._connection.page().create({
            "parent": {
                "database_id": self._origin
            },
            "properties": self._map_props(properties)
        })

    def update(self, page_id, properties):
        return self._connection.page(page_id).update({
            "parent": {
                "database_id": self._origin
            },
            "properties": self._map_props(properties)
        })

class AmorcitoCompras(AmorcitoObject):
    @property
    def _origin(self):
        return os.environ.get("COMPRAS_ID")

    def _map_props(self, properties):
        props = {}

        if "name" in properties:
            props["Name"] = {
                "title": [
                    {
                        "type": "text",
                        "text" : {
                            "content": properties["name"]
                        }
                    }
                ]
            }

        if "list" in properties:
            props["List"] = {
                "select": {
                    "name": properties["list"]
                }
            }

        if "done" in properties:
            props["Done"] = {
                "checkbox": properties["done"]
            }

        return props

    def lists(self):
        res = self._connection.database(self._origin).retrieve()
        options = []
        for r in res.json()["properties"]["List"]["select"]["options"]:
            options.append(r["name"])
        return options

class AmorcitoGastos(AmorcitoObject):
    @property
    def _origin(self):
        return os.environ.get("GASTOS_ID")

    def _map_props(self, properties):
        props = {}

        if "name" in properties:
            props["Name"] = {
                "title": [
                    {
                        "type": "text",
                        "text" : {
                            "content": properties["name"]
                        }
                    }
                ]
            }

        if "amount" in properties:
            props["Amount"] = {
                "number": properties["amount"]
            }

        if "paid" in properties:
            props["Paid"] = {
                "select": {
                    "name": properties["paid"]
                }
            }

        return props

    def people(self):
        res = self._connection.database(self._origin).retrieve()
        options = []
        for r in res.json()["properties"]["Paid"]["select"]["options"]:
            options.append(r["name"])
        return options

class AmorcitoUsuarios(AmorcitoObject):
    @property
    def _origin(self):
        return os.environ.get("USUARIOS_ID")

    def _map_props(self, properties):
        props = {}

        if "name" in properties:
            props["Name"] = {
                "title": [
                    {
                        "type": "text",
                        "text" : {
                            "content": properties["name"]
                        }
                    }
                ]
            }

        if "chat_id" in properties:
            props["chat_id"] = {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": properties["chat_id"]
                        }
                    }
                ]
            }

        return props
