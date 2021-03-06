from elasticsearch import Elasticsearch
import re
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

okt = Okt()

#stopwords들을 텍스트 파일에서 가져온다.
with open("static/text/stopwords.txt", "rt", encoding="utf-8") as f:
    stop_words = f.readlines()
stop_words = [line.rstrip() for line in stop_words]

#DB에서 크롤링한 데이터들을 받아온다
contents = [' ', ]
food_names = [' ', ]

#DB를 사용하기 위한 ip와 port 번호
es_host="127.0.0.1"
es_port="9200"

es = Elasticsearch([{"host" : es_host, 'port' : es_port}], timeout = 30)

#DB에서 크롤링한 데이터를 받아오기 위한 함수이다
def getCorpus():
    data = {"match_all" : {}}
    body = {"query" : data}
    docs = es.search(index='food', body=body, size=10000)
    if docs['hits']['total']['value']>0:
        for doc in docs['hits']['hits']:
            contents.append(doc['_source']['content'])
            food_names.append(doc['_source']['food_name'])


#자연어 전처리를 위한 함수이다. 형태소를 분석해서 원형으로 바꿔주며 불용어를 처리해준다.
def morph_and_stopword(s):
    token_ls = ""
    # 형태소 분석
    tmp = okt.morphs(s, stem=True, norm=True)

    # 불용어 처리
    for token in tmp:
        if token not in stop_words:
            token_ls += " " + token
    return token_ls

#자연어 전처리를 위한 함수이다. 유의미한 글자를 제외하고 이모티콘 두구점들을 정규표현식을 통해 삭제한다.
def sub_special(s):
    return re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z ]', '', s)

#코사인 유사도 분석을 해서 음식을 추천해준다.
def recommendFood(title, cosine_sim):
    # 기존 데이터와 음식 유사도를 구하기
    sim_scores = list(enumerate(cosine_sim[0]))
    
    # 유사도에 따라 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #print(sim_scores)
    # 가장 유사한 10개의 음식을 받아옴
    sim_scores = sim_scores[1:11]
    for s in sim_scores:
        print(s)
    
    # 가장 유사한 10개 음식의 인덱스 받아옴
    food_indices = [i[0] for i in sim_scores]
    
    
    for i in food_indices:
        print(food_names[i])
        print(contents[i])
        
    print("결과 : " + food_names[food_indices[0]])
    return food_names[food_indices[0]]

#문장 자연어 전처리를 해주는 함수
def preProcessSentence(sentence):
    sentence = sub_special(sentence)
    sentence = morph_and_stopword(sentence)
    return sentence

#코퍼스를 자연어 전처리를 해주는 함수
def preProcessCorpus():
    for i, c in enumerate(contents):
        contents[i] = preProcessSentence(c)


if __name__ == '__main__':
    
    getCorpus()
    #DB에서 데이터를 가져온다.
    text = input("쓰고 싶은 말을 쓰세요 : ")
    
    #TF-IDF를 사용자의 글과 함께 비교하기 위해서 코퍼스에 추가한다.
    contents[0] = preProcessSentence(text)
    food_names[0] = 'user'
    print(contents[0])
    
    #TF-IDF 벡터를 구한다.
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(contents)
    print(tfidf_matrix.shape)
    #TF-IDF 벡터로 코사인 유사도를 분석한다.
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    recommendFood(text, cosine_sim)
    
