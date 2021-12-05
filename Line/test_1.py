'''
Created on 2021/10/31

@author: janef
'''
import requests
import lxml.html

etree = lxml.html.etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

title = []

def search(url):
    res = requests.get(url, headers=headers)
    content = res.content.decode()
    html = etree.HTML(content)
    title.extend(html.xpath('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[1]/a/@href'))
    return ()


def getAllcom(keyword):
    search(f'https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword={keyword}&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2')


getAllcom('餅乾')
print(title)