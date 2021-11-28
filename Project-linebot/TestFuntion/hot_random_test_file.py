from pymongo import MongoClient, collection
import json
import random
secretFile=json.load(open("secretFile.json",'r'))
channelAccessToken=secretFile['channelAccessToken']
channelSecret=secretFile["channelSecret"]
ip = secretFile["IP"]
def hot():
    hot = []
    connection = MongoClient(host=ip,port=27017)
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
    connection = MongoClient(host=ip,port=27017)
    db = connection.kingstone
    collection = db['inter']
    # allbooks = list(collection.find())
    chooseisbn = list(collection.aggregate([{'$project':{'_id':0,'ISBN':1}},{'$sample':{'size':3}}]))
    # chooseisbn[0] = chooseisbn[0]['ISBN']
    return [chooseisbn[0]['ISBN'],chooseisbn[1]['ISBN'],chooseisbn[2]['ISBN']]
def findyoumaybelike(isbn):  #轉盤樣板
    connection = MongoClient(host=ip,port=27017)
    db = connection.kingstone
    collection = db['comment_all.json']
    data = collection.find({'ISBN':isbn})
    datas = list(data)[0]['list']
    return datas

# print(findyoumaybelike("9789868949645"))
# print((choosebookISBN()))