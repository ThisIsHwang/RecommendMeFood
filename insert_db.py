
from koreanSimilarity import preProcessSentence
import sys
from elasticsearch import Elasticsearch
import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import urllib.request

es_host="127.0.0.1"
es_port="9200"

es = Elasticsearch([{"host" : es_host, 'port' : es_port}], timeout = 30)

client_id = "eJhNnO3TymuMBJiJjqX5"
client_secret = "6eqzRwNKNB"
food_name_list = ['치킨', '족발', '김밥', '라면', '짜장면', '피자']
for f in food_name_list:
    encText = urllib.parse.quote(f)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=100"# json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

    retdata = response_body.decode('utf-8')
    jsonresult = json.loads(retdata)

    k=0
    for i in jsonresult['items']:
        if "naver" in i['link']:
            index = i['link'].find('blog')
            i['link'] = i['link'][:index] + 'm.' + i['link'][index:]
            # print(i['link'])
            page = requests.get(i['link'])
            soup = BeautifulSoup(page.content,'html.parser')
            
            food_data = {
                "food_name" : f,
                "content" : "" 
            }  

            for a in soup.find_all('p'):
                #print(a.get_text())
            
                food_data['content'] += a.get_text()
            food_data['content'] = preProcessSentence(food_data['content'])
            k+=1
            
            res= es.index(index='food', doc_type='food', body=food_data)
            print(res)
            print(food_data)        





