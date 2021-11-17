# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent,TextSendMessage,CarouselTemplate,CarouselColumn,ImageSendMessage,PostbackEvent,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,URITemplateAction,PostbackTemplateAction, events
from linebot.models.messages import ImageMessage,TextMessage
import time
import json
from elasticsearch import Elasticsearch
from linebot.models.responses import Content
from linebot.models.template import ConfirmTemplate
import numpy as np
from pymongo import MongoClient, collection
from pymongo.errors import DuplicateKeyError
import random

# create flask server

app = Flask(__name__)

secretFile=json.load(open("secretFile.json",'r'))
channelAccessToken=secretFile['channelAccessToken']
channelSecret=secretFile["channelSecret"]
ip = secretFile["IP"]
line_bot_api =LineBotApi(channelAccessToken)
handler=WebhookHandler(channelSecret)

def mongo_user_stored(self):
    connection = MongoClient(host=ip,port=27017)
    db = connection.kingstone
    collection = db['customers']
    try:
        collection.insert([self])
        print('已新增',self['_id'])
        print("----------")
    except DuplicateKeyError:
        collection.update({ '_id' : self['_id'] },{ '$push': { 'tag': self['tag'][0] }})
        print("----------")
    except:
        print('已存在_id',self['_id'],'(因此不寫入)')
        print("----------")

def findbook_ISBN(self):
    es = Elasticsearch(hosts=ip, port=9200)
    res = es.search(index="cleanbook_test", query={"match":{"ISBN":self}})
    # print(res['hits']['hits'])
    # book = res['hits']['hits'][0]["_source"]
    for hit in res['hits']['hits']:
        # global book_all
        book_all = hit["_source"]
        book_all.pop('書籍簡介')
    return book_all
def findbook_Name(self):
    es = Elasticsearch(hosts=ip, port=9200)
    res = es.search(index="cleanbook_test", size=10,query={"match":{"書名":self}})
    
    # print(res)
    books = []
    for i,hit in enumerate(res['hits']['hits']):
        book = hit["_source"]
        book.pop('書籍簡介')
        books.append(book)
    return books
def findbook_Intro(self):
    es = Elasticsearch(hosts=ip, port=9200)
    res = es.search(index="cleanbook_test", size=10,query={"match":{"書籍簡介":self}})

    # print(res)
    books = []
    for i,hit in enumerate(res['hits']['hits']):
        book = hit["_source"]
        book.pop('書籍簡介')
        books.append(book)
        # print(i,book)
    return books
def findbook_Author(self):
    es = Elasticsearch(hosts=ip, port=9200)
    res = es.search(index="cleanbook_test", size=10,query={"match":{"作者":{"query":self,"fuzziness":"AUTO"}}})

    # print(res)
    books = []
    for i,hit in enumerate(res['hits']['hits']):
        book = hit["_source"]
        book.pop('書籍簡介')
        books.append(book)
        # print(i,book)
    return books
def random_choosebookISBN():  #按鈕樣版
    connection = MongoClient(host=ip,port=27017)
    db = connection.kingstone
    collection = db['hotbook']
    # allbooks = list(collection.find())
    chooseisbn = list(collection.aggregate([{'$project':{'_id':0,'ISBN':1}},{'$sample':{'size':3}}]))
    # chooseisbn[0] = chooseisbn[0]['ISBN']
    return [chooseisbn[0]['ISBN'],chooseisbn[1]['ISBN'],chooseisbn[2]['ISBN']]

def findyoumaybelike_ISBN(self):  #轉盤樣板
    connection = MongoClient(host=ip,port=27017)
    db = connection.kingstone
    collection = db['userCF']
    data = collection.find({'ISBN':self})
    datas = list(data)[0]['list']
    return datas

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
    message = event.message.text
    if message == '@暢銷榜推薦':
        sendCarousel(event)
    elif message == '@使用說明':
        instruction(event)
    elif message == '@歷史紀錄':
        history(event)
        
    elif message == '@團隊介紹':
        team_introduction(event)
    elif message == '@聯絡我們':
        team_email(event)
    elif message[0:1] == '$':
        sendButton(event)
    elif message[0:1] == '&':
        UseAuthor(event,message)
    elif message[0:1] == '#':
        Usebookintro(event,message)
    elif message[0:4] == '@查詢中':
        a=1
    elif message[0:4] != 'http':
        a=1
    elif message[0:4] != 'http':
        # print('....................:'+message[0:4])
        UsebookName(event,message)
