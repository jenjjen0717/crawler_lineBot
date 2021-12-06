from linebot.models import *
from config import *
# 使用quote進行中文轉碼
from urllib.parse import quote


def item_carousel(alt_text, itemImagelist, itemTitlelist, itemPricelist, itemUrllist):
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    i = 0
    for imageUrl, itemTitle, itemPrice, itemUrl in zip(itemImagelist, itemTitlelist, itemPricelist, itemUrllist):
        if i < 5:
            bubble = {"type": "bubble",
                      "hero": {
                          "type": "image",
                          "url": imageUrl,
                          "size": "full",
                          "aspectRatio": "20:13",
                          "aspectMode": "fit"
                      },
                      "body": {
                          "type": "box",
                          "layout": "vertical",
                          "spacing": "sm",
                          "contents": [
                                    {
                                        "type": "text",
                                        "text": itemTitle,
                                        "weight": "bold",
                                        "size": "xl",
                                        "wrap": False,
                                        "contents": []
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
                                                "contents": []
                                            }
                                        ]
                                    }
                          ]
                      },
                      "footer": {
                          "type": "box",
                          "layout": "vertical",
                          "spacing": "sm",
                          "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "uri",
                                            "label": "查看",
                                            "uri": itemUrl
                                        },
                                        "style": "primary"
                                    }
                          ]
                      }
                      }
            contents['contents'].append(bubble)
            i += 1
    message = FlexSendMessage(alt_text=alt_text, contents=contents)
    return message
