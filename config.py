from dotenv import load_dotenv
load_dotenv()

import os
import notion_client
import telegrambot
import amorcito

class Config:
    def notion(self):
        return notion_client.Client(auth=os.environ.get("NOTION_SECRET_KEY"))

    def webhook(self):
        if "URL" in os.environ:
            return {
                "url": os.environ.get("URL"),
                "port": int(os.environ.get("PORT"), 5000)
            }

    def tb(self, bot, webhook=None):
        return telegrambot.TelegramBot(bot, os.environ.get("TELEGRAM_BOT_TOKEN"), webhook)

    def amorcito(self):
        return amorcito.Amorcito()