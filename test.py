import re
import requests
from bs4 import BeautifulSoup
import json
import urllib

from datetime import datetime, timedelta
import time
from pytz import timezone, utc

DOMAIN = "https://shopee.tw/"
keyword = input()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29',
    'referer': f'https://shopee.tw/search?keyword={urllib.parse.quote(keyword)}',
    'if-none-match-': '55b03-73059b9f12afd4ac0c8880518e91f2c0',

}

path = "test.txt"
f = open(path, 'w', encoding="utf-8")


def getShopeekey(keyword):
    data = {}
    data['search_keyword'] = keyword
    parseAllList(data, keyword)


f1 = open("doc.txt", "w", encoding="utf-8")


def parseAllList(data, keyword):
    ty_url = DOMAIN + \
        'api/v2/search_items/?by=relevancy&keyword={}&limit=50&newest=0&order=desc&page_type=search&version=2'.format(
            keyword)
    resp = requests.get(ty_url, headers=headers).text
    doc = json.loads(resp)
    print(doc, file=f1)

    totalcount = doc['query_rewrite']['ori_totalCount']
    total_pg = (totalcount // 50) + 1
    doc['totalPage'] = total_pg

    for num in range(0, total_pg):
        pg_url = DOMAIN + \
            'api/v2/search_items/?by=sales&conditions=new&keyword={}&limit=100&newest={}&order=desc&page_type=search&price_max=600&rating_filter=4&shippings=2&skip_autocorrect=1&version=2'.format(
                keyword, (num*50))
        data['Page'] = num + 1
        parseList(pg_url, data, num)


def parseList(pg_url, data, num):
    print(pg_url)
    resp = requests.get(pg_url, headers=headers).text
    doc = json.loads(resp)
    position = 0
    count = 0

    for i in doc['items']:
        productid = i['itemid']
        name = i['name']
        shopid = i['shopid']
        data['Brand'] = i['brand']

        data['PrdCode'] = productid
        article_url = DOMAIN + name + '-i.{}.{}'.format(shopid, productid)
        data['url'] = article_url

        promotion = []
        if not i['ads_keyword'] == None:
            promotion.append('廣告')
        if not i['add_on_deal_info'] == None:
            promotion.append(i['add_on_deal_info']['add_on_deal_label'])
        if int(i['show_discount']) > 0:
            promotion.append('折扣')
        if i['service_by_shopee_flag'] == None:
            promotion.append('24h快速到貨')

        if num == 0:
            position = position + 1
        else:
            count = count + 1
            position = (num * 50) + count
        data['position_section'] = position
        data['position_total'] = data['position_section']

        parseItem(shopid, productid, promotion, data)


def parseItem(shopid, productid, promotion, data):
    pg_url = DOMAIN + \
        'api/v2/item/get?itemid={}&shopid={}'.format(productid, shopid)
    resp = requests.get(pg_url, headers=headers).text
    doc = json.loads(resp)

    flavor = 0
    if not len(doc['item']['models']) == 0:
        for i in doc['item']['models']:
            flavor = flavor + 1

    data['Description'] = doc['item']['name']
    data['like'] = doc['item']['liked_count']
    data['rating'] = doc['item']['item_rating']['rating_star']
    data['review_count'] = doc['item']['cmt_count']
    data['sold_unit'] = doc['item']['historical_sold']

    if not doc['item']['bundle_deal_info'] == None:
        promotion.append(doc['item']['bundle_deal_info']['bundle_deal_label'])
    if doc['item']['shopee_verified'] == True:
        promotion.append('蝦皮優選')
    if doc['item']['show_official_shop_label'] == True:
        promotion.append('商城')
    data['promotion_tag'] = promotion

    if doc['item']['is_official_shop'] == True:
        data['subchannel'] = '購物商城'
    if doc['item']['show_free_shipping'] == True:
        data['delivery'] = '免運費'
    else:
        data['delivery'] = '需運費'

    data['Selling_price'] = str(doc['item']['price_max'])[:-5]
    data['List_price'] = str(doc['item']['price_min_before_discount'])[:-5]
    if data['List_price'] == 0:
        data['List_price'] = str(doc['item']['price_max'])[:-5]

    crawler_tm = datetime.now(tz=timezone('Asia/Taipei'))
    data['rtime'] = datetime.strftime(crawler_tm, '%Y-%m-%d %H:%M:%S')

    if not flavor == 0:
        for i in range(0, flavor):
            data['option_flavor'] = doc['item']['models'][(i)]['name']
            data['List_price'] = str(doc['item']['models'][(i)]['price'])[:-5]
            print(data, file=f)
    else:
        data['option_flavor'] = ""
        print(data, file=f)


getShopeekey(keyword)
