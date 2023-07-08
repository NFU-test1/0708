from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import random

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == '遊戲開始':
        ans = str(random.randint(1,100))
        min_value = 0
        max_value = 100
        f = open('Myfile.txt','w')
        f.write(f"{ans} {min_value} {max_value}")
        f.close()
        msg = f'請輸入介於{min_value}到{max_value}的數字'
    else:
        f = open('Myfile.txt','r')
        file = f.read()
        ans,min_value,max_value = map(int,file.split())
        f = open('Myfile.txt','w')
        msg = int(msg)
        if msg == ans:
            ans = str(random.randint(1,100))
            min_value = 0
            max_value = 100
            f.write(f"{ans} {min_value} {max_value}")
            msg = "恭喜你 答對了！\n你真是太厲害了！"
        elif max_value > msg > ans:
            max_value = msg
            f.write(f"{ans} {min_value} {max_value}")
            msg = f'請輸入介於{min_value}到{max_value}的數字'
        elif min_value < msg < ans:
            min_value = msg
            f.write(f"{ans} {min_value} {max_value}")
            msg = f'請輸入介於{min_value}到{max_value}的數字'
        else:
            f.write(f"{ans} {min_value} {max_value}")
            msg = f'請輸入介於{min_value}到{max_value}的數字'
        f.close()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


if __name__ == "__main__":
    app.run()