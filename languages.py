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
            "OK now I will send you messages in Russian": "OK. Теперь я буду отправлять тебе сообщения на Русском"

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
            if message.isdigit():
                return message
            else:
                print("No such a message in dictionary")
                return False


