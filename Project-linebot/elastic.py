from elasticsearch import Elasticsearch


if __name__ == "__main__":
    es = Elasticsearch(hosts='localhost', port=9200)
    res = es.search(index="kingstone", body={"query":{"fuzzy":{"書名":"python"}}})
    # print(res)
    for hit in res['hits']['hits']:
        print(hit["_source"]['書名'])