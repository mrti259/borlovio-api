from config import Config

class AmorcitoBot:
    def __init__(self, client, amorcito):
        self._amorcito = amorcito
        self._client = client
        self._amorcito.load_actions({
            "forbidden": self._forbidden,
            "start": self._start,
            "": self._default,
        })

    def _forbidden(self, *args):
        return "No estas autorizado"

    def _start(self, *args):
        return "Hola!"

    def _default(self, *args):
        return "No ocurrió nada"

    def on(self, command, message, xbot):
        user_id = message.chat.id
        txt = message.text
        xbot.send_message(user_id, self._amorcito.reply_for(user_id, command if command else txt)(message))
        xbot.send_message(user_id, self._amorcito.ask_for_input(user_id)())

config = Config()
tb = config.tb(AmorcitoBot(config.notion(), config.amorcito()))
