from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests


class item(ABC):

    def __init__(self, keyword):
        self.keyword = keyword

    @abstractmethod
    def scrape(self):
        pass


class shopee(item):
    def get_list(self):
        r = requests.get("https://shopee.tw/search?keyword=" + self.keyword)

        soup = BeautifulSoup(r.content, "html.parser")

        cards = soup.find_all(
            'div', {'class': "col-xs-2-4 shopee-search-item-result__item", 'data-sqe': "item"}, limit=5)

        content = ""
        for card in cards:

            title = card.find(
                "div", {"class": "_10Wbs- _5SSWfi UjjMrh"}).getText()

            sold = card.find(
                "div", {"class": "_2VIlt8"}).getText()

            address = card.find(
                "div", {"class": "_1w5FgK"}).getText()

            # 將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
            content += f"{title} \n{sold}顆星 \n{address} \n\n"

        return content
