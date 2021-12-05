from lxml import etree
import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

title = []


def search(url):
    res = requests.get(url, headers=headers)
    content = res.content.decode()
    html = etree.HTML(content)
    title.extend(html.xpath(
        '//*[@id="main"]/div/div[3]/div/div[2]/div[2]/div[2]/div[1]/a/@href'))
    return title


def getAllcom(keyword):
    search(f'https://shopee.tw/search?keyword={keyword}')


getAllcom('餅乾')
print(title)
