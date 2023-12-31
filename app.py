"""
Created on 2021/10/27

@author: janef
"""
from linebot.models import *
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask import request, abort
from flask import Flask
from liffpy import LineFrontendFramework as LIFF, ErrorResponse

import tempfile
import os

from config import *
from shopee import *
from shopee_item import *

liff_api = LIFF(CHANNEL_ACCESS_TOKEN)

app = Flask(__name__, template_folder="templates")
static_tmp_path = os.path.join(os.path.dirname(__file__), "static", "tmp")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        msg = event.message.text
        message = shopee(msg)
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    message = shopee_option(data)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
