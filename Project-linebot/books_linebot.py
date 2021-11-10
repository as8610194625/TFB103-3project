# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextSendMessage,CarouselTemplate,CarouselColumn,StickerSendMessage,LocationSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,URITemplateAction,PostbackTemplateAction, events
from linebot.models.messages import ImageMessage,TextMessage
import time
import json

from linebot.models.responses import Content
import python_mongodb_stored as mongo
from pymongo import MongoClient, collection
import random
from elastic import random_find
# create flask server
# hotbooks = 1
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
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     # get user info & message
#     user_id = event.source.user_id
#     msg = event.message.text
#     user_name = line_bot_api.get_profile(user_id).display_name
#     line_bot_api.reply_message(event.reply_token, 
#                                 [TextSendMessage(text = '本機自動回覆'),
#                                 StickerSendMessage(package_id='6325',sticker_id='10979908')])
    
#     # push text_msg
#     line_bot_api.push_message(user_id,
#                                 TextSendMessage(text = '您好^^'))
#     # get msg details
#     print('msg from [', user_name, '](', user_id, ') : ', msg)
#     storedID = {'_id':user_id,'userName':user_name,'Log':msg}
#     # mongo.kingstone_stored(storedID)
contents = 1
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if message == '@個性查詢':
        # line_bot_api.reply_message(event.reply_token,
        #                     [TextSendMessage(text = ''.join(hot_randome()[0]))])
        # line_bot_api.push_message(event.reply_token,
        #                     [TextSendMessage(text = ''.join(hot_randome()[1]))])
        sendButton(event)
    elif message == '@直接查詢':
        sendCarousel(event)
    elif message == '@我的最愛':
        c = 1
    # elif message == '@簡介':
    #     line_bot_api.reply_message(event.reply_token,
    #                         [TextSendMessage(text = contents)])

def sendButton(event):  #按鈕樣版
    connection = MongoClient(host='localhost',port=27017)
    db = connection.kingstone
    collection = db['test']
    allbooks = list(collection.find())
    chooseone = random.choice(allbooks)
    # choosebooks = random.sample(allbooks,2)
    # hot.append(choosebooks)
    imageurl = chooseone['圖片網址']
    book = chooseone['書名']
    url = chooseone['書籍網站']
    isbn = chooseone['ISBN']
    # global contents
    contents = chooseone['書籍簡介']
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url=imageurl,  #顯示的圖片
                title=book,  #主標題
                text=isbn,  #副標題
                actions=[
                    MessageTemplateAction(  #顯示文字計息
                        label='簡介',
                        text= contents
                    ),
                    URITemplateAction(  #開啟網頁
                        label='連結網頁',
                        uri=url
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='回傳訊息',  #按鈕文字
                        # text='@購買披薩',  #顯示文字訊息
                        data='action=buy'  #Postback資料
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendCarousel(event):  #轉盤樣板
    time.sleep(1)
    books = random_find()
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=books[0]['_source']['圖片網址'],
                        title=books[0]['_source']['書名'],
                        text=books[0]['_source']['ISBN'],
                        actions=[
                            MessageTemplateAction(
                                label='簡介',
                                text=books[0]['_source']['書籍簡介']
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri=books[0]['_source']['書籍網站']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=books[1]['_source']['圖片網址'],
                        title=books[1]['_source']['書名'],
                        text=books[1]['_source']['ISBN'],
                        actions=[
                            MessageTemplateAction(
                                label='簡介',
                                text=books[1]['_source']['書籍簡介']
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri=books[1]['_source']['書籍網站']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=books[2]['_source']['圖片網址'],
                        title=books[2]['_source']['書名'],
                        text=books[2]['_source']['ISBN'],
                        actions=[
                            MessageTemplateAction(
                                label='簡介',
                                text=books[2]['_source']['書籍簡介']
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri=books[2]['_source']['書籍網站']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=books[3]['_source']['圖片網址'],
                        title=books[3]['_source']['書名'],
                        text=books[3]['_source']['ISBN'],
                        actions=[
                            MessageTemplateAction(
                                label='簡介',
                                text=books[3]['_source']['書籍簡介']
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri=books[3]['_source']['書籍網站']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=books[4]['_source']['圖片網址'],
                        title=books[4]['_source']['書名'],
                        text=books[4]['_source']['ISBN'],
                        actions=[
                            MessageTemplateAction(
                                label='簡介',
                                text=books[4]['_source']['書籍簡介']
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri=books[4]['_source']['書籍網站']
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
# def sendCarousel(event):  #轉盤樣板
#     time.sleep(0.5)
#     connection = MongoClient(host='localhost',port=27017)
#     db = connection.kingstone
#     collection = db['test']
#     allbooks = list(collection.find())
#     choosebooks = random.sample(allbooks,6)
#     try:
#         message = TemplateSendMessage(
#             alt_text='轉盤樣板',
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url=choosebooks[0]['圖片網址'],
#                         title=choosebooks[0]['書名'],
#                         text=choosebooks[0]['ISBN'],
#                         actions=[
#                             MessageTemplateAction(
#                                 label='簡介',
#                                 text=choosebooks[0]['書籍簡介']
#                             ),
#                             URITemplateAction(
#                                 label='連結網頁',
#                                 uri=choosebooks[0]['書籍網站']
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url=choosebooks[1]['圖片網址'],
#                         title=choosebooks[1]['書名'],
#                         text=choosebooks[1]['ISBN'],
#                         actions=[
#                             MessageTemplateAction(
#                                 label='簡介',
#                                 text=choosebooks[1]['書籍簡介']
#                             ),
#                             URITemplateAction(
#                                 label='連結網頁',
#                                 uri=choosebooks[1]['書籍網站']
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url=choosebooks[2]['圖片網址'],
#                         title=choosebooks[2]['書名'],
#                         text=choosebooks[2]['ISBN'],
#                         actions=[
#                             MessageTemplateAction(
#                                 label='簡介',
#                                 text=choosebooks[2]['書籍簡介']
#                             ),
#                             URITemplateAction(
#                                 label='連結網頁',
#                                 uri=choosebooks[2]['書籍網站']
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url=choosebooks[3]['圖片網址'],
#                         title=choosebooks[3]['書名'],
#                         text=choosebooks[3]['ISBN'],
#                         actions=[
#                             MessageTemplateAction(
#                                 label='簡介',
#                                 text=choosebooks[3]['書籍簡介']
#                             ),
#                             URITemplateAction(
#                                 label='連結網頁',
#                                 uri=choosebooks[3]['書籍網站']
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url=choosebooks[4]['圖片網址'],
#                         title=choosebooks[4]['書名'],
#                         text=choosebooks[4]['ISBN'],
#                         actions=[
#                             MessageTemplateAction(
#                                 label='簡介',
#                                 text=choosebooks[4]['書籍簡介']
#                             ),
#                             URITemplateAction(
#                                 label='連結網頁',
#                                 uri=choosebooks[4]['書籍網站']
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url=choosebooks[5]['圖片網址'],
#                         title=choosebooks[5]['書名'],
#                         text=choosebooks[5]['ISBN'],
#                         actions=[
#                             MessageTemplateAction(
#                                 label='簡介',
#                                 text=choosebooks[5]['書籍簡介']
#                             ),
#                             URITemplateAction(
#                                 label='連結網頁',
#                                 uri=choosebooks[5]['書籍網站']
#                             )
#                         ]
#                     )
#                 ]
#             )
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

# run app
if __name__ == "__main__":
    app.run(host='localhost',debug=True, port=12345)
