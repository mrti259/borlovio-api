import telebot
from .webhook import Webhook

class TelegramBot:
    def __init__(self, token, webhook=None):
        self._bot = telebot.TeleBot(token)

    def run(self, webhook):
        if not webhook:
            self._bot.polling()
        else:
            webhook.run_for(self)

    def set_webhook(self, url):
        self._bot.remove_webhook()
        self._bot.set_webhook(url=url + self._bot.token)
        return "!", 200

    def process_new_updates(self, json_string):
        update = telebot.types.Update.de_json(json_string)
        self._bot.process_new_updates([update])
        return "!", 200

    def send_message(self, chat_id, text, **kwargs):
        self._bot.send_message(chat_id, text, **kwargs)

    def send_message_with_next_step_handler(self, chat_id, text, next_step_handler, **kwargs):
        self._bot.send_message(chat_id, text, **kwargs)
        self._bot.register_next_step_handler_by_chat_id(chat_id, next_step_handler)

    def send_message_with_options_and_next_step_handler(self, chat_id, text, options, next_step_handler):
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.add(*list(map(lambda x: telebot.types.KeyboardButton(x), options)))
        self.send_message_with_next_step_handler(chat_id, text, next_step_handler, reply_markup=markup)