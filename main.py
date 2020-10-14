from my_tele_bot import MyTeleBot
import threading
from news_sender import NewsSender

"""
Put bot and news sender in separate threads using 'threading'
create class for News Sender
"""

news_sender = NewsSender()  # NewsSender object


def send_news():
    news_sender.send_news()


def bot_polling():
    bot = MyTeleBot(token_path="secure_codes/token.txt")
    #  configuring news_sender:
    news_sender.data_base_handler = bot.data_base_handler
    news_sender.news_api_handler = bot.news_api_handler
    news_sender.language_handler = bot.language_handler
    news_sender.bot = bot.bot
    bot.polling()


def main():
    thread1 = threading.Thread(target=bot_polling)
    thread2 = threading.Thread(target=send_news)
    thread1.start()
    thread2.start()


if __name__ == "__main__":
    main()