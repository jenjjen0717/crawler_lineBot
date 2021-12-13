from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from linebot.models import *

from config import *

import time
import random
import string


def shopeeTest():

    domain = "https://shopee.tw/"
    """
    # 建立chrome設定
    chromeOption = webdriver.ChromeOptions()
    # 設定瀏覽器的語言為utf-8中文
    chromeOption.add_argument("--lang=zh-CN.UTF8")
    # 設定瀏覽器的user agent
    chromeOption.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
    """
    driver = webdriver.Chrome()
    driver.set_window_size(1024, 960)

    driver.get(domain)
    time.sleep(5)

    image_path = "./static/tmp/test2.png"
    driver.refresh()
    time.sleep(10)
    driver.save_screenshot(image_path)

    action = ActionChains(driver)
    action.move_by_offset(930, 70).click().perform()

    image_path = "./static/tmp/test4.png"
    driver.refresh()
    time.sleep(10)
    driver.save_screenshot(image_path)

    driver.close()

    message = []

    # 瀏覽器螢幕截圖
    # 建立一個隨機4碼的字串，使圖片縮圖瀏覽不會因為讀取同一個url快取而重覆
    random_code = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(4)
    )
    message.append(
        ImageSendMessage(
            original_content_url=HEROKU_APP_URL
            + "/static/tmp/test2.png?"
            + random_code,
            preview_image_url=HEROKU_APP_URL + "/static/tmp/test2.png?" + random_code,
        )
    )
    message.append(
        ImageSendMessage(
            original_content_url=HEROKU_APP_URL
            + "/static/tmp/test4.png?"
            + random_code,
            preview_image_url=HEROKU_APP_URL + "/static/tmp/test4.png?" + random_code,
        )
    )

    return message


if __name__ == "__main__":
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import *

    msg = shopeeTest()
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(USERID, msg)
