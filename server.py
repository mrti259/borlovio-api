from flask import Flask, request
from telebot import types

class Webhook:
    def __init__(self, url, port):
        self._config = {
            "url": url,
            "port": port
        }

    def start(self, bot):
        return Server(self._config, bot)

class Server:
    def __init__(self, config, bot):
        self._url = config.get("url")
        self._bot = bot
        self._server = Flask(__name__)
        self._register_services()
        self._server.run(host="0.0.0.0", port=config.get("port"))

    def _register_services(self):
        @self._server.route('/' + self._bot.token, methods=['POST'])
        def getMessage():
            json_string = request.get_data().decode('utf-8')
            update = types.Update.de_json(json_string)
            self._bot.process_new_updates([update])
            return "!", 200

        @self._server.route("/")
        def webhook():
            self._bot.remove_webhook()
            self._bot.set_webhook(url=self._url + self._bot.token)
            return "!", 200