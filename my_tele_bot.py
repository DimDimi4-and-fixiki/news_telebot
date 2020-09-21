from telebot import TeleBot, types


class MyTeleBot(TeleBot):
    """
    class of my custom tele-bot
    :param token_path: str;  path to the file with token
    """

    def __init__(self, **kwargs):
        self.token_path = kwargs.get("token_path", None)
        self.bot = super(MyTeleBot, self).__init__(token=self.get_token())  # parent class init
        self.started = False  # True if bot is started
        print(self.get_token())

        @self.message_handler(commands=["start"])  # start command handler
        def start(message):
            start_message_text = """Hello, I'm a news bot.\nYou can get news on different topics every day)"""

            choose_topics_text = "Choose topics you want to get news on:"
            self.send_message(message.chat.id, start_message_text)  # hello message
            self.send_message(message.chat.id, choose_topics_text)  # choose topic message
            markup = types.ReplyKeyboardMarkup()
            topics = [""]
            markup.row()

        @self.message_handler(commands=["choose_country"])
        def choose_country(message):
            choose_country_message = "Select country you want to get news about:"
            countries = ["Russia", "United States", "France", "United Kingdom", "Germany", "Canada"]
            markup = get_custom_keyboard(items=countries)  # markup for reply
            self.send_message(message.chat.id, choose_country_message,
                              reply_markup=markup)  # choose country text
            country_name_to_short_name = {  # dictionary with countries short names
                "Russia": "ru",
                "United States": "us",
                "France": "fr",
                "United Kingdom": "gb",
                "Germany": "gr",
                "Canada": "ca",
            }

        def get_custom_keyboard(items):
            """
            makes custom keyboard with specified items
            :param items: list
            :return: ReplyKeyboardMarkup object
            """
            markup = types.ReplyKeyboardMarkup()
            markup.row_width = 3
            for item in items:
                markup.add(item)
            return markup

    def get_token(self):
        """
        gets token from different types of files
        :return: token: str
        """
        token_path_file_name = self.token_path.split("/")[-1]  # name of file with token
        token_path_extension = token_path_file_name.split(".")[-1]  # extension of token file
        if token_path_extension == "txt":  # text file
            return self.get_token_from_txt()

    def get_token_from_txt(self):
        """
        gets token from txt file
        :return: token: str
        """
        f = open(self.token_path, "r")
        return f.read()