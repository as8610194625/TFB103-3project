from pymongo import MongoClient, collection
import json
import os

def kingstone_stored(self):
    connection = MongoClient(host='10.2.18.6',port=27017)
    db = connection.kingstone
    collection = db['customers']
    try:
        result = collection.insert([self])
        print('已新增',self['_id'])
        print("----------")
    except:
        print('已存在_id',self['_id'],'(因此不寫入)')
        print("----------")
