from datetime import datetime

from . import Controller

class GastosController(Controller):
    def index(self, user_id, message, xbot):
        self.gastos(user_id, message, xbot)

    def gastos(self, user_id, message, xbot):
        options = {
            "Agregar": self.agregar,
            "Ver": self.ver
        }

        def nxt(msg):
            text = msg.text
            if text in options:
                self._user_dict[user_id] = self._bot.schemas.gastos.page()
                options[text](user_id, message, xbot)
            else:
                self.fallo(user_id, message, xbot)
                self._bot.default(user_id, msg, xbot)

        xbot.send_message_with_options_and_next_step_handler(user_id, "Qué querés hacer?", options, nxt)

    def ver(self, user_id, message, xbot):
        gastos_str = "\n·".join(map(lambda x: str(x), self._traer_gastos()))
        xbot.send_message(user_id, "Los gastos del mes son:\n·" + gastos_str)
        self.index(user_id, message, xbot)

    def agregar(self, user_id, message, xbot):
        self.agregar_nombre(user_id, message, xbot)

    def agregar_nombre(self, user_id, message, xbot):
        def nxt(msg):
            text = msg.text
            if text:
                self._user_dict[user_id].name = text
                self.agregar_valor(user_id, message, xbot)
            else:
                self.fallo(user_id, message, xbot)
                self.index(user_id, msg, xbot)

        xbot.send_message_with_next_step_handler(user_id, "En qué gastaron?", nxt)

    def agregar_valor(self, user_id, message, xbot):
        def nxt(msg):
            text = msg.text
            if text.isnumeric:
                self._user_dict[user_id].amount = msg.text
                self.agregar_pago(user_id, message, xbot)
            else:
                self.fallo(user_id, message, xbot)
                self.index(user_id, msg, xbot)

        xbot.send_message_with_next_step_handler(user_id, "Cuánto costó?", nxt)

    def agregar_pago(self, user_id, message, xbot):
        options = self._traer_gastos_paid()

        def nxt(msg):
            e = -1
            text = msg.text

            if text in options:
                self._user_dict[user_id].paid = msg.text
                e = self._crear_gasto(user_id)

            if not e:
                self.exito(user_id, message, xbot)
            else:
                self.fallo(user_id, message, xbot)

            self.index(user_id, msg, xbot)

        xbot.send_message_with_options_and_next_step_handler(user_id, "Quién pago?", options, nxt)

    def _crear_gasto(self, user_id):
        return self._bot.schemas.gastos.create(self._user_dict[user_id])

    def _traer_gastos(self):
        inicio_mes = datetime.today().strftime("%Y-%m-01")
        return self._bot.schemas.gastos.query(filter={"property": "Date", "date": {"on_or_after": inicio_mes}})

    def _traer_gastos_paid(self):
        paid = []

        for x in self._bot.schemas.gastos.retrieve()["properties"]["Paid"]["select"]["options"]:
            paid.append(x["name"])

        return paid