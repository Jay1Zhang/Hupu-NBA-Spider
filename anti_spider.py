import time
import random
from selenium import webdriver
from urllib.request import urlopen

import config


# 获取html源码
def get_html(url):
    if config.use_selenium:
        driver = webdriver.Firefox()    # 打开浏览器
        driver.get(url)     # 打开网页 - 知乎关键词检索后的网页
        sleep_random(max_time=1)
        html = driver.page_source  # get html
        #driver.close()
    else:
        html = urlopen(url)
        sleep_random(max_time=1)

    return html


def sleep_random(max_time):
    sleep_time = round(max_time * random.random(), 4)
    time.sleep(sleep_time)

