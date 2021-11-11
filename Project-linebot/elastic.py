from elasticsearch import Elasticsearch
from pymongo import MongoClient, collection
import json
import random
es = Elasticsearch(hosts='10.2.18.6', port=9200)

book_all=1
def you_maybe_like(ISBN):
    # res = es.search(index="kingstone", body={"from":10,"size":20,"query":{"match_all":{}}})
    res = es.search(index="cleanbook_test", body={"query":{"match":{"ISBN":ISBN}}})
    # print(res['hits']['hits'])
    # book = res['hits']['hits'][0]["_source"]
    for hit in res['hits']['hits']:
        global book_all
        book_all = hit["_source"]
    return book_all
def find_book(book):
    res = es.search(index="kingstone", body={"size":5,"query":{"match":{"書籍簡介":{"query":book,"fuzziness":"AUTO"}}}})
    # res = es.search(index="kingstone", body={"query":{"match":{"ISBN":book}}})
    # print(res)
    for i,hit in enumerate(res['hits']['hits']):
        book = hit["_source"]['書名']
        print(i,book)
    return book
def recommend(ISBN_LIST):
    f = open (r"C:\Users\Tibame\Desktop\TFB103-3project\Project-linebot\recommand_youmaybelike.json","r",encoding="utf-8")
    like_dict = json.loads(f.read())
    books = []
    for book in like_dict[ISBN_LIST]:
        books.append(you_maybe_like(book))
    return(books)
# print(recommend('1905302050014'))
def random_find():
    connection = MongoClient(host='10.2.18.6',port=27017)
    db = connection.kingstone
    collection = db['comment1']
    allbooks = list(collection.find())[0]
    allbooks.pop('_id')
    choose = random.sample(allbooks.keys(),5)
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