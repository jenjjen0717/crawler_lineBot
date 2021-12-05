from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *


def quick_replyCon():
    message = TextSendMessage(
        text="商品狀況",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=PostbackAction(
                        label="new", data="new", display_text="全新")
                ),
                QuickReplyButton(
                    action=PostbackAction(
                        label="used", data="used", display_text="二手")
                ),
            ]
        )
    )
    return message
