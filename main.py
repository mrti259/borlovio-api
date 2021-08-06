from config import Config
from notion import Notion
from borlovio import Bor

config = Config()

notion = Notion(config.SECRET_KEY, config.NOTION_VERSION)
bor = Bor(notion.database(config.DATABASE_ID))

while __name__ == "__main__":
    print("Qué te gustaría saber si vi?")
    x = input(":")

    if x == "":
        print("Bye!")
        break

    status = bor.status(x)

    if status == "Completed":
        print("Si, vi", x, ":D")
    elif status == "In progress":
        print("Estoy viendo", x, ":)")
    elif status == "Not started":
        print("No vi", x, ", pero la tengo pendiente :)")
    else:
        print("No, no vi", x, ":(")

    print("")