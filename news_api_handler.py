from newsapi import NewsApiClient


class NewsApiHandler(object):

    def __init__(self, **kwargs):
        self.news_api_key_path = kwargs.get("path", None)
        self.api_key = self.get_news_api_key()
        print("API Key: ", self.api_key)
        self.news_api = NewsApiClient(api_key=self.api_key)

    def get_news(self, **kwargs):
        topic = str(kwargs.get("topic"))
        country = str(kwargs.get("country"))
        news = self.news_api.get_top_headlines(country=country,
                                               category=topic,
                                               )
        print(news["articles"])
        print(type(news))

    def get_news_api_key(self):
        """
        gets news_api key
        :return: str        news_api key
        """
        if self.news_api_key_path.split(".")[-1] == "txt":  # txt file
            return self.get_news_api_key_from_txt()

    def get_news_api_key_from_txt(self):
        """
        gets news_api key from txt file
        :return: key: str
        """
        f = open(self.news_api_key_path, "r")
        return f.read()




