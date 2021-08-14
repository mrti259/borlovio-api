from config import Config
from amorcito import Amorcito
import json

config = Config()
amorcito = Amorcito(config.connection())