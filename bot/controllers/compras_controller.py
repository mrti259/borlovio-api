from . import Controller

class ComprasController(Controller):
    def index(self, user_id, message, xbot):
        self.elegir_categoria(user_id, message, xbot)

    def compras(self, user_id, message, xbot):
        options = {
            "Agregar": self.agregar,
            "Marcar como hecho": self.archivar,
        }

        def nxt(msg):
            text = msg.text
            if text in options:
                options[text](user_id, msg, xbot)
            else:
                self.fallo(user_id, msg, xbot)
                self._bot.default(user_id, msg, xbot)

        self.ver(user_id, message, xbot)
        xbot.send_message_with_options_and_next_step_handler(user_id, "Qué querés hacer?", options, nxt)

    def elegir_categoria(self, user_id, message, xbot):
        options = self._traer_categorias()

        def nxt(msg):
            text = msg.text
            if text in options:
                self._user_dict[user_id] = self._bot.schemas.compras.page(category=msg.text)
                self.compras(user_id, message, xbot)
            else:
                self.fallo(user_id, message, xbot)
                self._bot.default(user_id, msg, xbot)

        xbot.send_message_with_options_and_next_step_handler(user_id, "Qué categoría querés ver?", options, nxt)

    def ver(self, user_id, message, xbot):
        compras_str = "\n·".join([compra.name for compra in self._traer_listas(user_id)])
        xbot.send_message(user_id, "Hay que comprar:\n·" + compras_str if compras_str else "No hay nada para comprar!")

    def agregar(self, user_id, message, xbot):
        def nxt(msg):
            names:list[str] = msg.text.split(",")

            for name in names:
                self._user_dict[user_id].name = name.strip().capitalize()
                e = self._bot.schemas.compras.create(self._user_dict[user_id])

            if not e:
                self.exito(user_id, msg, xbot)
            else:
                self.fallo(user_id, msg, xbot)

            self.compras(user_id, msg, xbot)

        xbot.send_message_with_next_step_handler(user_id, "Qué querés agregar? Separá los items por coma para agregar más de uno", nxt)

    def archivar(self, user_id, message, xbot):
        lista = self._traer_listas(user_id)
        options = {compra.name: compra for compra in lista}

        def nxt(msg):
            text = msg.text
            if text in options:
                compra = options[text]
                compra.done = True
                self._bot.schemas.compras.update(compra)
                self.exito(user_id, msg, xbot)
            else:
                self.fallo(user_id, message, xbot)

            self.index(user_id, msg, xbot)

        if options:
            xbot.send_message_with_options_and_next_step_handler(user_id, "Qué querés marcar?", options, nxt)
        else:
            self.fallo(user_id, message, xbot)
            self.index(user_id, message, xbot)

    def _traer_categorias(self):
        categorias = []
        for x in self._bot.schemas.compras.retrieve()["properties"]["Category"]["select"]["options"]:
            categorias.append(x["name"])
        return categorias

    def _traer_listas(self, user_id):
        lista = []

        for compra in self._bot.schemas.compras.query(filter={
            "and": [
                {
                    "property": "Category",
                    "select": {
                        "equals": self._user_dict[user_id].category
                    }
                },
                {
                    "property": "Done",
                    "checkbox": {
                        "equals": False
                    }
                }
            ]
        }):
            lista.append(compra)

        return lista