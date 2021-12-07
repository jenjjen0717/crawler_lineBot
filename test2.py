from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from linebot.models import *

from flex_msg import *
from config import *

import time


def shopee(keyword, minP, maxP):

    domain = "https://shopee.tw/"

    driver = webdriver.Chrome()
    driver.set_window_size(1024, 960)

    driver.get(domain)

    action = ActionChains(driver)
    action.move_by_offset(930, 200).click().perform()

    search_item = driver.find_element_by_class_name(
        "shopee-searchbar-input__input")
    search_item.send_keys(keyword)
    time.sleep(1)

    search_button = driver.find_element_by_class_name(
        "shopee-searchbar__search-button")
    search_button.click()
    driver.refresh()
    time.sleep(2)

    priceMin = driver.find_element_by_css_selector(
        ".shopee-price-range-filter__inputs>input:nth-child(1)")
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

    adsCheck = driver.find_elements_by_css_selector(
        "._25_r8I.ggJllv>.LvWDWe>._1p-nLd")
    ads = len(adsCheck)

    itemUrllist = []
    itemUrl = driver.find_elements_by_css_selector(
        '.col-xs-2-4.shopee-search-item-result__item>a'
    )
    for num in range(ads, 10):
        # print(url.get_attribute('href'))
        if itemUrl[num].get_attribute('href') != None:
            itemUrllist.append(itemUrl[num].get_attribute('href'))
    print(itemUrllist)

    for i in range(50):
        y_position = i*100
        driver.execute_script(f'window.scrollTo(0, {y_position});')
        time.sleep(0.1)

    itemImagelist = []
    itemImageurl = driver.find_elements_by_css_selector("._3-N5L6._2GchKS")
    for num in range(ads, 10):
        if str(type(itemImageurl[num].get_attribute('src'))) != "<class 'NoneType'>":
            if '_tn' in itemImageurl[num].get_attribute('src'):
                itemImagelist.append(itemImageurl[num].get_attribute('src'))
                print(itemImageurl[num].get_attribute('src'))

    itemTitlelist = []
    itemTitle = driver.find_elements_by_css_selector("._10Wbs-._5SSWfi.UjjMrh")
    for num in range(ads, 10):
        itemTitlelist.append(itemTitle[num].text)
    print(itemTitlelist)

    itemPricelist = []
    itemPrice = driver.find_elements_by_css_selector(
        ".zp9xm9.xSxKlK._1heB4J")
    for num in range(ads, 10):
        itemPricelist.append(itemPrice[num].text)
    print(itemPricelist)

    driver.close()

    message = item_carousel("搜尋結果", itemImagelist,
                            itemTitlelist, itemPricelist, itemUrllist)
    return message


if __name__ == '__main__':
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import *
    msg = shopee('貓糧', '0', '600')
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(USERID, msg)
