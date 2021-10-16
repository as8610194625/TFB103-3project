from elasticsearch import Elasticsearch
import json
datas = open (r'kingstone_datas\json\kingstone_baa.json','r',encoding='utf-8')
# for data in datas:
#     data = json.loads(data)
#     try:
#         print(int(data['ISBN']))
#     except TypeError as e :
#         print(data['ISBN'])
        



def create_data(es, datas):
    for data in datas:
        data = json.loads(data)
        print(data['ISBN'])
        try:
            es.index(index='datas', id=int(data['ISBN']),body=data)
        except TypeError:
            # es.index(index='datas',body=data) 
            pass

if __name__ == "__main__":
    es = Elasticsearch(hosts='192.168.159.128', port=9200)
    create_data(es, datas)
    print('ok')