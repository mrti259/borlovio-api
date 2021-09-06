from dotenv import load_dotenv
load_dotenv()

import os
import notion_client
import bot
import xbot

class Config:
    def notion(self):
        return notion_client.Client(auth=os.environ.get("NOTION_SECRET_KEY"))

    def webhook(self):
        if "URL" in os.environ:
            return xbot.Webhook({
                "url": os.environ.get("URL"),
                "port": int(os.environ.get("PORT", 5000))
            })

    def bot(self, connection):
        return bot.AmorcitoBot(connection)

    def tb(self, bot, webhook=None):
        return xbot.TelegramBot(bot, os.environ.get("TELEGRAM_BOT_TOKEN"), webhook)
