from config import Config
from notion import Notion

config = Config()
app = Notion(config.SECRET_KEY, config.NOTION_VERSION)