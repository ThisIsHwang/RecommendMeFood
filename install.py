from insert_db import insertToDB
from elasticsearch import Elasticsearch
            
def inspectDB():
    es_host="127.0.0.1"
    es_port="9200"
    es = Elasticsearch([{"host" : es_host, 'port' : es_port}], timeout = 30)
    data = {"match_all" : {}}
    body = {"query" : data}
    docs = es.search(index='food', body=body, size=1)
    if docs['hits']['total']['value']==0:
        print("새로운 데이터들을 크롤링해옵니다.")
        insertToDB()
    else:
        print("이미 데이터가 있어 크롤링해올 필요가 없습니다.")
inspectDB()