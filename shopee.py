from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from linebot.models import *
from urllib.parse import quote, unquote
from selenium.webdriver.common.keys import Keys

from flex_msg import *
from postback import *
from config import *

import time
import random
import string
import re


def shopee(data):

    chromeOption = webdriver.ChromeOptions()
    # 設定瀏覽器的語言為utf-8中文
    chromeOption.add_argument("--lang=zh-CN.UTF8")
    chromeOption.add_argument("--no-sandbox")
    chromeOption.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chromeOption)

    keyword = data.split(" ")[0]
    minP = data.split(" ")[1]
    maxP = data.split(" ")[2]

    # driver = webdriver.Chrome()
    domain = "https://shopee.tw/"
    driver.set_window_size(1200, 960)

    driver.get(domain)
    time.sleep(1)

    image_path = "./static/tmp/test.png"
    driver.save_screenshot(image_path)
    time.sleep(2)

    # 彈窗廣告處理
    """action = ActionChains(driver)
    action.move_by_offset(930, 70).click().perform()"""
    # 關鍵字搜尋
    search_item = driver.find_element_by_class_name("shopee-searchbar-input__input")
    search_item.send_keys(keyword)
    search_item.send_keys(Keys.ENTER)
    time.sleep(2)

    for i in range(10):
        y_position = i * 100
        driver.execute_script(f"window.scrollTo(0, {y_position});")
        time.sleep(0.1)

    # 輸入價格區間
    priceMin = driver.find_element_by_css_selector(
        ".shopee-price-range-filter__inputs>input:nth-child(1)"
    )
    priceMax = driver.find_element_by_css_selector(
        ".shopee-price-range-filter__inputs>input:nth-child(3)"
    )
    applyBtn = driver.find_element_by_css_selector(
        ".shopee-button-solid.shopee-button-solid--primary._1-VOCH"
    )
    priceMin.send_keys(minP)
    priceMax.send_keys(maxP)
    applyBtn.click()
    driver.refresh()
    time.sleep(2)

    for i in range(10):
        y_position = i * 100
        driver.execute_script(f"window.scrollTo(0, {y_position});")
        time.sleep(0.1)

    # 廣告
    adsCheck = driver.find_elements_by_css_selector("._25_r8I.ggJllv>.LvWDWe>._1p-nLd")
    ads = len(adsCheck)

    itemUrllist = []
    itemUrl = driver.find_elements_by_css_selector(
        ".col-xs-2-4.shopee-search-item-result__item>a"
    )
    for num in range(ads, 10):
        # print(url.get_attribute('href'))
        if itemUrl[num].get_attribute("href") != None:
            itemUrllist.append(
                unquote(itemUrl[num].get_attribute("href"), encoding="utf-8")
            )
    print(itemUrllist)

    # 商品圖片
    itemImagelist = []
    itemImageurl = driver.find_elements_by_css_selector("._3-N5L6._2GchKS")
    for num in range(ads, 10):
        if str(type(itemImageurl[num].get_attribute("src"))) != "<class 'NoneType'>":
            if "_tn" in itemImageurl[num].get_attribute("src"):
                itemImagelist.append(itemImageurl[num].get_attribute("src"))
                print(itemImageurl[num].get_attribute("src"))
    # 商品名稱
    itemTitlelist = []
    itemTitle = driver.find_elements_by_css_selector("._10Wbs-._5SSWfi.UjjMrh")
    for num in range(ads, 10):
        itemTitlelist.append(itemTitle[num].text)
    print(itemTitlelist)
    # 商品價格
    itemPricelist = []
    itemPrice = driver.find_elements_by_css_selector(".zp9xm9.xSxKlK._1heB4J")
    for num in range(ads, 10):
        itemPricelist.append(itemPrice[num].text)
    print(itemPricelist)

    driver.close()

    message = []
    random_code = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(4)
    )
    message.append(
        ImageSendMessage(
            original_content_url=HEROKU_APP_URL + "/static/tmp/test.png?" + random_code,
            preview_image_url=HEROKU_APP_URL + "/static/tmp/test.png?" + random_code,
        )
    )

    message.append(
        item_carousel("搜尋結果", itemImagelist, itemTitlelist, itemPricelist, itemUrllist)
    )
    return message


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

    msg = shopee("貓糧 0 600")
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(USERID, msg)
