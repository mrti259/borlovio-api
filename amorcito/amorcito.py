class Amorcito:
    def __init__(self, connection):
        self._connection = connection
        self._databases_id = []
        self._connect()

    def _connect(self):
        res = self._connection.search({
            "filter": {
                "property": "object",
                "value": "database"
            }
        })

        self._databases_id = {}

        for r in res.json()["results"]:
            self._databases_id[r["title"][0]["text"]["content"]] = r["id"]

    def _users(self):
        return self._connection.user().list()

    def _database_id(self, name):
        return self._databases_id.get(name)

    def agregar_compra(self, name, list):
        return self._connection.page().create({
            "parent": {
                "database_id": self._database_id("Compras")
            },
            "properties": {
                "List": {
                    "select": {
                        "name": list
                    }
                },
                "Done": {
                    "checkbox": False
                },
                "Name": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": name
                            }
                        }
                    ]
                }
            }
        })

    def marcarCompra(self, name):
        res = self._connection.database(self._database_id("Compras")).query({
            "filter": {
                "and": [
                    {
                        "property": "Done",
                        "checkbox": {
                            "equals": False
                        }
                    },
                    {
                        "property": "Name",
                        "title": {
                            "equals": name
                        }
                    }
                ]
            }
        })

        _ids = [r["id"] for r in res.json()["results"]]

        return self._connection.page(_ids[0]).update({
            "properties": {
                "Done": {
                    "checkbox": True
                }
            }
        })

    def verComprasPendientes(self, lista):
        res = self._connection.database(self._database_id("Compras")).query({
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
                            "equals": lista
                        }
                    }
                ]
            }
        })

        compras = []

        for r in res.json()["results"]:
            compras.append(r["properties"]["Name"]["title"][0]["text"]["content"])

        return compras

    def agregarGasto(self, name, amount, paid):
        return self._connection.page().create({
            "parent": {
                "database_id": self._database_id("Gastos compartidos")
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": name
                            }
                        }
                    ]
                },
                "Amount": {
                    "number": amount
                },
                #"Paid": {"people": []}
            }
        })

    def ver_gastos(self):
        res = self._connection.database(self._database_id("Gastos compartidos")).query({})

        gastos = []

        for r in res.json()["results"]:
            gastos.append(r["properties"]["Name"]["title"][0]["text"]["content"])

        return gastos
