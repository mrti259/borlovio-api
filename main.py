from config import Config
from notion import Notion
from bor import BorLoVio

config = Config()

notion = Notion(config.SECRET_KEY, config.NOTION_VERSION)
borlovio = BorLoVio(notion.database(config.DATABASE_ID))

if __name__ == "__main__":
    print("Hola!")

while __name__ == "__main__":
    print("\nQué te gustaría saber si vi?")
    x = input(":")

    if x == "":
        print("\nBye!")
        break

    print(borlovio.answer_for(x))