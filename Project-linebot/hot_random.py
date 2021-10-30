from pymongo import MongoClient, collection
import json
import random

def hot():
    hot = []
    connection = MongoClient(host='127.0.0.1',port=27017)
    db = connection.kingstone
    collection = db['test']
    allbooks = list(collection.find())
    choosetwo = random.sample(allbooks,2)
    for k,i in enumerate (choosetwo):
        reply = '第%s本'%(k+1),i['書名'],'\n',i['書籍網站']
        # print(reply)
        hot.append(reply)
    return hot
def sendButton():  #按鈕樣版
    connection = MongoClient(host='127.0.0.1',port=27017)
    db = connection.kingstone
    collection = db['test']
    allbooks = list(collection.find())
    chooseone = random.choice(allbooks)
    # choosetwo = random.sample(allbooks,2)
    # hot.append(choosetwo)
    imageurl = chooseone['圖片網址']
    book = chooseone['書名']
    url = chooseone['書籍網站']
    # global contents
    contents = chooseone['書籍簡介']
    print(imageurl,book,url)
sendButton()
