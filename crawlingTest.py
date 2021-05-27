import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import urllib.request

client_id = "eJhNnO3TymuMBJiJjqX5"
client_secret = "6eqzRwNKNB"
encText = urllib.parse.quote("짜장면")
url = "https://openapi.naver.com/v1/search/blog?query=" + encText # json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
   #print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

retdata = response_body.decode('utf-8')
jsonresult = json.loads(retdata)

for i in jsonresult['items']:
    if "naver" in i['link']:
        index = i['link'].find('blog')
        i['link'] = i['link'][:index] + 'm.' + i['link'][index:]
        # print(i['link'])
        page = requests.get(i['link'])
        soup = BeautifulSoup(page.content,'html.parser')
        for a in soup.find_all('p'):
            print(a.get_text())
