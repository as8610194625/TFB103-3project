import json
import pandas as pd 
from pymongo import MongoClient, collection
with open (r"C:\Users\Tibame\Desktop\TFB103-3project\Project-linebot\recommand_youmaybelike.json","r",encoding="utf-8") as f:
    a = json.loads(f.read())
    connection = MongoClient(host='10.2.14.10',port=27017)
    db = connection.kingstone
    collection = db['comment_all.json']
    collection.drop()
    for i,k in a.items():
        print(i,k)
        x = {"ISBN":str(i),"list":k}
        collection.insert([x])
