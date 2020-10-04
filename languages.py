"""
language translation dictionaries

Languages:
    English
    Russian
"""


class LanguageHandler(object):
    """
    class for translating in different languages
    """
    def __init__(self):

        self.greetings_message_rus = "Привет, я бот для отправки новостей.\nЯ буду отправлять " \
                                "тебе новости на разные темы каждый день)"

        self.eng_to_rus = {
            "Business": "Бизнес",
            "Entertainment": "Развлечения",
            "Health": "Здоровье",
            "Science": "Наука",
            "Sports": "Спорт",
            "Technology": "Технологии",
            """Hello, I'm a news bot.\nYou can get news on different topics every day)""": self.greetings_message_rus,
            "OK now I will send you messages in Russian": "OK. Теперь я буду отправлять тебе сообщения на Русском",
            "Choose topics you want to get news on:": "Выберите темы, на которые вы хотите получать новости",
            "Welcome back! What do you want to do?": "Рад снова тебя видеть). Что будешь делать?",
            "Please, select language of the bot:": "Выберите язык, на котором Вам отправлять сообщения:",
            "Select country you want to get news about:": "Выберите страну, о которой Вы хотите получать новости",
            "Select number of news you want to get on each topic\nNow you receive 3 articles on each topic every day": "Выберите число статей которые Вы хотите получать на каждую тему.\nСейчас вы получаете 3 статьи на каждый топик раз в день",
            "Choose part of the day:": "Выберите время дня",
            "Select topics you want to get news on:": "Выберите темы, на которые вы хотите получать новости",
            "You have no topics. Add some)": "Вы не выбрали ни одной темы. Добавьте темы)",
            "OK, I will send you news about ": "OK. Теперь я буду отправлять тебе новости из страны ",
            "Alright, ": "Хорошо, тема",
            " is added to your topics": "добавлена в Ваши темы",
            "You already have ": "Вы уже добавляли тему ",
            "in your topics": "в Ваши темы",
            "OK. I will send you ": "OK. Я буду отправлять тебе ",
            " articles on each topic": "статьи на каждую тему",
            "Please, enter a number from 1 to ": "Введите число от 1 до ",
            "You don't have such a topic": "Вы не выбирали такую тему",
            " was deleted from your topics": "была удалена из Ваших тем",
            "Select time you want to get news at": "Выберите время, в которое Вы хотите получать новости",
            "Morning": "Утро",
            "Afternoon": "День",
            "Evening": "Вечер",
            "OK, I will send you news at ": "OK. Я буду отправлять тебе новости в ",
            " every day)": " каждый день)",
            "Add topics": "Добавить темы",
            "Change news time": "Поменять время отправки новостей",
            "Select country": "Выбрать страну",
            "Delete topics": "Удалить темы",
            "Change number of articles": "Изменить число статей",
            "Change language": "Поменять язык",
            "Russia": "Россия",
            "United States": "США",
            "France": "Франция",
            "United Kingdom": "Великобритания",
            "Germany": "Германия",
            "Canada": "Канада",

        }

        self.rus_to_eng = {
            "Бизнес": "Business",
            "Развлечения": "Entertainment",
            "Здоровье": "Health",
            "Наука": "Science",
            "Спорт": "Sports",
            "Технологии": "Technology",
        }

    def translate(self, message, **kwargs):
        """
        :param message: str     message to translate
        :param kwargs:
            from: str           original language
            to:   str           final language
        :return: str            translated message
        you can use both 'eng' and 'English'
                         'rus' and 'Russian'
        """
        message = str(message)
        first_language = kwargs.get("first_language", None)
        second_language = kwargs.get("second_language", None)
        if (first_language == "English" or first_language == "eng") and (second_language == "Russian" or second_language == "rus"):
            if message in self.eng_to_rus.keys():
                return self.eng_to_rus[message]
            elif message.isdigit():
                return message
            else:
                print("No such a message in dictionary")
                return False
        if (first_language == "Russian" or first_language == "rus") and (second_language == "English" or second_language == "eng"):
            if message in self.rus_to_eng.keys():
                return self.rus_to_eng[message]
            elif message.isdigit():
                return message
            else:
                print("rus to eng error")
                return ""



