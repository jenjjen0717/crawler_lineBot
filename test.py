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


def shopee_1():

    """
    chromeOption = webdriver.ChromeOptions()
    chromeOption.add_argument("--lang=zh-CN.UTF8")
    # 設定瀏覽器的user agent
    chromeOption.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    )
    """

    domain = "https://shopee.tw/"

    driver = webdriver.Chrome()
    driver.set_window_size(1200, 960)

    driver.get(domain)
    time.sleep(1)

    image_path = "./static/tmp/test.png"
    driver.save_screenshot(image_path)
    time.sleep(2)

    driver.close()

    random_code = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(4)
    )
    message = ImageSendMessage(
        original_content_url=HEROKU_APP_URL + "/static/tmp/test.png?" + random_code,
        preview_image_url=HEROKU_APP_URL + "/static/tmp/test.png?" + random_code,
    )
    return message
