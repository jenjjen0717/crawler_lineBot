'''
Created on 2021/10/27

@author: janef
'''
from linebot.models import *
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask import request, abort
from flask import Flask

import tempfile
import os

from message import *

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
line_bot_api = LineBotApi(
    'JSbhommMXXm7pKKEuh39wpG7jIRfUlIYeFJ5rSGVl5JmidKgfChl9YT88P58hxFrDdzk/Gho3/9xH7eYGqhDvunICTg0xVPhl6EumgGpUyeylC8t/JvDIWdDVp9aFcDev4rYqmIGjdih4tynMX6hNgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('479d40465262d442c52077b32933ff9a')


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(PostbackEvent)
def handle_postback(event):
    ts = event.postback.data
    if ts == "new":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='全新'))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='二手'))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        quick_replyCon())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
