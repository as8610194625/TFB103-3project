from pymongo import MongoClient, collection
import json
import os
connection = MongoClient(host='10.2.14.10',port=27017)
db = connection.kingstone
collection = db['cleanbook']
def kingstone_stored(self):
    with open (self,'r',encoding='utf-8') as f:
        for data in f:
            data = json.loads(data)
            data['_id'] = data['ISBN']
            try:
                result = collection.insert([data])
                print('已新增',data)
                print("----------")
            except:
                print('已存在_id',data['_id'],'(因此不寫入)')
                print("----------")


# for filename in os.listdir(os.getcwd()+'\\kingstone_datas\\json'):
#     kingstone_stored(os.getcwd()+'\\kingstone_datas\\json\\'+filename)
#     # print(filename)
kingstone_stored(r"C:\Users\Tibame\Desktop\TFB103-3project\allbooks_update.json")
print('Completed')
