from config import Config
from bor import BorLoVio
import sys

config = Config()
borlovio = BorLoVio(config.database())


if __name__ == "__main__":
    print(borlovio.start())

    while True:
        print(borlovio.ask_for_input())
        x = input(":")

        if x == "":
            print(borlovio.stop())
            break

        print(borlovio.answer_for(x))
        print("")