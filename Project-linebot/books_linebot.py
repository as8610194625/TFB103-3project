# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextSendMessage,StickerSendMessage,LocationSendMessage
from linebot.models.messages import ImageMessage,TextMessage
import time
import json
import python_mongodb_stored as mongo
# create flask server
app = Flask(__name__)

secretFile=json.load(open("secretFile.txt",'r'))
channelAccessToken=secretFile['channelAccessToken']
channelSecret=secretFile["channelSecret"]

line_bot_api =LineBotApi(channelAccessToken)
handler=WebhookHandler(channelSecret)


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
    # get user info & message
    user_id = event.source.user_id
    msg = event.message.text
    user_name = line_bot_api.get_profile(user_id).display_name
    line_bot_api.reply_message(event.reply_token, 
                               [TextSendMessage(text = '本機自動回覆'),
                                StickerSendMessage(package_id='6325',sticker_id='10979908')])
    
    # push text_msg
    line_bot_api.push_message(user_id,
                              TextSendMessage(text = '您好^^'))
    # get msg details
    print('msg from [', user_name, '](', user_id, ') : ', msg)
    storedID = {'_id':user_id,'userName':user_name,'Log':msg}
    mongo.kingstone_stored(storedID)

# @handler.add(MessageEvent, message=TextMessage)
# def handle(event):
    # message = event.message.text
    # if message == @A:
    #     .....

# run app
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=12345)