def history(event):
    user_id = event.source.user_id
    connection = MongoClient(host=ip,port=27017)
    db = connection.kingstone
    collection = db['customers']
    isbn_list = list(collection.find({"_id":user_id},{"_id":0,"tag":1}))[0]['tag']
    print(isbn_list)
    book = list(map(findbook_ISBN,isbn_list))
    def carousel(book):
        if len(book['書名']) > 20:
            book['書名'] = book['書名'][:20]+'...'
        else:
            book['書名'] = book['書名']
        return CarouselColumn(
                        thumbnail_image_url=book['圖片網址'],
                        title=book['書名'],
                        text=book['作者'],
                        actions=[
                            PostbackTemplateAction(
                                label='查看更多資訊',
                                # text=books[0]['書籍簡介']
                                text=book['書籍網站'],
                                data='*'+book['ISBN']
                            ),
                            # URITemplateAction(
                            #     label='連結網頁',
                            #     alt_uri=books[0]['書籍網站'],
                            #     uri=books[0]['書籍網站']
                            # ),
                            PostbackTemplateAction(
                                label='您可能喜歡....',
                                text='@查詢中',
                                data='#'+book['ISBN']
                            ),
                            PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+book['ISBN'])])
    try:
        if len(book) < 10 :
            message = TemplateSendMessage(
                    alt_text='轉盤樣板',
                    template=CarouselTemplate(
                        columns=[carousel(i) for i in book]))
        
            line_bot_api.reply_message(event.reply_token, message)
        elif len(book) >= 10:
            message = TemplateSendMessage(
                    alt_text='轉盤樣板',
                    template=CarouselTemplate(
                        columns=[carousel(i) for i in book]))
        
            line_bot_api.reply_message(event.reply_token, message)
            # book = book[-10:]
            # books = '書名：'+'\n書名：'.join([i['書名'] for i in book])
            # message = TextSendMessage(text= books)
            # line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def UsebookName(event,message):
    
    book = findbook_Name(message)
    def carousel(book):
        if len(book['書名']) > 20:
            book['書名'] = book['書名'][:20]+'...'
        else:
          book['書名'] = book['書名']
        return CarouselColumn(
                        thumbnail_image_url=book['圖片網址'],
                        title=book['書名'],
                        text=book['作者'],
                        actions=[
                            PostbackTemplateAction(
                                label='查看更多資訊',
                                # text=books[0]['書籍簡介']
                                text=book['書籍網站'],
                                data='*'+book['ISBN']
                            ),
                            # URITemplateAction(
                            #     label='連結網頁',
                            #     alt_uri=books[0]['書籍網站'],
                            #     uri=books[0]['書籍網站']
                            # ),
                            PostbackTemplateAction(
                                label='您可能喜歡....',
                                text='@查詢中',
                                data='#'+book['ISBN']
                            ),
                            PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+book['ISBN'])])
    try:
     
        message = TemplateSendMessage(
                alt_text='轉盤樣板',
                template=CarouselTemplate(
                    columns=[carousel(i) for i in book]))
        line_bot_api.reply_message(event.reply_token, message)
        
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def Usebookintro(event,message):
    
    book = findbook_Intro(message)
    def carousel(book):
        if len(book['書名']) > 20:
            book['書名'] = book['書名'][:20]+'...'
        else:
          book['書名'] = book['書名']
        return CarouselColumn(
                        thumbnail_image_url=book['圖片網址'],
                        title=book['書名'],
                        text=book['作者'],
                        actions=[
                            PostbackTemplateAction(
                                label='查看更多資訊',
                                # text=books[0]['書籍簡介']
                                text=book['書籍網站'],
                                data='*'+book['ISBN']
                            ),
                            # URITemplateAction(
                            #     label='連結網頁',
                            #     alt_uri=books[0]['書籍網站'],
                            #     uri=books[0]['書籍網站']
                            # ),
                            PostbackTemplateAction(
                                label='您可能喜歡....',
                                text='@查詢中',
                                data='#'+book['ISBN']
                            ),
                            PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+book['ISBN'])])
    try:
     
        message = TemplateSendMessage(
                alt_text='轉盤樣板',
                template=CarouselTemplate(
                    columns=[carousel(i) for i in book]))
        line_bot_api.reply_message(event.reply_token, message)
        
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def UseAuthor(event,message):
    
    book = findbook_Author(message)
    def carousel(book):
        if len(book['書名']) > 20:
            book['書名'] = book['書名'][:20]+'...'
        else:
          book['書名'] = book['書名']
        return CarouselColumn(
                        thumbnail_image_url=book['圖片網址'],
                        title=book['書名'],
                        text=book['作者'],
                        actions=[
                            PostbackTemplateAction(
                                label='查看更多資訊',
                                # text=books[0]['書籍簡介']
                                text=book['書籍網站'],
                                data='*'+book['ISBN']
                            ),
                            # URITemplateAction(
                            #     label='連結網頁',
                            #     alt_uri=books[0]['書籍網站'],
                            #     uri=books[0]['書籍網站']
                            # ),
                            PostbackTemplateAction(
                                label='您可能喜歡....',
                                text='@查詢中',
                                data='#'+book['ISBN']
                            ),
                            PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+book['ISBN'])])
    try:
     
        message = TemplateSendMessage(
                alt_text='轉盤樣板',
                template=CarouselTemplate(
                    columns=[carousel(i) for i in book]))
        line_bot_api.reply_message(event.reply_token, message)
        
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendButton(event):  #按鈕樣版
    # es = Elasticsearch(hosts=ip, port=9200)
    # seed = int(time.time())
    # res = es.search(index="cleanbook_test",size=1,query={"function_score":{"random_score":{"seed":seed,"field":"_seq_no"}}})
    # for chooseone in res['hits']['hits']:
    #     chooseone = chooseone['_source']
    message = event.message.text
    book = findbook_ISBN(message[1:])
    if len(book['書名']) > 20:
        book['書名']=book['書名'][:10]+'...'
    else:
        book['書名']=book['書名']
    # contents = chooseone['書籍簡介'][:20]
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url=book['圖片網址'],  #顯示的圖片
                title=book['書名'],  #主標題
                text=book['作者'],  #副標題
                actions=[
                    PostbackTemplateAction(  #顯示文字計息
                        label='查看更多資訊',
                        text= book['書籍網站'],
                        data='*'+book['ISBN']
                    ),
                    PostbackTemplateAction(
                        label='您可能喜歡....',
                        text='@查詢中',
                        data='#'+book['ISBN']
                    ),
                    PostbackTemplateAction(
                            label='似乎有很像的書',
                            text='@查詢中',
                            data='%'+book['ISBN'])
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendCarousel(event):  #轉盤樣板
    isbn_list = random_choosebookISBN()
    books = list(map(findbook_ISBN,isbn_list))
    if len(books[0]['書名']) >20:
        books[0]['書名']=books[0]['書名'][:20]+'.....'
    elif len(books[1]['書名']) >20:
        books[1]['書名']=books[1]['書名'][:20]+'.....'
    elif len(books[2]['書名']) >20:
        books[2]['書名']=books[2]['書名'][:20]+'.....'
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                            thumbnail_image_url=books[0]['圖片網址'],
                            title=books[0]['書名'],
                            text=books[0]['作者'],
                            actions=[
                                PostbackTemplateAction(
                                    label='查看更多資訊',
                                    # text=books[0]['書籍簡介']
                                    text=books[0]['書籍網站'],
                                    data='*'+books[0]['ISBN']
                                ),
                                # URITemplateAction(
                                #     label='連結網頁',
                                #     uri=books[0]['書籍網站']
                                # ),
                                PostbackTemplateAction(
                                    label='您可能喜歡....',
                                    text='@查詢中',
                                    data='#'+books[0]['ISBN']
                                ),
                                PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+books[0]['ISBN'])
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=books[1]['圖片網址'],
                            title=books[1]['書名'],
                            text=books[1]['作者'],
                            actions=[
                                PostbackTemplateAction(
                                    label='查看更多資訊',
                                    # text=books[1]['書籍簡介']
                                    text=books[1]['書籍網站'],
                                    data='*'+books[1]['ISBN']
                                ),
                                # URITemplateAction(
                                #     label='連結網頁',
                                #     uri=books[1]['書籍網站']
                                # ),
                                PostbackTemplateAction(
                                    label='您可能喜歡....',
                                    text='@查詢中',
                                    data='#'+books[1]['ISBN']
                                ),
                                PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+books[1]['ISBN'])
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=books[2]['圖片網址'],
                            title=books[2]['書名'],
                            text=books[2]['作者'],
                            actions=[
                                PostbackTemplateAction(
                                    label='查看更多資訊',
                                    # text=books[2]['書籍簡介']
                                    text=books[2]['書籍網站'],
                                    data='*'+books[2]['ISBN']
                                ),
                                # URITemplateAction(
                                #     label='連結網頁',
                                #     uri=books[2]['書籍網站']
                                # ),
                                PostbackTemplateAction(
                                    label='您可能喜歡....',
                                    text='@查詢中',
                                    data='#'+books[2]['ISBN']
                                ),
                                PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+books[2]['ISBN'])
                            ]
                        )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        print(LineBotApiError)
        # print('.........')
