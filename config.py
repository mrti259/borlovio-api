import dotenv
import os
from notion import Notion

class Config:
    def database(self):
        notion = Notion(os.environ.get("NOTION_SECRET_KEY"), os.environ.get("NOTION_VERSION"))
        return notion.database(os.environ.get("NOTION_DATABASE_ID"))