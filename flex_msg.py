from linebot.models import *
from config import *

# 使用quote進行中文轉碼
from urllib.parse import unquote


def item_carousel(alt_text, itemImagelist, itemTitlelist, itemPricelist, itemUrllist):
    contents = dict()
    contents["type"] = "carousel"
    contents["contents"] = []
    i = 0
    for imageUrl, itemTitle, itemPrice, itemUrl in zip(
        itemImagelist, itemTitlelist, itemPricelist, itemUrllist
    ):
        if i < 5:
            bubble = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": imageUrl + "?",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "fit",
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": itemTitle[:30]
                            if len(itemTitle) < 30
                            else itemTitle[:30] + "...",
                            "weight": "bold",
                            "size": "xl",
                            "wrap": False,
                            "contents": [],
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": itemPrice,
                                    "weight": "bold",
                                    "size": "xl",
                                    "flex": 0,
                                    "wrap": True,
                                    "contents": [],
                                }
                            ],
                        },
                    ],
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "查看",
                                "data": itemUrl,
                            },
                        }
                    ],
                },
            }
            contents["contents"].append(bubble)
            i += 1
    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "See more",
                        "data": "see more",
                    },
                    "flex": 1,
                    "gravity": "center",
                }
            ],
        },
    }
    contents["contents"].append(bubble)
    message = FlexSendMessage(alt_text=alt_text, contents=contents)
    return message
