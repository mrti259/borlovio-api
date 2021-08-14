from notion import NotionConnection
import os
import dotenv

dotenv.load_dotenv()

class Config:
    def connection(self):
        return NotionConnection(os.environ.get("NOTION_SECRET_KEY"), "2021-07-27")