from telebot import TeleBot
from telebot import types
from data_base_handler import DataBaseHandler
from datetime import date
from data_base_handler import data_base_handler
from news_api_handler import NewsApiHandler
from languages import LanguageHandler
import time
import schedule


"""
TODO:
create method something like

Add dictionary to the separate file: 
eng_to_rus = 
    {
        "Choose topic": "Выберите темы для новостей"
        ...
    }  # dict for translation with all the messages
    
def my_send_message(message, **kwargs):
    language = kwargs.get("language", None)  # language of the message
    message_to_send = kwargs.get("message_to_send", None)  # message to send: str
    translated_message_to_send = message_to_send
    if str(language) == "rus" and message_to_send in eng_to_rus.keys():
        translated_message_to_send = eng_to_rus[message_to_send]
    self.bot.send_message(message.chat.id, translated_message_to_send)
        
"""


class MyTeleBot(object):
    """
    class of my custom tele-bot
    :param token_path: str;  path to the file with token
    """

    def __init__(self, **kwargs):
        self.token_path = kwargs.get("token_path", None)
        self.MAX_NUM_OF_ARTICLES = 6  # maximum number of articles on each topic
        self.bot = TeleBot(token=self.get_token())  # parent class init
        self.started = False  # True if bot is started
        self.data_base_handler = DataBaseHandler(path="news_bot_db")  # creating database handler
        self.news_api_handler = NewsApiHandler(path="secure_codes/newsapi.txt")
        self.language_handler = LanguageHandler()
        self.markup_hider = types.ReplyKeyboardRemove()
        self.country_name_to_short_name = {  # dictionary with countries short names
            "Russia": "ru",
            "United States": "us",
            "France": "fr",
            "United Kingdom": "gb",
            "Germany": "gr",
            "Canada": "ca",
        }
        self.basic_markup_buttons = ["Add topics", "Change news time",
                                     "Select country", "Delete topics",
                                     "Change number of articles", "Change language"
                                     ]  # buttons on a basic keyboard
        self.russian_basic_markup_buttons = ["Добавить темы", "Поменять время отправки новостей",
                                             "Выбрать страну", "Удалить темы", "Изменить число статей",
                                             "Поменять язык", ]
        self.basic_markup = None
        self.topics = ["Business", "Entertainment",
                       "Health", "Science", "Sports",
                       "Technology"]  # topics to choose from
        self.topics_rus = ["Бизнес", "Развлечения",
                           "Здоровье", "Наука",
                           "Спорт", "Технологии"]
        self.delete_topics = ["-Business", "-Entertainment",
                              "-Health", "-Science", "-Sports",
                              "-Technology"]
        self.delete_topics_rus = ["-Бизнес", "-Развлечения",
                                  "-Здоровье", "-Наука",
                                  "-Спорт", "-Технологии"]
        #  topics items with OK button:
        self.topics_ok = self.topics
        self.topics_ok.append("OK")
        self.topics_ok_rus = self.topics_rus
        self.topics_ok_rus.append("OK")

        self.languages = ["English", "Russian"]  # list of languages of the bot

        self.countries = ["Russia", "United States", "France",
                          "United Kingdom", "Germany", "Canada"]
        self.countries_rus = ["Россия", "США", "Франция",
                              "Объединенное королевство", "Германия", "Канада"]




        @self.bot.message_handler(commands=["start"])  # start command handler
        def start(message):
            self.basic_markup = get_custom_keyboard(items=self.basic_markup_buttons)
            start_message_text = """Hello, I'm a news bot.\nYou can get news on different topics every day)"""
            nickname = get_user_nickname(message)  # gets user's nickname
            telegram_id = get_user_telegram_id(message)  # gets user's telegram id
            data_base_handler.add_chat_id(telegram_id=telegram_id,
                                               chat_id=message.chat.id)

            is_registered = data_base_handler.check_user(telegram_id=telegram_id)
            print("registered: ", is_registered)
            choose_topics_text = "Choose topics you want to get news on:"
            welcome_back_message = "Welcome back! What do you want to do?"
            if is_registered:
                language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
                show_basic_keyboard(message, welcome_back_message, language=language)
            else:
                add_user_to_database(message)
                self.bot.send_message(message.chat.id, start_message_text)  # hello message
                select_language(message)
                #select_topics(message)
                #select_num_of_articles(message)
                #select_country(message)

        @self.bot.message_handler(commands=["select_language"])
        def select_language(message):
            markup = get_custom_keyboard(items=self.languages)
            telegram_id = get_user_telegram_id(message)
            select_language_message = "Please, select language of the bot:"
            data_base_handler.add_chat_id(telegram_id=telegram_id,
                                          chat_id=message.chat.id)
            user_language = data_base_handler.get_user_language(telegram_id=telegram_id)
            if user_language == "Russian":
                select_language_message = "Пожалуйста, выберите язык бота:"
            self.bot.send_message(message.chat.id, select_language_message,
                                  reply_markup=markup)

        @self.bot.message_handler(commands=["get_news"])
        def get_news(message):
            self.news_api_handler.get_news(country="ru",
                                           topic="business")

        @self.bot.message_handler(commands=["select_country"])
        def select_country(message):
            telegram_id = get_user_telegram_id(message)
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            choose_country_message = "Select country you want to get news about:"
            choose_country_message_rus = "Выберите страну, из которой Вы хотите получать новости:"
            markup = get_custom_keyboard(items=self.countries,
                                         one_time_keyboard=True,
                                         )  # markup for reply
            markup_rus = get_custom_keyboard(items=self.countries_rus,
                                             one_time_keyboard=True)  # markup in Russian
            if user_language == "English":  # user uses English
                self.bot.send_message(message.chat.id, choose_country_message,
                                      reply_markup=markup)  # sends choose country message
            if user_language == "Russian":  # user uses Russian
                self.bot.send_message(message.chat.id, choose_country_message_rus,
                                      reply_markup=markup_rus)

        @self.bot.message_handler(commands=["select_num_of_articles"])
        def select_num_of_articles(message):
            telegram_id = get_user_telegram_id(message)
            num_of_articles = self.data_base_handler.get_user_num_of_articles(telegram_id=telegram_id)

            select_num_of_articles_message = "Select number of news you want to get on each topic\nNow you receive " + num_of_articles + " articles on each topic every day"
            select_num_of_articles_message_rus = "Выберите сколько статей Вы хотите получать на каждую тему:\nПока что я буду отправлять Вам по " + num_of_articles + " статьи на каждую тему."

            is_user_registered = check_user_registration(telegram_id=telegram_id)
            number_of_articles = [str(i) for i in range(1, self.MAX_NUM_OF_ARTICLES)]
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)

            markup = get_custom_keyboard(items=number_of_articles,
                                         one_time_keyboard=True)
            if user_language == "English":
                self.bot.send_message(message.chat.id,
                                      select_num_of_articles_message,
                                      reply_markup=markup)
            if user_language == "Russian":
                self.bot.send_message(message.chat.id,
                                      select_num_of_articles_message_rus,
                                      reply_markup=markup)

        @self.bot.message_handler(commands=["send_news"])
        def send_news(message):
            telegram_id = get_user_telegram_id(message)
            user_topics = str(data_base_handler.get_user_topics(telegram_id=telegram_id))
            user_topics = user_topics.split(";")[:-1]  # user's topics
            user_country = self.data_base_handler.get_user_country(telegram_id=telegram_id)
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            user_num_of_articles = self.data_base_handler.get_user_num_of_articles(telegram_id=telegram_id)
            for topic in user_topics:

                news = self.news_api_handler.get_news(topic=topic,
                                                      country=user_country,
                                                      num_of_articles=user_num_of_articles)
                topic_message = ""
                if user_language == "English":
                    topic_message = "Your news on topic \'" + topic + "\'"

                if user_language == "Russian":
                    topic_rus = self.language_handler.translate(topic,
                                                                first_language="English",
                                                                second_language="Russian")
                    topic_message = "Ваши новости на тему \'" + topic_rus + "\'"
                self.bot.send_message(message.chat.id, topic_message)
                news_to_text(message, news)


        @self.bot.message_handler(commands=["select_time"])
        def select_part_of_day(message):
            """
            Provides user with part of the day options
            opens markup keyboard with part of the day options
            :param message: message from the user
            """
            parts_of_day = ["Morning", "Afternoon", "Evening"]  # options
            parts_of_day_rus = ["Утро", "День", "Вечер"]  # options in Russian
            part_of_day_markup = get_custom_keyboard(items=parts_of_day,
                                                     one_time_keyboard=True)
            part_of_day_markup_rus = get_custom_keyboard(items=parts_of_day_rus,
                                                         one_time_keyboard=True)
            telegram_id = get_user_telegram_id(message)
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            choose_part_of_day_message = ""  # message to be sent
            if user_language == "English":
                choose_part_of_day_message = "Choose part of the day to get news at:"
                self.bot.send_message(message.chat.id, choose_part_of_day_message,
                                      reply_markup=part_of_day_markup)
            elif user_language == "Russian":
                choose_part_of_day_message = "Выберите время дня, в которое Вы хотите получать новости:"
                self.bot.send_message(message.chat.id, choose_part_of_day_message,
                                      reply_markup=part_of_day_markup_rus)

        @self.bot.message_handler(commands=["select_topics"])
        def select_topics(message):
            telegram_id = get_user_telegram_id(message)
            #  flag if user has any topics:
            user_check_topics = data_base_handler.check_topics(telegram_id=telegram_id)

            language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            select_topic_message = "Select topics you want to get news on:"
            topics_markup = get_custom_keyboard(items=self.topics,
                                                one_time_keyboard=True)  # topics markup
            markup_items = self.topics  # items to make a markup
            if language == "Russian":
                markup_items = self.topics_rus
                if user_check_topics:
                    markup_items = self.topics_ok_rus
                send_translated_message(select_topic_message, telegram_id=telegram_id,
                                        chat_id=message.chat.id, markup_items=markup_items)
            if language == "English":
                markup_items = self.topics
                if user_check_topics:
                    markup_items = self.topics_ok
                self.bot.send_message(message.chat.id, select_topic_message,
                                      reply_markup=get_custom_keyboard(
                                          items=markup_items))

        @self.bot.message_handler(commands=["lul"])
        def lul(message):
            telegram_id = get_user_telegram_id(message)
            self.send_news_to_user(telegram_id=telegram_id, chat_id=message.chat.id)

        @self.bot.message_handler(commands=["delete_topics"])
        def delete_topics(message):
            """
            pops up a delete topics markup keyboard

            :param message: message object received from the user

            """
            telegram_id = get_user_telegram_id(message)
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            are_topics_added = self.data_base_handler.check_topics(telegram_id=telegram_id)
            if not are_topics_added:
                no_topics_message = "You have no topics. Add some)"
                no_topics_message_rus = "Вы еще не добавили темы. Добавьте несколько):"
                topics_markup = get_custom_keyboard(items=self.topics,
                                                    one_time_keyboard=True)
                topics_markup_rus = get_custom_keyboard(items=self.topics_rus,
                                                        one_time_keyboard=True)
                if user_language == "English":
                    self.bot.send_message(message.chat.id, no_topics_message,
                                          reply_markup=topics_markup)
                if user_language == "Russian":
                    self.bot.send_message(message.chat.id, no_topics_message_rus,
                                          reply_markup=topics_markup_rus)

            else:
                user_topics = str(data_base_handler.get_user_topics(telegram_id=telegram_id))
                user_topics = user_topics.split(";")[:-1]  # user's topics
                select_topic_message = "Please select a topic you want to delete:"
                select_topic_message_rus = "Выберите тему, которую Вы хотите удалить:"
                topics_list = []
                for topic in user_topics:
                    if user_language == "English":
                        topics_list.append("- " + topic)
                    elif user_language == "Russian":
                        topic_rus = self.language_handler.translate(topic,
                                                                    first_language="English",
                                                                    second_language="Russian")
                        topics_list.append("- " + topic_rus)

                if user_language == "English":
                    self.bot.send_message(message.chat.id, select_topic_message,
                                          reply_markup=get_custom_keyboard(items=topics_list))
                if user_language == "Russian":
                    self.bot.send_message(message.chat.id, select_topic_message_rus,
                                          reply_markup=get_custom_keyboard(items=topics_list))


                """
                TO DO:
                add markup keyboard with user topics
                add method for handling button press
                """

        @self.bot.message_handler(commands=["info"])
        def info(message):
            name = self.get_me()
            print(name)
            print(message.from_user)

        def change_language(message):
            text = str(message.text)
            if text == "Change language" or text == "Поменять язык":
                select_language(message)

        @self.bot.message_handler(content_types=["text"])
        def text_is_received(message):
            select_time(message)
            country_name_selected(message)
            time_selected(message)
            topic_selected(message)
            num_of_articles_selected(message)
            language_selected(message)
            change_language(message)
            ok_message_received(message)
            add_topics_message_received(message)
            select_time_message_received(message)
            delete_topic_selected(message)
            change_num_of_articles_message_received(message)
            delete_topics_message_received(message)
            select_country_message_received(message)

        def country_name_selected(message):
            """
            handler for country selection
            :param message:
            """
            country = str(message.text)  # country user sent to the bot
            telegram_id = get_user_telegram_id(message)  # user's telegram id
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            is_user_registered = check_user_registration(telegram_id=telegram_id)
            current_time = date.today()  # current date
            country_name_selected_message = \
                "OK, I will send you news about " + country
            country_name_selected_message_rus = "OK, Я буду отправлять новости из страны \'" + country + "\'"
            if user_language == "English":
                if country in self.countries:  # user uses English
                    if not is_user_registered:
                        self.bot.send_message(message.chat.id,
                                              country_name_selected_message)  # sends message to the user
                    else:
                        show_basic_keyboard(message, country_name_selected_message)
                    print("Country is selected")

                    self.data_base_handler.add_country(telegram_id=telegram_id,
                                                       country_name=country,
                                                       current_time=current_time)

                    if not is_user_registered:
                        select_num_of_articles(message)
            if user_language == "Russian":  # user uses Russian
                country_eng = self.language_handler.translate(country,
                                                              first_language="Russian",
                                                              second_language="English")
                if country in self.countries_rus:
                    if not is_user_registered:  # user is not registered
                        self.bot.send_message(message.chat.id,
                                              country_name_selected_message_rus)
                    else:  # user is registered
                        show_basic_keyboard(message, country_name_selected_message_rus)
                    self.data_base_handler.add_country(telegram_id=telegram_id,
                                                       country_name=country_eng,
                                                       current_time=current_time)
                    if not is_user_registered:
                        select_num_of_articles(message)

        def topic_selected(message):
            """
            handler for topic selection
            :param message:  message from the user
            """
            topic = str(message.text)
            telegram_id = get_user_telegram_id(message)  # user telegram id
            language = data_base_handler.get_user_language(telegram_id=telegram_id)

            if topic != "OK" and (topic in self.topics or topic in self.topics_rus):
                print("TOPICS: ", self.topics)
                topic_selected_message = "Alright, " + topic + " is added to your topics"
                topic_is_used_message = "You already have " + topic + " in your topics"
                topic_selected_message_rus = "Хорошо, тема \'" + \
                                             self.language_handler.translate(topic, first_language="English",
                                                                             second_language="Russian") + \
                                             "\" добавлена в ваши темы"
                topic_is_used_message_rus = "Тема \'" + topic + "\' уже была добавлена в Ваши темы"
                # makes a request to the database and returns the result:
                if topic in self.topics_rus:
                    topic_eng = self.language_handler.translate(topic,
                                                                first_language="rus",
                                                                second_language="eng")
                else:
                    topic_eng = topic

                res = self.data_base_handler.add_topic(telegram_id=telegram_id,
                                                       topic=topic_eng)
                if res:  # topic could be added

                    if language == "Russian":
                        self.bot.send_message(message.chat.id, topic_selected_message_rus)
                    else:
                        self.bot.send_message(message.chat.id, topic_selected_message)
                else:  # topic was added before
                    if language == "English":  # user uses English
                        self.bot.send_message(message.chat.id,
                                              topic_is_used_message)
                    elif language == "Russian":  # user uses Russian
                        self.bot.send_message(message.chat.id,
                                              topic_is_used_message_rus)

        def delete_topic_selected(message):
            """
            Handles topic user sent and deletes it from the user's topics
            :param message:
            :return:
            """
            topic = str(str(message.text)[2:])
            if topic not in self.topics and topic not in self.topics_rus:
                return
            telegram_id = get_user_telegram_id(message)  # user's telegram id
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            topic_deleted_message = "OK. Topic " + topic + " was deleted from your topics"
            topic_deleted_message_rus = "OK. Тема \'" + topic + "\' была удалена из Ваших тем"
            error_message = "Please, select one topic from the list"
            error_message_rus = "Пожалуйста, выберите одну тему из списка"
            user_topics = str(data_base_handler.get_user_topics(telegram_id=telegram_id))
            user_topics = user_topics.split(";")[:-1]  # user's topics

            topics_list = []
            for t in user_topics:
                if user_language == "English":
                    topics_list.append("- " + t)
                elif user_language == "Russian":
                    topic_rus = self.language_handler.translate(t,
                                                                first_language="English",
                                                                second_language="Russian")
                    topics_list.append("- " + topic_rus)

            if user_language == "English":
                if topic in self.topics:
                    self.data_base_handler.delete_topic(telegram_id=telegram_id,
                                                        topic=topic)
                    show_basic_keyboard(message, topic_deleted_message)

            if user_language == "Russian":
                if topic in self.topics_rus:
                    topic_eng = self.language_handler.translate(topic, first_language="Russian",
                                                                second_language="English")
                    self.data_base_handler.delete_topic(telegram_id=telegram_id,
                                                        topic=topic_eng)
                    show_basic_keyboard(message, topic_deleted_message_rus)

        def language_selected(message):
            language = str(message.text)
            if language in self.languages:
                telegram_id = get_user_telegram_id(message)  # user telegram id
                language_selected_message = "OK now I will send you messages in " + str(language)
                current_time = date.today()  # current date
                self.data_base_handler.add_language(telegram_id=telegram_id,
                                                    language=language,
                                                    current_time=current_time)

                is_registered = check_user_registration(telegram_id=telegram_id)
                if not is_registered:  # user is not registered
                    select_topics(message)
                if is_registered:
                    show_basic_keyboard(message, language_selected_message,
                                        language=language)

        def num_of_articles_selected(message):
            max_num_of_articles = self.MAX_NUM_OF_ARTICLES
            num_of_articles = str(message.text)
            telegram_id = get_user_telegram_id(message)
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            current_time = date.today()
            is_user_registered = check_user_registration(telegram_id=telegram_id)
            num_of_articles_selected_message = "OK. I will send you " + str(num_of_articles) + " articles on each topic"
            num_of_articles_selected_message_rus = "OK. Я буду отправлять Вам по " + str(num_of_articles) + " статьи на каждую тему"
            error_message = "Please, enter a number from 1 to " + str(max_num_of_articles)
            error_message_rus = "Пожалуйста, введите число от 1 до " + str(max_num_of_articles)

            if user_language == "English":
                if num_of_articles.isdigit() and 0 < int(num_of_articles) <= max_num_of_articles:
                    self.data_base_handler.add_num_of_articles(telegram_id=telegram_id,
                                                               current_time=current_time,
                                                               num_of_articles=num_of_articles)
                    if not is_user_registered:
                        self.data_base_handler.update_user_first_time_enter(telegram_id=telegram_id)
                    show_basic_keyboard(message, num_of_articles_selected_message)

                else:
                    if num_of_articles.isdigit():
                        self.bot.send_message(message.chat.id, error_message)
            if user_language == "Russian":
                if num_of_articles.isdigit() and 0 < int(num_of_articles) <= max_num_of_articles:
                    self.data_base_handler.add_num_of_articles(telegram_id=telegram_id,
                                                               current_time=current_time,
                                                               num_of_articles=num_of_articles)
                    if not is_user_registered:
                        self.data_base_handler.update_user_first_time_enter(telegram_id=telegram_id)
                    show_basic_keyboard(message, num_of_articles_selected_message_rus)
                else:
                    if num_of_articles.isdigit():
                        self.bot.send_message(message.chat.id, error_message_rus)

        def select_time(message):
            """
            Handles part of the day message from the user
            sends markup for time selection
            :param message: message from the user
            """
            morning_time_options = ["5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00"]  # options for morning
            afternoon_time_options = ["12:00", "13:00", "14:00", "15:00", "16:00"]  # options for afternoon
            evening_time_options = ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00"]  # options for evening
            select_time_message = "Select time you want to get news at:"
            select_time_message_rus = "Выберите время, в которое Вы хотите получать новости:"
            text = str(message.text)
            morning_markup = get_custom_keyboard(items=morning_time_options,
                                                 one_time_keyboard=True)  # markup for morning options
            afternoon_markup = get_custom_keyboard(items=afternoon_time_options,
                                                   one_time_keyboard=True)  # markup for afternoon options
            evening_markup = get_custom_keyboard(items=evening_time_options,
                                                 one_time_keyboard=True)  # markup for evening options
            if text == "Morning":
                self.bot.send_message(message.chat.id, select_time_message,
                                      reply_markup=morning_markup)  # sends markup for morning
            if text == "Afternoon":
                self.bot.send_message(message.chat.id, select_time_message,
                                      reply_markup=afternoon_markup)  # sends markup for afternoon
            if text == "Evening":
                self.bot.send_message(message.chat.id, select_time_message,
                                      reply_markup=evening_markup)  # sends markup for evening
            if text == "Утро":
                self.bot.send_message(message.chat.id, select_time_message_rus,
                                      reply_markup=morning_markup)
            if text == "День":
                self.bot.send_message(message.chat.id, select_time_message_rus,
                                      reply_markup=afternoon_markup)
            if text == "Вечер":
                self.bot.send_message(message.chat.id, select_time_message_rus,
                                      reply_markup=evening_markup)

        def time_selected(message):
            """
            Handles time message from user
            :param message: message object received from the user
            :return:
            """
            text = str(message.text)
            hours = [str(i) for i in range(0, 24)]
            print(text.split(":"))
            if text.split(":")[0] in hours and text.split(":")[-1] == "00":
                selected_time = str(message.text)  # selected time
                telegram_id = get_user_telegram_id(message)  # user's telegram id
                current_time = date.today()  # current date
                is_user_registered = check_user_registration(telegram_id=telegram_id)
                user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
                self.data_base_handler.add_time(telegram_id=telegram_id,
                                                news_time=selected_time,
                                                current_time=current_time)
                time_selected_message = "OK, I will send you news at " + str(selected_time) + " every day"
                time_selected_message_rus = "OK. Я буду отравлять новости в " + str(selected_time) + " каждый день"
                if user_language == "English":
                    if not is_user_registered:
                        self.bot.send_message(message.chat.id, time_selected_message)
                    else:
                        show_basic_keyboard(message, time_selected_message)
                if user_language == "Russian":
                    if not is_user_registered:
                        self.bot.send_message(message.chat.id, time_selected_message_rus)
                    else:
                        show_basic_keyboard(message, time_selected_message_rus)

                if not is_user_registered:
                    select_country(message)

        def ok_message_received(message):
            """
            Handles OK message from user
            Sends the user's list of topics
            :param message: message object received from the user
            """
            text = str(message.text)
            telegram_id = get_user_telegram_id(message)
            user_language = data_base_handler.get_user_language(telegram_id=telegram_id)
            user_registered = check_user_registration(telegram_id=telegram_id)
            if text == "OK" or text == "ОК":  # OK in English or Russian
                user_topics = str(data_base_handler.get_user_topics(telegram_id=telegram_id))
                topics_list_message = "OK. Now your topics are: \n"  # string with user topics
                if user_language == "Russian":  # user uses Russian
                    topics_list_message = "OK. Ваши темы: \n"
                user_topics = user_topics.split(";")[:-1]  # user's topics
                print("USER_TOPICS: ", user_topics)
                for topic in user_topics:  # adds all user's topics to string
                    if user_language == "English":
                        topics_list_message += "- " + topic + "\n"
                    if user_language == "Russian":
                        translated_topic = self.language_handler.translate(message=topic,
                                                                           first_language="English",
                                                                           second_language="Russian")
                        topics_list_message += "- " + translated_topic + "\n"
                if not user_registered:
                    self.bot.send_message(message.chat.id, topics_list_message)
                else:
                    show_basic_keyboard(message, topics_list_message)
                if not user_registered:  # user is not registered
                    select_part_of_day(message)

        def add_topics_message_received(message):
            """
            Handles 'Add topics' message from the user
            :param message: message object received from the user
            """
            text = str(message.text)
            telegram_id = get_user_telegram_id(message)
            if text == "Add topics" or text == "Добавить темы":
                select_topics(message)

        def select_time_message_received(message):
            """
            Handles 'Change time' message from the user
            :param message: message object from the user
            """
            text = str(message.text)
            if text == "Change news time" or text == "Поменять время отправки новостей":
                select_part_of_day(message)

        def select_country_message_received(message):
            text = str(message.text)
            if text == "Select country" or text == "Выбрать страну":
                select_country(message)

        def change_num_of_articles_message_received(message):
            """
            Handles 'Change number of articles message' from the user
            :param message: message object from the user
            :return:
            """
            text = str(message.text)
            if text == "Change number of articles" or text == "Изменить число статей":
                select_num_of_articles(message)

        def delete_topics_message_received(message):
            text = str(message.text)
            if text == "Delete topics" or text == "Удалить темы":
                delete_topics(message)


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
                markup.add(str(item))
            return markup

        def check_user_registration(telegram_id):
            """

            :param telegram_id: int;  Telegram id of the user
            :return: True if user was registered before
                     False if user wasn't registered
            """
            first_time_enter = self.data_base_handler.get_user_first_time_enter(telegram_id=telegram_id)

            print("IS_REGISTERED:", first_time_enter)
            print("RERERE: ", self.invert_bool(first_time_enter))
            return self.invert_bool(first_time_enter)

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

        def news_to_text(message, news):
            """
            Transforms news dictionary to text
            Gets list of dictionaries
            :return:
            """
            message_text = ""
            telegram_id = get_user_telegram_id(message)
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            print("NEWS_TO_TEXT", news)
            for article in news:
                message_text = ""
                photo_url = article["urlToImage"]
                if user_language == "English":  # makes message in English
                    message_text += "- Article by " + article["source"]["name"] + "\n"
                    message_text += "- Title: " + article["title"] + "\n"
                    message_text += "- Article: " + article["content"] + "\n"
                    message_text += "Read full article on " + article["url"]
                if user_language == "Russian":
                    message_text += "- Автор: " + article["source"]["name"] + "\n"
                    message_text += "- Заголовок: " + article["title"] + "\n"
                    message_text += "- Прочитать статью полностью можно на " + article["url"]
                print("MESSAGE_TEXT", message_text)

                if photo_url != "None" and photo_url != None:
                    self.bot.send_photo(message.chat.id, photo=photo_url, caption=message_text)
                else:
                    self.bot.send_message(message.chat.id, message_text)

        def send_translated_message(text, **params):
            telegram_id = params.get("telegram_id", None)  # user's telegram id
            chat_id = params.get("chat_id", None)  # chat id to send message
            markup_items = params.get("markup_items", None)
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)

            if user_language == "Russian":
                #  translates message into russian:
                translated_message = self.language_handler.translate(message=text,
                                                                     first_language="English",
                                                                     second_language="Russian")
                # sends message with no markup
                if not markup_items:
                    self.bot.send_message(chat_id, translated_message)
                else:
                    markup = get_custom_keyboard(items=markup_items)
                    self.bot.send_message(chat_id, translated_message,
                                          reply_markup=markup)


        def show_basic_keyboard(message, text, **k):
            #self.bot.send_message(message.chat.id, "", reply_markup=self.markup_hider)
            lang = k.get("language", "English")
            telegram_id = get_user_telegram_id(message)
            user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
            basic_markup = get_custom_keyboard(items=self.basic_markup_buttons)
            if user_language == "Russian":
                text = self.language_handler.translate(text,
                                                       first_language="English",
                                                       second_language="Russian")
                basic_markup = get_custom_keyboard(items=self.russian_basic_markup_buttons)
            self.bot.send_message(message.chat.id, str(text), reply_markup=basic_markup)

    def get_token(self):
        """
        gets token from different types of files
        :return: token: str
        """
        token_path_file_name = self.token_path.split("/")[-1]  # name of file with token
        token_path_extension = token_path_file_name.split(".")[-1]  # extension of token file
        if token_path_extension == "txt":  # text file
            return self.get_token_from_txt()

    def send_news_to_users(self, ids):
        """
        :param ids: list    list of users telegram_ids
        """



    def get_token_from_txt(self):
        """
        gets token from txt file
        :return: token: str
        """
        f = open(self.token_path, "r")
        return f.read()

    def polling(self, *args):
        self.bot.polling(*args)

    def invert_bool(self, x):
        if x == True or x == "True":
            return False
        else:
            return True
