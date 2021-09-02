from flask import Flask, request

class Webhook:
    def __init__(self, config):
        self._config = config
        self._server = Flask(__name__)

    def run_for(self, bot):
        @self._server.route('/' + bot.token, methods=['POST'])
        def get_message():
            json_string = request.get_data().decode('utf-8')
            return bot.process_new_updates(json_string)

        @self._server.route("/")
        def webhook():
            return bot.set_webhook(self._config.get("url"))

        self._server.run(host="0.0.0.0", port=self._config.get("port"))