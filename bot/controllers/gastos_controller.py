from . import Controller

class GastosController(Controller):
    def index(self, user_id, message, xbot):
        options = {
            "Agregar": self.agregar,
            "Ver": self.ver
        }

        def nxt(msg):
            text = msg.text
            if text in options:
                self._user_dict[user_id] = {}
                options[text](user_id, message, xbot)
            else:
                self.fallo(user_id, message, xbot)

        xbot.send_message_with_options_and_next_step_handler(user_id, "Qué querés hacer?", options, nxt)

    def ver(self, user_id, message, xbot):
        xbot.send_message(user_id, "Aca va a lista")

    def agregar(self, user_id, message, xbot):
        self.agregar_nombre(user_id, message, xbot)

    def agregar_nombre(self, user_id, message, xbot):
        def nxt(msg):
            self._user_dict[user_id]["nombre"] = msg.text
            self.agregar_valor(user_id, message, xbot)

        xbot.send_message_with_next_step_handler(user_id, "Qué querés agregar?", nxt)

    def agregar_valor(self, user_id, message, xbot):
        def nxt(msg):
            self._user_dict[user_id]["valor"] = msg.text
            self.agregar_pago(user_id, message, xbot)

        xbot.send_message_with_next_step_handler(user_id, "Cuánto costó?", nxt)

    def agregar_pago(self, user_id, message, xbot):
        options = ["Bor", "Lumo"]

        def nxt(msg):
            self._user_dict[user_id]["pago"] = msg.text
            self.exito(user_id, message, xbot)

        xbot.send_message_with_options_and_next_step_handler(user_id, "Quién pago?", options, nxt)