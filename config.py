from notion import NotionConnection
import os
import dotenv
import telebot

dotenv.load_dotenv()

class Config:
    def connection(self):
        return NotionConnection(os.environ.get("NOTION_SECRET_KEY"), "2021-07-27")

    def bot(self):
        return telebot.TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN"))