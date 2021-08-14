from .amorcito import Amorcito

class AmorcitoBot:
    def __init__(self, connection, bot):
        self._amorcito = Amorcito(connection)
        self._bot = bot
        self._register_services()
        self._run()

    def _register_services(self):
        @self._bot.message_handler(commands=["start"])
        def start(message):
           self._bot.reply_to(message, "Hola!")

        @self._bot.message_handler(commands=["stop"])
        def stop(message):
           self._bot.reply_to(message, "Chau!")

        @self._bot.message_handler(commands=["help"])
        def help(message):
           self._bot.reply_to(message, "Sorry, no te puedo ayudar :(")

        @self._bot.message_handler()
        def default(message):
            pass

    def _run(self):
        self._bot.polling()