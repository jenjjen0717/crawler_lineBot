from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from linebot.models import *

import time
import random
import string

from postback import *
from config import *


def shopee_option(data):

    driver = webdriver.Chrome()
    driver.set_window_size(1024, 960)

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

    print(optionList)
    print(stockStat)
    print(price)

    driver.close()

    message = itemOption_carousel("選項", data, optionList, price, stockStat)
    return message


if __name__ == "__main__":
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import *

    msg = shopee_option(
        "https://shopee.tw/%E3%80%90%E6%80%AA%E7%8D%B8%E9%83%A8%E8%90%BDLitoMon%E3%80%91%E8%B2%93%E6%97%8F-98-%E9%AE%AE%E8%82%89%E4%B8%BB%E9%A3%9F%E7%B3%A7800g-%E8%B2%93%E7%B3%A7-%E9%AE%AE%E8%82%89%E7%B3%A7-%E4%B8%BB%E9%A3%9F-%E4%B9%BE%E9%A3%9F-%E5%AE%98%E6%96%B9%E7%9B%B4%E9%80%81-%E6%95%88%E6%9C%9F%E6%9C%80%E6%96%B0-i.326491541.7659409525?sp_atk=9a81d319-17fa-4d49-90aa-da7946608e79"
    )
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(USERID, msg)
