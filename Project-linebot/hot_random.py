from pymongo import MongoClient, collection
import json
import random

def hot():
    hot = []
    connection = MongoClient(host='10.2.18.6',port=27017)
    db = connection.kingstone
    collection = db['cleanbook']
    allbooks = list(collection.find())
    choosetwo = random.sample(allbooks,2)
    for k,i in enumerate (choosetwo):
        reply = '第%s本'%(k+1),i['書名'],'\n',i['書籍網站']
        # print(reply)
        hot.append(reply)
    return hot
def sendButton():  #按鈕樣版
    connection = MongoClient(host='10.2.18.6',port=27017)
    db = connection.kingstone
    collection = db['comment1']
    allbooks = list(collection.find())[0]
    allbooks.pop('_id')
    choose = random.sample(allbooks.keys(),5)
    # allbooks = list(collection.find())
    # chooseone = random.choice(allbooks)
    # choosetwo = random.sample(allbooks,6)
    # # hot.append(choosetwo)
    # print(choosetwo)
    # imageurl = chooseone['圖片網址']
    # book = chooseone['書名']
    # url = chooseone['書籍網站']
    # global contents
    # contents = chooseone['書籍簡介']
    # print(imageurl,book,url)
    
sendButton()