def team_introduction(event):
    message = TextSendMessage(
        text="""
        \n緯育第47期 \nAI/Big Data資料分析師養成班\n第三組
        \n曾旭暉:\nhttps://github.com/gt50918 
        \n曾巧庭:\nhttps://github.com/u3814520 
        \n倪睿謙:\nhttps://github.com/as8610194625 
        \n謝元華:\nhttps://github.com/Hemsnick 
        \n黃啟烜:\nhttps://github.com/Vicbosstw
        """
        )
    try:
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def team_email(event):
    message = TextSendMessage(
        text="""
        \n曾旭暉:\ngt50918@gmail.com 
        \n曾巧庭:\nu3814520@gmail.com 
        \n倪睿謙:\nburabo19971019@gmail.com 
        \n謝元華:\nqoo071917@gmail.com 
        \n黃啟烜:\ngavye1b456tw@gmail.com
        """
        )
    try:
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def instruction(event):
    message = [TextSendMessage(
        text="""
        \n使用說明!!!!!!!
        \n點選輪盤"暢銷榜推薦"，會隨機推選3本書
        \n點選歷史紀錄，會有您過去曾點選查看更多資訊的書籍
        \n可直接在對話框內打上想要查詢的書名，會依據最相近名詞推選10本書
        \n若想查詢"作者"，請在對話框前打上"&"
        \nex:&金庸
        \n若想直接搜尋書籍"ISBN"，請在對話框前打上"$"
        \nex:$9789888570188
        \n若想直接搜尋書籍"簡介"，請在對話框前打上"#"
        \nex:#大地是人類生存的根基，也是人類活動的舞台........
        """
        ),
        ImageSendMessage(original_content_url="https://i.imgur.com/tOGjEkB.jpg",
        preview_image_url="https://i.imgur.com/tOGjEkB.jpg")
        ]
    try:
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    # print(data)
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    # print(user_id,user_name)
    if data[0:1] == '*':
        stored = {'_id':user_id,'userName':user_name,'tag':[data[1:]]}
        mongo_user_stored(stored)
    if data[0:1] == '#':
        try:
            isbn_list = findyoumaybelike_ISBN(data[1:])
            # print(isbn_list)
            # books = list(map(findbook_ISBN,isbn_list))
            you_maybe_like_function(event,isbn_list)
        except:
            sendCarousel(event)
