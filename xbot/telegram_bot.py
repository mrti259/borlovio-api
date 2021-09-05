import telebot

from .xbot import XBot
from .webhook import Webhook

class TelegramBot(XBot):
    def __init__(self, bot, token, webhook_config=None):
        self._telebot = telebot.TeleBot(token)
        self._register_services(bot)
        self._run(webhook_config)

    def _register_services(self, bot):
        @self._telebot.message_handler(commands=["start"])
        def start(message):
            bot.on("start", message, self)

        @self._telebot.message_handler(commands=["help"])
        def help(message):
            bot.on("help", message, self)

        @self._telebot.message_handler(commands=["stop"])
        def stop(message):
            bot.on("stop", message, self)

        @self._telebot.message_handler()
        def default(message):
            bot.on("", message, self)

    def _run(self, webhook):
        if not webhook:
            self._telebot.polling()
        else:
            Webhook(webhook)

    def set_webhook(self, url):
        self._telebot.remove_webhook()
        self._telebot.set_webhook(url=url + self._telebot.token)
        return "!", 200

    def process_new_updates(self, json_string):
        update = telebot.types.Update.de_json(json_string)
        self._telebot.process_new_updates([update])
        return "!", 200

    def send_message(self, chat_id, text, **kwargs):
        self._telebot.send_message(chat_id, text, **kwargs)

    def send_message_with_next_step_handler(self, chat_id, text, next_step_handler, **kwargs):
        self._telebot.send_message(chat_id, text, **kwargs)
        self._telebot.register_next_step_handler_by_chat_id(chat_id, next_step_handler)

    def send_message_with_options_and_next_step_handler(self, chat_id, text, options, next_step_handler):
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(*list(map(lambda x: telebot.types.KeyboardButton(x), options)))
        self.send_message_with_next_step_handler(chat_id, text, next_step_handler, reply_markup=markup)