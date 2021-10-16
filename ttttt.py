from elasticsearch import Elasticsearch
 

if __name__ == "__main__":
    es = Elasticsearch(hosts='192.168.159.128', port=9200)
    res = es.search(index="datas", body={"query":{"match_all":{}}})
    # print(res)
    for hit in res['hits']['hits']:
        print(hit["_source"]['ISBN'])