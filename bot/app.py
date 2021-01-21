#-*- coding: utf-8 -*-
from flask import Flask, request, abort
import json
import base64
from time import time

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ThingsEvent, ScenarioResult,
)

app = Flask(__name__)
ACCESS_TOKEN = "71ZTbCq+tXWKHuqhv6CPebD9auikhKuc6epLEeJNi/olrF94Af2q+1r55g9zKEYB+KdaPJHId4055Mi5J1SB2jGLaXMyGhyUhdG399Ar6ggNtkj5+cOm4IXE7q84s8oKQz5z9mQ8iAvDGlRl3t4VLQdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "442a5e1c75f7aa7127f53f84e4c0234a"
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
@app.route("/")
def healthcheck():
    return 'OK'
@app.route("/callback", methods=['POST'])
def callback():
    
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'
@handler.add(ThingsEvent)
def handle_things_event(event):
    
    if event.things.type != "scenarioResult":
        return
    if event.things.result.result_code != "success":
        app.logger.warn("Error result: %s", event)
        return
    button_state = int.from_bytes(base64.b64decode(event.things.result.ble_notification_payload), 'little')
    if button_state > 0:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Button is pressed!"))
if __name__ == "__main__":
    app.run(debug=True)