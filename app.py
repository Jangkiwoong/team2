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




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/seoul')
def seoul():
    return render_template('seoul.html')

@app.route('/gyeonggi_do')
def gyeonggi_do():
    return render_template('gyeonggi_do.html')

@app.route('/Gangwon_do')
def Gangwon_do():
    return render_template('Gangwon_do.html')

@app.route('/Chungcheong_do')
def Chungcheong_do():
    return render_template('Chungcheong_do.html')





@app.route("/", methods=["POST"])
def mars_post():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg':'POST 연결 완료!'})



@app.route("/gyeonggi", methods=["GET"])
def gyeonggi_get():
    all_gyeonggi = list(db.gyeonggi.find({},{'_id':False}))
    print('###')
    print(all_gyeonggi)
    print('###')
    return jsonify({'result': all_gyeonggi})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
