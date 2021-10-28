from pymongo import MongoClient, collection
import json
from jieba_def import cut_words

connection = MongoClient(host='10.2.18.6',port=27017)
db = connection.kingstone
collection = db['test']
collections = db['jieba']
cursor = collection.find()
# print(cursor.alive)

for i in cursor:
    # print(i['書籍簡介'])
    print('--------------------')
    try:
        if not i['書籍簡介'].encode('utf-8').isalpha():
            # collection.update({"_id": i['_id']}, {"$set": {'書籍簡介': cut_words(i['書籍簡介'])}})
            collections.insert({'_id':i['_id'],'書籍簡介':cut_words(i['書籍簡介'])})
        else:
            collection.update({"_id": i['_id']}, {"$set": {'書籍簡介': i['書籍簡介'].split(' ')}})
            collections.insert({'_id':i['_id'],'書籍簡介':i['書籍簡介'].split(' ')})
    except:
        continue