def you_maybe_like_function(event,isbn_list):  #轉盤樣板
    # books_list = findyoumaybelike_ISBN(isbn)
    books = list(map(findbook_ISBN,isbn_list))
    if len(books[0]['書名']) >20:
        books[0]['書名']=books[0]['書名'][:20]+'.....'
    elif len(books[1]['書名']) >20:
        books[1]['書名']=books[1]['書名'][:20]+'.....'
    elif len(books[2]['書名']) >20:
        books[2]['書名']=books[2]['書名'][:20]+'.....'
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                            thumbnail_image_url=books[0]['圖片網址'],
                            title=books[0]['書名'],
                            text=books[0]['作者'],
                            actions=[
                                PostbackTemplateAction(
                                    label='查看更多資訊',
                                    # text=books[0]['書籍簡介']
                                    text=books[0]['書籍網站'],
                                    data='*'+books[0]['ISBN']
                                ),
                                # URITemplateAction(
                                #     label='連結網頁',
                                #     uri=books[0]['書籍網站']
                                # ),
                                PostbackTemplateAction(
                                    label='您可能喜歡....',
                                    text='@查詢中',
                                    data='#'+books[0]['ISBN']
                                ),
                                PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+books[0]['ISBN'])
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=books[1]['圖片網址'],
                            title=books[1]['書名'],
                            text=books[1]['作者'],
                            actions=[
                                PostbackTemplateAction(
                                    label='查看更多資訊',
                                    # text=books[1]['書籍簡介']
                                    text=books[1]['書籍網站'],
                                    data='*'+books[1]['ISBN']
                                ),
                                # URITemplateAction(
                                #     label='連結網頁',
                                #     uri=books[1]['書籍網站']
                                # ),
                                PostbackTemplateAction(
                                    label='您可能喜歡....',
                                    text='@查詢中',
                                    data='#'+books[1]['ISBN']
                                ),
                                PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+books[1]['ISBN'])
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=books[2]['圖片網址'],
                            title=books[2]['書名'],
                            text=books[2]['作者'],
                            actions=[
                                PostbackTemplateAction(
                                    label='查看更多資訊',
                                    # text=books[2]['書籍簡介']
                                    text=books[2]['書籍網站'],
                                    data='*'+books[2]['ISBN']
                                ),
                                # URITemplateAction(
                                #     label='連結網頁',
                                #     uri=books[2]['書籍網站']
                                # ),
                                PostbackTemplateAction(
                                    label='您可能喜歡....',
                                    text='@查詢中',
                                    data='#'+books[2]['ISBN']
                                ),
                                PostbackTemplateAction(
                                label='似乎有很像的書',
                                text='@查詢中',
                                data='%'+books[2]['ISBN'])
                            ]
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token,message)
    
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
# run app
if __name__ == "__main__":
    app.run(host='localhost',debug=True, port=12345)
