from notion import NotionConnection
from server import Webhook
import os
import dotenv
import telebot

dotenv.load_dotenv()

class Config:
    def connection(self):
        return NotionConnection(os.environ.get("NOTION_SECRET_KEY"), os.environ.get("NOTION_VERSION")

    def bot(self):
        return telebot.TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN"))

    def webhook(self):
        if "URL" in os.environ:
            return Webhook(os.environ.get("URL"), os.environ.get("PORT"))
