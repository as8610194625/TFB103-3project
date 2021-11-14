import json
import pandas as pd 
from pymongo import MongoClient, collection


connection = MongoClient(host='192.168.1.7',port=27017)
db = connection.kingstone
collection = db['comment_all.json']
collection_clean = db['cleanbook']
collection_inter = db['inter']
all_1 = collection.find()
clean = collection_clean.find()
all_list = []
clean_list = []
for a in all_1:
    all_list.append(str(a["ISBN"]))
for b in clean:
    clean_list.append(str(b["ISBN"]))
    print('b...waiting')
inter = set(clean_list) & set(all_list)
# print(inter)
for i in inter:
    collection_inter.insert({"ISBN":i})
    print('inserting......')
print("OK")