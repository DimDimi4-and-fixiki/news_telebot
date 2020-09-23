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
        query = "UPDATE User SET News_time = " + "\"" + str(news_time) + "\" WHERE Telegram_id = " + str(telegram_id)
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




data_base_handler = DataBaseHandler(path="news_bot_db")