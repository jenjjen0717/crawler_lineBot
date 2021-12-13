from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *


def itemOption_carousel(alt_text, itemUrl, titleList, priceList, stockStat):
    contents = dict()
    contents["type"] = "carousel"
    contents["contents"] = []
    i = 0
    for optionTitle, optionPrice, status in zip(titleList, priceList, stockStat):
        if i < len(optionTitle):
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "action": {"type": "uri", "uri": itemUrl},
                    "contents": [
                        {
                            "type": "text",
                            "text": optionTitle[:30]
                            if len(optionTitle) < 30
                            else optionTitle[:30] + "...",
                            "weight": "bold",
                            "size": "xl",
                            "wrap": True,
                            "contents": [],
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "flex": 1,
                            "contents": [
                                {
                                    "type": "text",
                                    "text": optionPrice,
                                    "weight": "bold",
                                    "size": "xl",
                                    "flex": 0,
                                    "wrap": True,
                                    "contents": [],
                                }
                            ],
                        },
                        {
                            "type": "text",
                            "text": status,
                            "size": "xxs",
                            "color": "#FF5551",
                            "flex": 0,
                            "margin": "md",
                            "wrap": True,
                            "contents": [],
                        },
                    ],
                },
            }
            contents["contents"].append(bubble)
            i += 1
    message = FlexSendMessage(alt_text=alt_text, contents=contents)
    return message
