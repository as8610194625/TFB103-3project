from elasticsearch import Elasticsearch


if __name__ == "__main__":
    es = Elasticsearch(hosts='10.2.18.6', port=9200)
    res = es.search(index="kingstone", body={"query":{"match_all":{}}})
    # print(res)
    for hit in res['hits']['hits']:
        print(hit["_source"]['書籍簡介'])