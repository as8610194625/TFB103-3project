import json
import pandas as pd 
from pymongo import MongoClient, collection
import numpy as np
import pandas as pd
import time
from elasticsearch import Elasticsearch

def mongo_time(self):  #按鈕樣版
    start = time.time()
    connection = MongoClient(host='10.2.14.10',port=27017)
    db = connection.kingstone
    collection = db['cleanbook']
    chooseisbn = list(collection.find({"ISBN":self}))[0]
    chooseisbn.pop('書籍簡介')
    end = time.time()
    # print(chooseisbn)
    return end-start
def elasic_time(self):
    start = time.time()
    es = Elasticsearch(hosts='10.2.14.10', port=9200)
    res = es.search(index="cleanbook_test", query={"match":{"ISBN":self}})
    # print(res['hits']['hits'])
    # book = res['hits']['hits'][0]["_source"]
    for hit in res['hits']['hits']:
        # global book_all
        book_all = hit["_source"]
        book_all.pop('書籍簡介')
    end = time.time()
    # print(book_all)
    return end-start
print('Momgodb查詢時間：',mongo_time("9789888570188"))
print('Elasticsearch查詢時間：',elasic_time("9789888570188"))

