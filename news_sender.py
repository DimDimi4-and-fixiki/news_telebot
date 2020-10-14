import schedule
import time
from datetime import datetime


class NewsSender(object):
    """
    class for sending news to the user on time
    Sends articles to the users
    """
    def __init__(self, **kwargs):
        self.bot = kwargs.get("bot", None)
        self.data_base_handler = kwargs.get("data_base_handler", None)  # DataBaseHandler object
        self.news_api_handler = kwargs.get("news_api_handler", None)  # NewsApiHandler object
        self.language_handler = kwargs.get("language_handler", None)
        self.sleep_interval = 5

    def send_news(self):
        """
        Checks the time and calls send news
        """
        while True:
            self.send_news_every_day()
            time.sleep(self.sleep_interval)

    def send_news_every_day(self):
        """
        Send news if the time has come
        """
        cur_time = self.get_current_time()
        times = ["00:00", "01:00", "02:00",
                 "03:00", "04:00", "05:00",
                 "06:00", "07:00", "08:00",
                 "09:00", "10:00", "11:00",
                 "12:00", "13:00", "14:00",
                 "15:00", "16:00", "17:00",
                 "18:00", "19:00", "20:00",
                 "21:00", "22:00", "23:00", "00:30"]

        for t in times:
            if self.is_time(cur_time, t):
                self.send_news_by_time(time=t)
                break

    def is_time(self, t1, t2):
        """
        :return bool
            True if t1 is close to t2
            False if t1 is not close to t2
        """
        hours1 = int(t1.split(":")[0])
        hours2 = int(t2.split(":")[0])
        minutes1 = int(t1.split(":")[1])
        minutes2 = int(t2.split(":")[1])
        seconds1 = float(t1.split(":")[-1])
        seconds2 = 0.0
        if hours1 == hours2 and minutes1 == minutes2 and abs(seconds2 - seconds1) <= self.sleep_interval:
            time.sleep(self.sleep_interval)
            print("T2", t2)
            return True
        if abs(hours1 - hours2) <= 1 and minutes1 == 59 and seconds1 >= 60 - self.sleep_interval:
            time.sleep(2)
            print("T2", t2)
            return True
        return False

    def send_news_by_time(self, **kwargs):
        """
        Sends news to users whose news_time = kwargs.news_time
        :param kwargs:
            news_time: str  time to send news in "hh:mm" format
        :return:
        """
        news_time = kwargs.get("time", None)
        ids = self.data_base_handler.get_users_by_time(time=news_time)
        print("IDS: ", ids)
        for telegram_id in ids:
            chat_id = self.data_base_handler.get_user_chat_id(telegram_id=telegram_id)
            self.send_news_to_user(telegram_id=telegram_id, chat_id=chat_id)


    def send_news_to_user(self, **kwargs):
        """
        Sends news to the user with particular telegram ID
        :param kwargs:
            telegram_id: str    the user's telegram_id
            chat_id:     str    the chat id of the user
        """
        telegram_id = kwargs.get("telegram_id", None)
        chat_id = kwargs.get("chat_id", None)
        user_topics = str(self.data_base_handler.get_user_topics(telegram_id=telegram_id))
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
            self.bot.send_message(chat_id, topic_message)
            self.send_articles(news=news, telegram_id=telegram_id, chat_id=chat_id)

    def send_articles(self, news, **kwargs):
        """
        Transforms news dictionary to text
        Gets list of dictionaries
        :return:
        """
        message_text = ""
        telegram_id = kwargs.get("telegram_id", None)
        user_language = self.data_base_handler.get_user_language(telegram_id=telegram_id)
        chat_id = kwargs.get("chat_id", None)
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
                self.bot.send_photo(chat_id, photo=photo_url, caption=message_text)
            else:
                self.bot.send_message(chat_id, message_text)

    @staticmethod
    def get_current_time():
        """
        gets current time in format "hh:mm:ss"
        """
        cur_full_time = str(datetime.now())
        cur_time = cur_full_time.split(" ")[-1]
        return cur_time
