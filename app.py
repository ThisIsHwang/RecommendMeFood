from flask import Flask
from flask import render_template
import argparse
from flask import jsonify, request
import koreanSimilarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)


#음식의 링크를 받아옵니다.
def getFoodImgLink(food):
    result = ""
    if food == "라면":
        result = "../static/images/rameon.jpg"
    if food == "족발":
        result = "../static/images/jogbal.jpg"
    if food == "치킨":
        result = "../static/images/chicken.jpg"
    if food == "피자":
        result = "../static/images/pizza.jpg"
    if food == "짜장면":
        result = "../static/images/noodle.jpg"
    if food == "김밥":
        result = "../static/images/gimbap.jpg"        
    return result


@app.route('/')
def home():
    return render_template('index.html') #첫 메인 홈페이지 정식이꺼 index.html , 근철이꺼 home.html

@app.route('/ajax', methods=['POST'])
def ajax():
    recommendation = request.get_json()['content']
    print(recommendation)
    koreanSimilarity.getCorpus()
    #DB에서 데이터를 가져온다.
    text = recommendation
    
    #TF-IDF를 사용자의 글과 함께 비교하기 위해서 코퍼스에 추가한다.
    koreanSimilarity.contents[0] = koreanSimilarity.preProcessSentence(text)
    koreanSimilarity.food_names[0] = 'user'
    print(koreanSimilarity.contents[0])
    
    #TF-IDF 벡터를 구한다.
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(koreanSimilarity.contents)
    #print(tfidf_matrix.shape)

    #TF-IDF 벡터로 코사인 유사도를 분석한다.
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    result = koreanSimilarity.recommendFood(text, cosine_sim)
    #print(data)
    print("결과 : " + result)
    link = getFoodImgLink(result)
    print(link)
    return jsonify(result="success", result2=result, linkResult=link)

app.run(debug=True)