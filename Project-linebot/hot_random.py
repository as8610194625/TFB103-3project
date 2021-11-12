from pymongo import MongoClient, collection
import json
import random
secretFile=json.load(open("secretFile.json",'r'))
channelAccessToken=secretFile['channelAccessToken']
channelSecret=secretFile["channelSecret"]

def hot():
    hot = []
    connection = MongoClient(host='10.2.14.10',port=27017)
    db = connection.kingstone
    collection = db['cleanbook']
    allbooks = list(collection.find())
    choosetwo = random.sample(allbooks,2)
    # for k,i in enumerate (choosetwo):
    #     reply = '第%s本'%(k+1),i['書名'],'\n',i['書籍網站']
    #     # print(reply)
    #     hot.append(reply)
    return hot
def choosebookISBN():  #按鈕樣版
    connection = MongoClient(host='10.2.14.10',port=27017)
    db = connection.kingstone
    collection = db['cleanbook']
    allbooks = list(collection.find())
    # allbooks.pop('_id')
    # choose = random.sample(allbooks.keys(),5)
    # allbooks = list(collection.find())
    # chooseone = random.choice(allbooks)
    choose = random.sample(allbooks,6)
    # # hot.append(choosetwo)
    # print(choose['ISBN'])
    # imageurl = chooseone['圖片網址']
    # book = chooseone['書名']
    # url = chooseone['書籍網站']
    # global contents
    # contents = chooseone['書籍簡介']
    # print(imageurl,book,url)
def findyoumaybelike(isbn):  #轉盤樣板
    connection = MongoClient(host='10.2.14.10',port=27017)
    db = connection.kingstone
    collection = db['comment_all.json']
    data = collection.find({'ISBN':isbn})
    datas = list(data)[0]
    return datas
# print(findyoumaybelike("9789577431455")[0])
