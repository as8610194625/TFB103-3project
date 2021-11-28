from elasticsearch import Elasticsearch
from pymongo import MongoClient, collection
import json
import time 
import random
import numpy as np

from books_linebot import findbook_Name
secretFile=json.load(open("secretFile.json",'r'))
channelAccessToken=secretFile['channelAccessToken']
channelSecret=secretFile["channelSecret"]
ip = secretFile["IP"]

# book_all=1
def find_bookisbn(ISBN):
    es = Elasticsearch(hosts=ip, port=9200)
    res = es.search(index="cleanbook_test", query={"match":{"ISBN":ISBN}})
    # print(res['hits']['hits'])
    # book = res['hits']['hits'][0]["_source"]
    for hit in res['hits']['hits']:
        global book_all
        book_all = hit["_source"]
        book_all.pop('書籍簡介')
        # print(book_all)
    return book_all
def find_bookname(book):
    es = Elasticsearch(hosts=ip, port=9200)
    res = es.search(index="cleanbook_test", size=3,query={"match":{"書籍簡介":{"query":book,"fuzziness":"AUTO"}}})
    # res = es.search(index="kingstone", body={"query":{"match":{"ISBN":book}}})
    # print(res)
    books = []
    for i,hit in enumerate(res['hits']['hits']):
        book = hit["_source"]
        # print(i,book)
        book.pop('書籍簡介')
        books.append(book)
    return books
def recommend(ISBN_LIST):
    f = open (r"C:\Users\Tibame\Desktop\TFB103-3project\Project-linebot\recommand_youmaybelike.json","r",encoding="utf-8")
    like_dict = json.loads(f.read())
    books = []
    for book in like_dict[ISBN_LIST]:
        books.append(find_bookisbn(book))
    return(books)
# print(recommend('1905302050014'))
def random_find():
    connection = MongoClient(host=ip,port=27017)
    db = connection.kingstone
    collection = db['comment1']
    allbooks = list(collection.find())[0]
    allbooks.pop('_id')
    choose = random.sample(set(allbooks.keys()),5)
    return choose
    # print(like_dict)
    # res = es.search(index="kingstone", body={"size":5,"query":{"function_score":{"functions":[{"random_score": {}}]}}})
    # res = es.search(index="kingstone", body={"query":{"match":{"ISBN":book}}})
    # print(res)
    # books = res['hits']['hits']
    # print(len(books))
    # for i,hit in enumerate(res['hits']['hits']):
    #     book = hit["_source"]['書名']
        # print(i,hit["_source"])
    # return books
# print(random_find())
def choosebooks():
    choose = []
    seed = int(time.time())
    es = Elasticsearch(hosts=ip, port=9200)
    res = es.search(index="cleanbook_test", query={"function_score":{"random_score":{"seed":seed,"field":"_seq_no"}}},size=3)
    for chooseone in res['hits']['hits']:
        chooseone = chooseone['_source']
        # print(type(chooseone))
        chooseone.pop('書籍簡介')
        choose.append(chooseone)
        # print(chooseone)
    choose = np.array(choose)
    return choose

print(find_bookname('Python'))