from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:1234@cluster0.zvpdvge.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.toy_project



# JWT 토큰을 만들 때 필요한 비밀문자열
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 가능.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.
import hashlib


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
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/register')
def register():
    return render_template('checkout.html')

@app.route('/list')
def gyeonggi_do():
    return render_template('list.html')

@app.route('/list_detail')
def Chungcheong_do():
    return render_template('list_detail.html')

@app.route('/main')
def list_search():
    return render_template('index.html')


#기웅
# 데이터 내려오기
@app.route("/gyeonggi", methods=["GET"])
def gyeonggi_get():
    all_gyeonggi = list(db.details.find({},{'_id':False}))
    return jsonify({'result': all_gyeonggi})

#검색기능
@app.route('/gyeonggi', methods=["POST"])
def search_get():
    search_receive = request.form['title_give']
    
    search_list = list(db.details.find({'$or': [{'title': {'$regex': search_receive}},]},{'_id': False}))
    
    return jsonify({'searches': search_list})

#기웅
#덕인
@app.route("/travelDetail", methods=["POST"])
def travelDetail_post():
    url_receive = request.form['url_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    
    title_split = soup.select_one('head > title').text 
    title = title_split.split('>')[0]  #'>'를 기준으로 문자열을 분리하고 첫 번째 부분을 선택

    image = soup.select_one('meta[property="og:image"]')['content']

    desc = soup.select_one('meta[name="description"]')['content']
    desc_split = desc.split('.')[0] + '.' #'.'를 기준으로 문자열을 분리하고 첫 번째 부분을 선택 

    doc = {
        'title':title,
        'desc':desc,
        'desc_split':desc_split,
        'image':image
    }
    db.details.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

#상세 페이지에 데이터 보내주기
@app.route('/list_detail/<temp>')
def detail_post(temp):
   detailTravel = db.details.find_one({'title':temp},{'_id': False})
   return render_template('list_detail.html', result = detailTravel,
                                        title = detailTravel['title'],
                                        desc = detailTravel['desc'],
                                        desc_split = detailTravel['desc_split'],
                                        image = detailTravel['image'])

@app.route("/travelDetail", methods=["GET"])
def travelDetail_get():
     all_details = list(db.details.find({},{'_id':False}))
     return jsonify({'result':all_details})

# 여행 상세 페이지 > 코멘트 DB 저장
@app.route("/detail/travelComment", methods=["POST"])
def travelComment_post():
    name_receive = request.form['name_give']
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    doc = {
        'name':name_receive,
        'title':title_receive,
        'comment':comment_receive,
        'star':star_receive
    }
    db.comments.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

# 코멘트 불러오기
@app.route("/detail/travelComment", methods=["GET"])
def travelComment_get():
    all_comments = list(db.comments.find({},{'_id':False}))
    return jsonify({'result': all_comments})

#덕인
#기영
@app.route('/test', methods=['GET'])
def test_get():
   
    all_users = list(db.details.find({},{'_id':False}))
    print(all_users)
    return jsonify({'result':all_users})

#기영
#소연

# 회원가입 API - id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']
    
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


# 로그인 id, pw 값을 받아서 토큰을 만들어 발급
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # pw암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된 pw을 가지고 해당 user 찾기.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰 발급
    if result is not None:
        # JWT - payload와 시크릿키 필요.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token 
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


#
#유저 정보 확인 API - 로그인된 유저만 call 할 수 있는 API
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        # token을 시크릿키로 디코딩합니다.
        # 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 만료시간 초과 에러 발생
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
#소연
# 윤기
# 윤기

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)