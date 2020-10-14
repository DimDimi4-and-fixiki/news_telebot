from newsapi import NewsApiClient


class NewsApiHandler(object):

    def __init__(self, **kwargs):
        self.news_api_key_path = kwargs.get("path", None)
        self.api_key = self.get_news_api_key()
        print("API Key: ", self.api_key)
        self.news_api = NewsApiClient(api_key=self.api_key)
        self.country_name_to_short_name = {  # dictionary with countries short names
            "Russia": "ru",
            "United States": "us",
            "France": "fr",
            "United Kingdom": "gb",
            "Germany": "de",
            "Canada": "ca",
        }

    def get_news(self, **kwargs):
        """
        gets news on particular topic
        :param kwargs:
            num_of_articles: str    number of articles to send

        :return:
        """

        topic = str(kwargs.get("topic", "Entertainment")).lower()
        country = str(kwargs.get("country", "Russia"))
        #  gets short name of the country
        country_short_name = self.country_name_to_short_name[country]
        num_of_articles = int(kwargs.get("num_of_articles", 3))
        news = self.news_api.get_top_headlines(country=country_short_name,
                                               category=topic,
                                               page_size=num_of_articles)
        return news["articles"]

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




