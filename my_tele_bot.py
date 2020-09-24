from telebot import TeleBot
from telebot import types
from data_base_handler import DataBaseHandler
from datetime import date
from data_base_handler import data_base_handler


class MyTeleBot(object):
    """
    class of my custom tele-bot
    :param token_path: str;  path to the file with token
    """

    def __init__(self, **kwargs):
        self.token_path = kwargs.get("token_path", None)
        self.bot = TeleBot(token=self.get_token())  # parent class init
        self.started = False  # True if bot is started
        self.data_base_handler = data_base_handler  # creating database handler
        self.country_name_to_short_name = {  # dictionary with countries short names
            "Russia": "ru",
            "United States": "us",
            "France": "fr",
            "United Kingdom": "gb",
            "Germany": "gr",
            "Canada": "ca",
        }
        self.topics = ["Business", "Entertainment",
                       "Health", "Science", "Sports",
                       "Technology"]  # topics to choose from

        self.countries = ["Russia", "United States", "France", "United Kingdom", "Germany", "Canada"]

        @self.bot.message_handler(commands=["start"])  # start command handler
        def start(message):
            start_message_text = """Hello, I'm a news bot.\nYou can get news on different topics every day)"""
            nickname = get_user_nickname(message)  # gets user's nickname
            telegram_id = get_user_telegram_id(message)  # gets user's telegram id

            is_registered = check_user_registration(telegram_id=telegram_id)
            print("registered: ", is_registered)
            choose_topics_text = "Choose topics you want to get news on:"
            welcome_back_message = "Welcome back! What do you want to do?"
            if is_registered:
                self.bot.send_message(message.chat.id, welcome_back_message)
            else:
                add_user_to_database(message)
                self.bot.send_message(message.chat.id, start_message_text)  # hello message
                select_country(message)

        @self.bot.message_handler(commands=["select_country"])
        def select_country(message):
            choose_country_message = "Select country you want to get news about:"

            markup = get_custom_keyboard(items=self.countries,
                                         one_time_keyboard=True,
                                         )  # markup for reply
            self.bot.send_message(message.chat.id, choose_country_message,
                                  reply_markup=markup)  # choose country text

        @self.bot.message_handler(commands=["select_time"])
        def select_part_of_day(message):
            """
            opens markup keyboard with part of the day options
            :param message: message from the user
            :return:
            """
            parts_of_day = ["Morning", "Afternoon", "Evening"]
            part_of_day_markup = get_custom_keyboard(items=parts_of_day,
                                                     one_time_keyboard=True)
            choose_part_of_day_message = "Choose part of the day:"
            self.bot.send_message(message.chat.id, choose_part_of_day_message,
                                  reply_markup=part_of_day_markup)

        @self.bot.message_handler(commands=["select_topics"])
        def select_topics(message):
            select_topic_message = "Select topics you want to get news on:"
            topics_markup = get_custom_keyboard(items=self.topics,
                                                one_time_keyboard=True)  # topics markup
            self.bot.send_message(message.chat.id, select_topic_message,
                                  reply_markup=topics_markup)

        @self.bot.message_handler(commands=["delete_topics"])
        def delete_topics(message):
            telegram_id = get_user_telegram_id(message)
            are_topics_added = self.data_base_handler.check_topics(telegram_id=telegram_id)
            if not are_topics_added:
                no_topics_message = "You have no topics. Add some)"
                topics_markup = get_custom_keyboard(items=self.topics,
                                                    one_time_keyboard=True)
                self.bot.send_message(message.chat.id, no_topics_message,
                                      reply_markup=topics_markup)

        @self.bot.message_handler(commands=["info"])
        def info(message):
            name = self.get_me()
            print(name)
            print(message.from_user)

        @self.bot.message_handler(content_types=["text"])
        def text_is_received(message):
            select_time(message)
            country_name_selected(message)
            time_selected(message)
            topic_selected(message)

        def country_name_selected(message):
            """
            handler for country selection
            :param message:
            """
            country_name_selected_message = \
                "OK, I will send you news about " + str(message.text)
            if str(message.text) in self.countries:
                self.bot.send_message(message.chat.id,
                                      country_name_selected_message)  # sends message to the user
                print("Country is selected")
                telegram_id = get_user_telegram_id(message)  # user's telegram id
                current_time = date.today()
                self.data_base_handler.add_country(telegram_id=telegram_id,
                                                   country_name=str(message.text),
                                                   current_time=current_time)

        def topic_selected(message):
            """
            handler for topic selection
            :param message:  message from the user
            """
            topic = str(message.text)
            telegram_id = get_user_telegram_id(message)  # user telegram id
            topic_selected_message = "Alright, " + topic + " is added to your topics"
            topic_is_used_message = "You already have " + topic + " in your topics"
            if topic in self.topics:
                # makes a request to the database and returns the result:
                res = self.data_base_handler.add_topic(telegram_id=telegram_id,
                                                       topic=topic)
                if res:
                    self.bot.send_message(message.chat.id, topic_selected_message)
                else:
                    self.bot.send_message(message.chat.id, topic_is_used_message)

        def select_time(message):
            """
            sends markup for time selection
            :param message: message from the user
            """
            morning_time_options = ["5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00"]  # options for morning
            afternoon_time_options = ["12:00", "13:00", "14:00", "15:00", "16:00"]  # options for afternoon
            evening_time_options = ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00"]  # options for evening
            select_time_message = "Select time you want to get news on"
            morning_markup = get_custom_keyboard(items=morning_time_options,
                                                 one_time_keyboard=True)  # markup for morning options
            afternoon_markup = get_custom_keyboard(items=afternoon_time_options,
                                                   one_time_keyboard=True)  # markup for afternoon options
            evening_markup = get_custom_keyboard(items=evening_time_options,
                                                 one_time_keyboard=True)  # markup for evening options
            if str(message.text) == "Morning":
                self.bot.send_message(message.chat.id, select_time_message,
                                      reply_markup=morning_markup)  # sends markup for morning
            if str(message.text) == "Afternoon":
                self.bot.send_message(message.chat.id, select_time_message,
                                      reply_markup=afternoon_markup)  # sends markup for afternoon
            if str(message.text) == "Evening":
                self.bot.send_message(message.chat.id, select_time_message,
                                      reply_markup=evening_markup)  # sends markup for evening

        def time_selected(message):
            text = str(message.text)
            hours = [str(i) for i in range(0, 24)]
            print(text.split(":"))
            if text.split(":")[0] in hours and text.split(":")[-1] == "00":
                selected_time = str(message.text)  # selected time
                telegram_id = get_user_telegram_id(message)  # user's telegram id
                current_time = date.today()  # current date
                self.data_base_handler.add_time(telegram_id=telegram_id,
                                                news_time=selected_time,
                                                current_time=current_time)
                time_selected_message = "OK, I will send you news at " + str(selected_time) + " every day)"
                self.bot.send_message(message.chat.id, time_selected_message)

        def get_user_nickname(message):
            """
            gets user's nickname in telegram
            :param message:
            :return: nickname: str
            """
            nickname = message.from_user.username  # gets nickname
            return nickname

        def get_user_telegram_id(message):
            """
            gets user's telegram id
            :param message:
            :return: telegram_id
            """
            telegram_id = message.from_user.id  # gets telegram id
            return telegram_id

        def get_custom_keyboard(items, **k):
            """
            makes custom keyboard with specified items
            :param items: list
            :return: ReplyKeyboardMarkup object
            """
            markup = types.ReplyKeyboardMarkup(**k)
            for item in items:
                markup.add(item)
            return markup

        def check_user_registration(telegram_id):
            """

            :param telegram_id: int;  Telegram id of the user
            :return: True if user was registered before
                     False if user wasn't registered
            """
            is_registered = self.data_base_handler.check_user(telegram_id=telegram_id)
            return is_registered

        def add_user_to_database(message):
            """
            Adds user data to the database
            :param message:
            """
            current_time = date.today()  # gets current date
            telegram_id = get_user_telegram_id(message)  # gets user's telegram id
            try:
                self.data_base_handler.add_user(
                    register_time=current_time,
                    telegram_id=telegram_id
                )
            except Exception as e:
                print("Add user crash")
                print(str(e))


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

    def polling(self, *args):
        self.bot.polling(*args)