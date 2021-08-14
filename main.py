from config import Config
from amorcito import AmorcitoBot

config = Config()
bot = AmorcitoBot(config.connection(), config.bot())