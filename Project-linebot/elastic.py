from elasticsearch import Elasticsearch
import json
import time
es = Elasticsearch(hosts='10.2.18.6', port=9200)
f = open (r"C:\Users\Tibame\Desktop\TFB103-3project\Project-linebot\recommand_youmaybelike.json","r",encoding="utf-8")
like_dict = json.loads(f.read())

def you_maybe_like(ISBN):
    # res = es.search(index="kingstone", body={"from":10,"size":20,"query":{"match_all":{}}})
    res = es.search(index="kingstone", body={"query":{"match":{"ISBN":ISBN}}})
    # print(res)
    for hit in res['hits']['hits']:
        book = hit["_source"]
def find_book(book):
    res = es.search(index="kingstone", body={"size":5,"query":{"match":{"書籍簡介":{"query":book,"fuzziness":"AUTO"}}}})
    # res = es.search(index="kingstone", body={"query":{"match":{"ISBN":book}}})
    # print(res)
    for i,hit in enumerate(res['hits']['hits']):
        book = hit["_source"]['書名']
        print(i,book)
    return book
def recommend(ISBN_LIST):
    books = []
    for book in like_dict[ISBN_LIST]:
        books.append(you_maybe_like(book))
    return(books)
# print(recommend('1905302050014'))
def random_find():
    res = es.search(index="kingstone", body={"size":5,"query":{"function_score":{"functions":[{"random_score": {}}]}}})
    # res = es.search(index="kingstone", body={"query":{"match":{"ISBN":book}}})
    # print(res)
    books = res['hits']['hits']
    print(len(books))
    # for i,hit in enumerate(res['hits']['hits']):
    #     book = hit["_source"]['書名']
    #     print(i,hit["_source"])
    return books
random_find()