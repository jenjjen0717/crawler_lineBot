from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from linebot.models import *
from urllib.parse import quote, unquote
from selenium.webdriver.common.keys import Keys

from postback import *
from postback import *
from config import *

import time
import re


def shopee_option(data):

    driver = webdriver.Chrome()
    driver.set_window_size(1200, 960)

    driver.get(data)
    time.sleep(2)

    optionList = []
    option = driver.find_elements_by_css_selector(
        ".flex.items-center._2oeDUI > .product-variation"
    )
    for i in option:
        optionList.append(i.text)

    stockStat = []
    price = []
    if len(optionList) == 0:
        optionList.append(driver.find_element_by_css_selector(".attM6y > span").text)
        stockStat.append(
            driver.find_element_by_css_selector(
                ".flex.items-center._90fTvx > .flex.items-center > div:nth-child(2)"
            ).text
        )
        price.append(
            driver.find_element_by_css_selector(".flex.items-center > .Ybrg9j").text
        )
    else:
        stocklist = []
        stockCheck = driver.find_elements_by_css_selector(
            ".flex.items-center._2oeDUI > .product-variation.product-variation--disabled"
        )
        for i in stockCheck:
            stocklist.append(i.text)
        print(stocklist)

        if len(optionList) == 0:
            optionList.append(
                driver.find_element_by_css_selector(".attM6y > span").text
            )
        else:
            for item in optionList:
                if item in stocklist:
                    stockStat.append("Out of Stock")
                    price.append("NONE")
                else:
                    driver.find_element_by_css_selector(
                        f".flex.items-center._2oeDUI > button:nth-child({optionList.index(item)+1})"
                    ).click()
                    time.sleep(1)
                    stockStat.append(
                        driver.find_element_by_css_selector(
                            ".flex.items-center._90fTvx > .flex.items-center > div:nth-child(2)"
                        ).text
                    )
                    price.append(
                        driver.find_element_by_css_selector(
                            ".flex.items-center > .Ybrg9j"
                        ).text
                    )

    url = "https://shopee.tw/" + quote(
        re.search("[^(?<=https://shopee.tw/)].*", data).group(), encoding="utf-8"
    )
    print(url)
    print(optionList)
    print(stockStat)
    print(price)

    driver.close()

    message = itemOption_carousel("選項", url, optionList, price, stockStat)
    return message


if __name__ == "__main__":
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import *

    msg = shopee_option(
        "https://shopee.tw/【怪獸部落LitoMon】貓族-98-鮮肉主食糧800g-貓糧-鮮肉糧-主食-乾食-官方直送-效期最新-i.326491541.7659409525?sp_atk=4d710b8c-2472-4860-9cba-7a413aca0537"
    )
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(USERID, msg)
