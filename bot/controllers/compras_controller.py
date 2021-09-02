from . import Controller

class ComprasController(Controller):
    def index(self, user_id, message, xbot):
        self.elegir_lista(user_id, message, xbot)

    def compras(self, user_id, message, xbot):
        options = {
            "Agregar": self.agregar,
            "Archivar": self.archivar,
        }

        def nxt(msg):
            text = msg.text
            if text in options:
                options[text](user_id, message, xbot)
            else:
                self.fallo(user_id, message, xbot)

        xbot.send_message_with_options_and_next_step_handler(user_id, "Qué querés hacer?", options, nxt)

    def elegir_lista(self, user_id, message, xbot):
        options = ["Super", "Super Grande", "Verduleria", "Farmacia"]

        def nxt(msg):
            text = msg.text
            if text in options:
                self._user_dict[user_id] = {"lista": text}
                self.compras(user_id, message, xbot)
            else:
                self.fallo(user_id, message, xbot)

        xbot.send_message_with_options_and_next_step_handler(user_id, "Qué lista querés ver?", options, nxt)

    def ver(self, user_id, message, xbot):
        xbot.send_message(user_id, "Aca va a lista")

    def agregar(self, user_id, message, xbot):
        def nxt(msg):
            self._user_dict[user_id]["nombre"] = msg.text
            self.exito(user_id, msg, xbot)

        xbot.send_message_with_next_step_handler(user_id, "Qué querés agregar?", nxt)

    def archivar(self, user_id, message, xbot):
        options = []

        def nxt(msg):
            text = msg.text
            if text in options:
                self.exito(user_id, msg, xbot)
            else:
                self.fallo(user_id, message, xbot)

        xbot.send_message_with_options_and_next_step_handler(user_id, "Qué querés eliminar?", options, nxt)