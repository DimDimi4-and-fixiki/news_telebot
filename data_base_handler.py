import sqlite3


class DataBaseHandler(object):
    """
    Handler for database in SQLite
    """
    def __init__(self, **kwargs):
        self.data_base_file_path = kwargs.get("path", None)  # database file
        self.connection = None  # connection to the database
        try:
            self.create_connection()
        except Exception:
            print("Data base connection crashed")

    def create_connection(self):
        """
        creates connection to the database
        """
        try:
            self.connection = sqlite3.connect(self.data_base_file_path)  # makes connection
        except Exception as e:
            print(e)

    def make_select_query(self, query: str):
        """
        makes SELECT query
        :param query: str;   query text
        :return: rows        result of the query
        """
        print(query)
        self.create_connection()
        cur = self.connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows

    def make_insert_query(self, query: str):
        """
        makes INSERT query to the database
        :param query: str;  query text
        """
        self.create_connection()
        print(query)
        cursor = self.connection.cursor()
        count = cursor.execute(query)
        self.connection.commit()

    def make_update_query(self, query: str):
        """
        :param query:
        :return:
        """
        self.create_connection()
        print(query)
        cursor = self.connection.cursor()
        count = cursor.execute(query)
        self.connection.commit()

    def add_user(self, **kwargs):
        """
        adds user to the database
        :param kwargs:
            nickname: str;       user's nickname in Telegram
            register_time: str;  time of user's registration
        :return:
        """
        user_nickname = kwargs.get("nickname", None)
        register_time = kwargs.get("register_time", None)
        telegram_id = kwargs.get("telegram_id", None)
        query = "INSERT INTO User(Country, Categories, News_time, Register_time, Telegram_id) VALUES("
        query += "Null, Null, Null, " + "\"" + str(register_time) + "\", " + str(telegram_id) + ")"
        print(query)
        self.make_insert_query(query=query)

    def check_user(self, telegram_id):
        """

        :param telegram_id: int;  Telegram id of the user
        :return: True if user is registered
                 False if user is not registered
        """
        query = "SELECT * FROM User WHERE Telegram_id = " + str(telegram_id)
        res = self.make_select_query(query=query)  # select all users with this Telegram_id
        print("LUL", res)
        return res != []

    def add_country(self, **kwargs):
        telegram_id = kwargs.get("telegram_id", None)
        country_name = kwargs.get("country_name", None)
        current_time = kwargs.get("current_time", None)
        is_user_registered = self.check_user(telegram_id=telegram_id)
        if not is_user_registered:
            self.add_user(telegram_id=telegram_id, current_time=current_time)
        query = "UPDATE User SET Country = " + "\"" + str(country_name) + "\" WHERE Telegram_id = " + str(telegram_id)
        self.make_update_query(query=query)

    def add_time(self, **kwargs):
        """
        adds information about news time in the database
        :param kwargs:
            telegram_id: str;  user's telegram id
            news_time: str;    time which user chose
            current_time: str; current time
        :return:
        """
        telegram_id = kwargs.get("telegram_id", None)
        news_time = kwargs.get("news_time", None)
        current_time = kwargs.get("current_time", None)
        is_user_registered = self.check_user(telegram_id=telegram_id)
        if not is_user_registered:
            self.add_user(telegram_id=telegram_id, current_time=current_time)
        query = "UPDATE User SET News_time = " + "\"" + str(news_time) + "\" WHERE Telegram_id = " +\
                str(telegram_id)
        self.make_update_query(query=query)

    def add_language(self, **kwargs):
        """
        adds information about language of the bot in the database
        :param kwargs:
            telegram_id: str;   user's telegram id
            language: str       language of the bot
            current_time: str;  current time
        :return:
        """
        telegram_id = kwargs.get("telegram_id", None)
        language = kwargs.get("language", None)
        current_time = kwargs.get("current_time", None)
        is_user_registered = self.check_user(telegram_id=telegram_id)
        if not is_user_registered:
            self.add_user(telegram_id=telegram_id, current_time=current_time)
        query = "UPDATE User SET Language = \"" + str(language) + "\" WHERE Telegram_id = " + \
                str(telegram_id)
        self.make_update_query(query=query)

    def add_num_of_articles(self, **kwargs):
        """
        Adds information about the user's number of articles in the database
        :param kwargs:
            telegram_id: str;       user's telegram id
            current_time: str;      current time
            num_of_articles: int    number of articles
        :return:
        """
        telegram_id = kwargs.get("telegram_id", None)
        current_time = kwargs.get("current_time", None)
        num_of_articles = kwargs.get("num_of_articles", None)
        is_user_registered = self.check_user(telegram_id=telegram_id)
        if not is_user_registered:
            self.add_user(telegram_id=telegram_id, current_time=current_time)
        query = "UPDATE User SET Num_of_articles = " + str(num_of_articles) + \
                " WHERE Telegram_id = " + str(telegram_id)
        self.make_update_query(query=query)

    def check_topics(self, **kwargs):
        """
        checks if user has any topics
        :param kwargs:
        :return: bool
            True if there are some topics
            False if there are no topics
        """
        telegram_id = kwargs.get("telegram_id", None)
        query = "SELECT Categories FROM User WHERE Telegram_id = " + \
                str(telegram_id)  # gets categories of the user
        res = self.make_select_query(query=query)  # makes SELECT query
        print(res)
        return res != [(None,)]

    def delete_topic(self, **kwargs):
        """
        deletes topic from user topics
        :param kwargs:
            telegram_id:    user's telegram_id
            topic: str      topic which should be deleted
        :return:
            False if topic is not in user's topics
            True if topic is deleted successfully
        """
        telegram_id = kwargs.get("telegram_id")
        topic = kwargs.get("topic")  # topic to delete
        user_topics = self.get_user_topics(telegram_id=telegram_id)
        if topic not in user_topics:
            return False
        new_user_topics = user_topics.replace(topic + ";", "")
        query = "UPDATE User SET Categories = \"" + str(new_user_topics) + \
                "\" WHERE Telegram_id = " + str(telegram_id)  # query to change topics
        print("DELETE: ", query)
        return True

    def add_topic(self, **kwargs):
        """
        adds one topic to existed topics of the user
        :param kwargs:
            topic : str     name of the topic
            telegram_id:    user's telegram id
        :returns:
            True if topic is added successfully
            False if topic is already chosen
        """
        telegram_id = kwargs.get("telegram_id", None)
        topic = kwargs.get("topic", None)
        is_topic_used = self.check_if_topic_is_used(telegram_id=telegram_id,
                                                    topic=topic)
        if is_topic_used:
            return False
        else:
            user_topics = self.get_user_topics(
                telegram_id=telegram_id)
            new_user_topics = user_topics + str(topic) + ";"
            query = "UPDATE User SET Categories = \"" + str(new_user_topics) \
                    + "\" WHERE Telegram_id = " + str(telegram_id)
            print(query)
            self.make_update_query(query=query)  # updates user's topics
            return True

    def get_user_first_time_enter(self, **kwargs):
        """
        gets user First_time_register value
            'True' if it is first time user enters a bot
            'False' if user entered a bot before
        :param kwargs:
        :return: str    user's First_time_register value
        """
        telegram_id = kwargs.get("telegram_id", None)
        query = "SELECT First_time_enter FROM User WHERE Telegram_id = " \
                + str(telegram_id)
        res = self.make_select_query(query=query)
        return res[0][0]

    def update_user_first_time_enter(self, **kwargs):
        """
        Sets user's First_time enter to 'False'
        :param kwargs:
        :return:
        """
        telegram_id = kwargs.get("telegram_id")


    def get_user_topics(self, **kwargs):
        """

        :param kwargs:
            telegram_id:    user's telegram id
        :return: str    all user topics separated by ';'
        """
        telegram_id = kwargs.get("telegram_id", None)
        query = "SELECT Categories FROM User WHERE Telegram_id = " + str(telegram_id)
        res = self.make_select_query(query=query)
        print("User topics: ", res)
        if res == [(None,)]:  # no topics at all
            return ""
        else:
            return res[0][0]

    def get_user_language(self, **kwargs):
        """
        gets language that user has chosen
        :param kwargs:
        :return: str    user's language
        """
        telegram_id = kwargs.get("telegram_id", None)
        query = "SELECT Language FROM User WHERE Telegram_id = " + str(telegram_id)
        res = self.make_select_query(query=query)
        return str(res[0][0])

    def check_if_topic_is_used(self, **kwargs):
        """
        checks if the user has already chosen the topic
        :param kwargs:
            telegram_id:    user's telegram id
            topic: str      name of the topic
        :returns:
            True if topic is already added
            False if topic is not used by the user
        """
        telegram_id = kwargs.get("telegram_id", None)
        topic = kwargs.get("topic")
        user_topics = self.get_user_topics(telegram_id=telegram_id)
        return topic in user_topics




data_base_handler = DataBaseHandler(path="news_bot_db")
