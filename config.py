import os

class Config:
    SECRET_KEY = os.environ["notion_secret_key"]
    DATABASE_ID = os.environ["notion_database_id"]
    NOTION_VERSION = os.environ["notion_version"]