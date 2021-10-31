'''
Created on 2021/10/27

@author: janef
'''
from linebot.models import *
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask import request, abort
from flask import Flask
app = Flask(__name__)


line_bot_api = LineBotApi(
    'pH1H8K7+HLxnyH8+1V4593fRaZ5w4os8qiFBxc9NEGP5LRI/hYETTD5Z1WYW64SEDdzk/Gho3/9xH7eYGqhDvunICTg0xVPhl6EumgGpUycshwQ1fUUwG+io+K/uTdAnYg/5XRvTsWocIYlbxWNMWAdB04t89/1O/w1cDnyilFU=')
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text))


if __name__ == '__main__':
    app.run()
