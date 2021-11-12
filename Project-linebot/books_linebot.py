# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent,TextSendMessage,CarouselTemplate,CarouselColumn,PostbackEvent,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,URITemplateAction,PostbackTemplateAction, events
from linebot.models.messages import ImageMessage,TextMessage
import time
import json
from elasticsearch import Elasticsearch
from linebot.models.responses import Content
import numpy as np
import python_mongodb_stored as mongo
from pymongo import MongoClient, collection
import random
from elastic import random_find,find_bookisbn,choosebooks
from hot_random import findyoumaybelike
# create flask server
# hotbooks = 1
app = Flask(__name__)

secretFile=json.load(open("secretFile.json",'r'))
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
    elif message[0:1] == '#':
        isbn_list = findyoumaybelike(message[2:])
        you_maybe_like_function(event,isbn_list)
def sendButton(event):  #按鈕樣版
    es = Elasticsearch(hosts='10.2.14.10', port=9200)
    seed = int(time.time())
    res = es.search(index="cleanbook_test", query={"function_score":{"random_score":{"seed":seed,"field":"_seq_no"}},"size":1})
    for chooseone in res['hits']['hits']:
        chooseone = chooseone['_source']
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
    # f = open (r"C:\Users\Tibame\Desktop\TFB103-3project\Project-linebot\recommand_youmaybelike.json","r",encoding="utf-8")
    # like_dict = json.loads(f.read())
    # random_books = random.sample(set(like_dict.keys()),5)
    # random_books = random_find()
    # books = list(map(lambda x:you_maybe_like(x),random_books))
    books = choosebooks()
    books = np.ndarray.tolist(books)
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=books[0]['圖片網址'],
                        title=books[0]['書名'],
                        text=books[0]['ISBN'],
                        actions=[
                            MessageTemplateAction(
                                label='簡介',
                                # text=books[0]['書籍簡介']
                                text='...'
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri=books[0]['書籍網站']
                            ),
                            PostbackTemplateAction(
                                label='您可能喜歡....',
                                text='#'+books[0]['ISBN'],
                                data='#A&查詢中'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=books[1]['圖片網址'],
                        title=books[1]['書名'],
                        text=books[1]['ISBN'],
                        actions=[
                            MessageTemplateAction(
                                label='簡介',
                                # text=books[1]['書籍簡介']
                                text='...'
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri=books[1]['書籍網站']
                            ),
                            PostbackTemplateAction(
                                label='您可能喜歡....',
                                text='#'+books[1]['ISBN'],
                                data='B&查詢中'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=books[2]['圖片網址'],
                        title=books[2]['書名'],
                        text=books[2]['ISBN'],
                        actions=[
                            MessageTemplateAction(
                                label='簡介',
                                # text=books[2]['書籍簡介']
                                text='...'
                            ),
                            URITemplateAction(
                                label='連結網頁',
                                uri=books[2]['書籍網站']
                            ),
                            PostbackTemplateAction(
                                label='您可能喜歡....',
                                text='#'+books[2]['ISBN'],
                                data='C&查詢中'
                            )
                        ]
                    ),
                    # CarouselColumn(
                    #     thumbnail_image_url=books[3]['圖片網址'],
                    #     title=books[3]['書名'],
                    #     text=books[3]['ISBN'],
                    #     actions=[
                    #         MessageTemplateAction(
                    #             label='簡介',
                    #             # text=books[3]['書籍簡介']
                    #             text='...'
                    #         ),
                    #         URITemplateAction(
                    #             label='連結網頁',
                    #             uri=books[3]['書籍網站']
                    #         )
                    #     ]
                    # ),
                    # CarouselColumn(
                    #     thumbnail_image_url=books[4]['圖片網址'],
                    #     title=books[4]['書名'],
                    #     text=books[4]['ISBN'],
                    #     actions=[
                    #         MessageTemplateAction(
                    #             label='簡介',
                    #             # text=books[4]['書籍簡介']
                    #             text='...'
                    #         ),
                    #         URITemplateAction(
                    #             label='連結網頁',
                    #             uri=books[4]['書籍網站']
                    #         )
                    #     ]
                    # )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
        # if isinstance(event,PostbackEvent):
        #     if event.postback.data[0:1] == 'A':
        #         other_books = findyoumaybelike(books[0]['ISBN'])
        #         try:
        #             you_maybe_like_function(other_books)
        #         except:
        #             line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        #             print(LineBotApiError)
        #     elif event.postback.data[0:1] == 'B':
        #         other_books = findyoumaybelike(books[1]['ISBN'])
        #         try:
        #             you_maybe_like_function(other_books)
        #         except:
        #             line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        #             print(LineBotApiError)
        #     elif event.postback.data[0:1] == 'C':
        #         other_books = findyoumaybelike(books[2]['ISBN'])
        #         try:
        #             you_maybe_like_function(other_books)
        #         except:
        #             line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        #             print(LineBotApiError)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        print(LineBotApiError)
        # print('.........')
def you_maybe_like_function(event,isbn_list):  #轉盤樣板
    # books_list = findyoumaybelike(isbn)
    books = list(map(find_bookisbn,isbn_list))
    message = TemplateSendMessage(
        alt_text='轉盤樣板',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=books[0]['圖片網址'],
                    title=books[0]['書名'],
                    text=books[0]['ISBN'],
                    actions=[
                        MessageTemplateAction(
                            label='簡介',
                            # text=books[0]['書籍簡介']
                            text='...'
                        ),
                        URITemplateAction(
                            label='連結網頁',
                            uri=books[0]['書籍網站']
                        ),
                        MessageTemplateAction(
                            label='您可能喜歡....',
                            text='#'+books[0]['ISBN'],
                            # data='C&查詢中'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=books[1]['圖片網址'],
                    title=books[1]['書名'],
                    text=books[1]['ISBN'],
                    actions=[
                        MessageTemplateAction(
                            label='簡介',
                            # text=books[1]['書籍簡介']
                            text='...'
                        ),
                        URITemplateAction(
                            label='連結網頁',
                            uri=books[1]['書籍網站']
                        ),
                        MessageTemplateAction(
                            label='您可能喜歡....',
                            text='#'+books[1]['ISBN'],
                            # data='C&查詢中'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=books[2]['圖片網址'],
                    title=books[2]['書名'],
                    text=books[2]['ISBN'],
                    actions=[
                        MessageTemplateAction(
                            label='簡介',
                            # text=books[2]['書籍簡介']
                            text='...'
                        ),
                        URITemplateAction(
                            label='連結網頁',
                            uri=books[2]['書籍網站']
                        ),
                        MessageTemplateAction(
                            label='您可能喜歡....',
                            text='#'+books[2]['ISBN'],
                            # data='C&查詢中'
                        )
                    ]
                )
            ]
        )
    )
# run app
if __name__ == "__main__":
    app.run(host='localhost',debug=True, port=12345)
