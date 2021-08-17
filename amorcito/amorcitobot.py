from .amorcito import Amorcito
from telebot import types

class AmorcitoBot:
    def __init__(self, connection, bot, webhook=None):
        self._amorcito = Amorcito(connection)
        self._bot = bot
        self._user_dict = {}
        self._register_services()
        self._run(webhook)

    def _run(self, webhook):
        print("Listening...")
        if webhook:
            webhook.start(self._bot)
        else:
            self._bot.polling()

    def _register_services(self):
        @self._bot.message_handler(func=lambda message: "Compras" in message.text)
        def compras(message):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            lists = self._amorcito.ver_listas()
            markup.add(*list(map(lambda x: types.KeyboardButton(x), lists)))
            self._send_message(message, "Qué lista te gustaria ver?", reply_markup=markup)
            self._bot.register_next_step_handler_by_chat_id(message.chat.id, self._compras_list)

        @self._bot.message_handler(func=lambda message: "Gastos" in message.text)
        def gastos(message):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(
                types.KeyboardButton("Ver"),
                types.KeyboardButton("Agregar"),
            )
            self._send_message(message, "Qué queres hacer con los gastos", reply_markup=markup)
            self._bot.register_next_step_handler_by_chat_id(message.chat.id, self._gastos_action)

        @self._bot.message_handler(commands=["start"])
        def start(message):
            self._send_message(message, "Hola!")
            self._default(message)

        @self._bot.message_handler()
        def default(message):
            self._default(message)

    def _send_message(self, message, text, **kwargs):
        self._bot.send_message(message.chat.id, text, **kwargs)

    def _default(self, message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(
            types.KeyboardButton("Compras"),
            types.KeyboardButton("Gastos"),
        )
        self._send_message(message, f"Qué querés ver?", reply_markup=markup)

    def _successed(self, message):
        self._send_message(message, "Listo!")
        self._default(message)

    def _failed(self, message):
        self._send_message(message, "No se pudo marcar el item")
        self._default(message)

    def _compras_list(self, message):
        self._user_dict[message.chat.id] = {
            "list": message.text
        }
        self._compras_ver(message)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(
            types.KeyboardButton("Agregar"),
            types.KeyboardButton("Marcar"),
        )
        self._send_message(message, "Qué querés hacer con la lista?", reply_markup=markup)
        self._bot.register_next_step_handler_by_chat_id(message.chat.id, self._compras_action)

    def _compras_action(self, message):
        if "Agregar" in message.text:
            self._send_message(message, "Qué te gustaría agregar?")
            self._bot.register_next_step_handler_by_chat_id(message.chat.id, self._compras_agregar)

        if "Marcar" in message.text:
            res = self._amorcito.ver_compras_pendientes(**self._user_dict[message.chat.id])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            items = list(map(lambda x: types.KeyboardButton(x), res))
            markup.add(*items)
            self._send_message(message, "Qué compra hiciste?", reply_markup=markup)
            self._bot.register_next_step_handler_by_chat_id(message.chat.id, self._compras_marcar)

    def _compras_ver(self, message):
        res = self._amorcito.ver_compras_pendientes(**self._user_dict[message.chat.id])
        msg = "Hay que comprar:\n- " + "\n- ".join(res)
        self._send_message(message, msg)

    def _compras_agregar(self, message):
        self._user_dict[message.chat.id]["name"] = message.text
        self._amorcito.agregar_compra(**self._user_dict[message.chat.id])
        self._successed(message)

    def _compras_marcar(self, message):
        res = self._amorcito.ver_compras_pendientes(**self._user_dict[message.chat.id])
        item = message.text
        if item in res:
            self._amorcito.marcar_compra(res.get(item))
            self._successed(message)
        else:
            self._failed(message)

    def _gastos_action(self, message):
        if "Ver" in message.text:
            gastos = list(map(lambda x: "{name} - {amount} ({paid}) - {date}".format(**x), self._amorcito.ver_gastos()))
            self._send_message(message, "\n".join(gastos))

        if "Agregar" in message.text:
            self._send_message(message, "Qué gasto te gustaría agregar?")
            self._bot.register_next_step_handler_by_chat_id(message.chat.id, self._gastos_agregar_name)

    def _gastos_agregar_name(self, message):
        self._user_dict[message.chat.id] = {
            "name": message.text
        }
        self._send_message(message, "De cuánto fue?")
        self._bot.register_next_step_handler_by_chat_id(message.chat.id, self._gastos_agregar_amount)

    def _gastos_agregar_amount(self, message):
        self._user_dict[message.chat.id]["amount"] = int(message.text)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        users = self._amorcito.ver_personas()
        markup.add(*list(map(lambda x: types.KeyboardButton(x), users)))
        self._send_message(message, "Quién pago?", reply_markup=markup)
        self._bot.register_next_step_handler_by_chat_id(message.chat.id, self._gastos_agregar_paid)

    def _gastos_agregar_paid(self, message):
        self._user_dict[message.chat.id]["paid"] = message.text
        res = self._amorcito.agregar_gasto(**self._user_dict[message.chat.id])
        self._successed(message)