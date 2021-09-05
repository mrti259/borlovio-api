from config import Config

config = Config()
tb = config.tb(config.bot(config.notion()), config.webhook())
