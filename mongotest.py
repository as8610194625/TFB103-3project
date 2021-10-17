from pymongo import MongoClient, collection
import json
from jieba_def import cut_words

connection = MongoClient(host='127.0.0.1',port=27017)
db = connection.kingstone
collection = db['test']
cursor = collection.find()
# print(cursor.alive)
for i in cursor:
    # print(i['書籍簡介'])
    print('--------------------')
    try:
        if not i['書籍簡介'].encode('utf-8').isalpha():
            try:
                collection.update({"_id": i['_id']}, {"$set": {'書籍簡介': cut_words(i['書籍簡介'])}})
            except:
                continue
        else:
            try:
                collection.update({"_id": i['_id']}, {"$set": {'書籍簡介': i['書籍簡介'].split(' ')}})
            except:
                continue
    except:
        continue