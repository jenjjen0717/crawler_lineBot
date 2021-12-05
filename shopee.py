import re
import requests
from bs4 import BeautifulSoup
import json
import urllib

from app import handle_postback

DOMAIN = "https://shopee.tw/"
keyword = input()
price_max = input()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29',
    'referer': f'https://shopee.tw/search?keyword={urllib.parse.quote(keyword)}',
    'if-none-match-': '55b03-73059b9f12afd4ac0c8880518e91f2c0',
}


def get_keyword(keyword):
    data = {}
    get_allList(data, keyword)


f1 = open("shopee.txt", "w", encoding="utf-8")
f2 = open("shopeeItem.txt", "w", encoding="utf-8")


def get_allList(data, keyword):
    search_url = DOMAIN + \
        f"api/v2/search_items/?by=relevancy&keyword={keyword}&limit=50&newest=0&order=desc&page_type=search&version=2"
    r = requests.get(search_url, headers=headers).text
    getList = json.loads(r)
    print(getList, file=f1)

    page_url = DOMAIN + \
        f"api/v2/search_items/?by=sales&conditions={conditions}&keyword={keyword}&limit=10&newest=0&order=desc&page_type=search&price_max={price_max}&version=2"
    get_list(page_url, data)


def get_list(page_url, data):
    r = requests.get(page_url, headers=headers).text
    getList = json.loads(r)

    for i in getList['items']:
        productid = i['itemid']
        name = i['name']
        shopid = i['shopid']
        data['Brand'] = i['brand']

        data['PrdCode'] = productid
        article_url = DOMAIN + name + '-i.{}.{}'.format(shopid, productid)
        data['url'] = article_url

        promotion = []
        if not i['ads_keyword'] == None:
            continue
        if not i['add_on_deal_info'] == None:
            promotion.append(i['add_on_deal_info']['add_on_deal_label'])
        if int(i['show_discount']) > 0:
            promotion.append('折扣')
        if i['service_by_shopee_flag'] == None:
            promotion.append('24h快速到貨')

        get_item(shopid, productid, promotion, data)


def get_item(shopid, productid, promotion, data):
    item_url = DOMAIN + \
        'api/v2/item/get?itemid={}&shopid={}'.format(productid, shopid)
    r = requests.get(item_url, headers=headers).text
    getList = json.loads(r)

    flavor = 0
    if not len(getList['item']['models']) == 0:
        for i in getList['item']['models']:
            flavor = flavor + 1

    data['Description'] = getList['item']['name']
    data['like'] = getList['item']['liked_count']
    data['rating'] = getList['item']['item_rating']['rating_star']
    data['review_count'] = getList['item']['cmt_count']
    data['sold_unit'] = getList['item']['historical_sold']

    if not getList['item']['bundle_deal_info'] == None:
        promotion.append(
            getList['item']['bundle_deal_info']['bundle_deal_label'])
    if getList['item']['shopee_verified'] == True:
        promotion.append('蝦皮優選')
    if getList['item']['show_official_shop_label'] == True:
        promotion.append('商城')
    data['promotion_tag'] = promotion

    if getList['item']['is_official_shop'] == True:
        data['subchannel'] = '購物商城'
    if getList['item']['show_free_shipping'] == True:
        data['delivery'] = '免運費'
    else:
        data['delivery'] = '需運費'

    data['Selling_price'] = str(getList['item']['price_max'])[:-5]
    data['List_price'] = str(getList['item']['price_min_before_discount'])[:-5]
    if data['List_price'] == 0:
        data['List_price'] = str(getList['item']['price_max'])[:-5]

    if not flavor == 0:
        for i in range(0, flavor):
            data['option_flavor'] = getList['item']['models'][(i)]['name']
            data['List_price'] = str(
                getList['item']['models'][(i)]['price'])[:-5]
            print(data, file=f2)
    else:
        data['option_flavor'] = ""
        print(data, file=f2)


get_keyword(keyword)
