from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:1234@cluster0.zvpdvge.mongodb.net/?retryWrites=true&w=majority')
db = client.toy_project

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20210829',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# path
import os
simp_path = '/'
abs_path = os.path.abspath(simp_path)



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/gyeonggi_do')
def gyeonggi_do():
    return render_template('gyeonggi_do.html')



@app.route('/list_detail')
def Chungcheong_do():
    return render_template('list_detail.html')

@app.route('/list')
def list_search():
    return render_template('list.html')




#기웅
# 데이터 내려오기
@app.route("/gyeonggi", methods=["GET"])
def gyeonggi_get():
    all_gyeonggi = list(db.gyeonggi.find({},{'_id':False}))
    return jsonify({'result': all_gyeonggi})

#검색기능
@app.route('/gyeonggi', methods=["POST"])
def search_get():
    search_receive = request.form['title_give']
    
    search_list = list(db.gyeonggi.find({'$or': [{'title': {'$regex': search_receive}},]},{'_id': False}))
    
    return jsonify({'searches': search_list})


#상세페이지로 데이터 주기
@app.route('/list_det/<temp>')
def test_post(temp):
   print('###')
   print(temp)
   print('###')
   asd = db.gyeonggi.find_one({'title':temp},{'_id': False})
   return render_template('list_detail.html',result = asd)









#기웅
#덕인

























#덕인
#기영
































#기영
#소연












































#소연
#윤기



































#윤기



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)