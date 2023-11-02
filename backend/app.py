# app.py
from flask import Flask
#Flask 모듈 및 패키지
from config import Config
#Config 클래스를 사용하여 애플리케이션의 설정을 구성.
#config.py 파일에서 db 연결정보 및 기타 애플리케이션 관련 설정 포함.
from models import db
#db 객체를 생성하고 초기화 
#models 모듈에서 정의한 db 모델과 연결하기 위해 Flask-SQLAlchemy 사용
from routes.users import app as users
from routes.admin import app as admin
#rotues.user, admin 모듈에서 app Blueprint 객체를 가져옴
#Blueprint란 애플리케이션의 구조를 더 모듈화하고 구성 요소를 관리하기 쉽게만드는 역할
from flask_cors import CORS
#CORS(Cross Origin Resource Sharing)
#웹 애플리케이션을 로컬호스트(http://localhost:3000)에서 실행될 때 교차 출처 요청을 허용하도록 설정

#Flask 애플리케이션 인스턴스 만들기 및 구성 설정
app = Flask(__name__)
app.config.from_object(Config)
#db 초기화
db.init_app(app) 
# Registering the blueprint
app.register_blueprint(users)  
app.register_blueprint(admin)


#CORS 구성
CORS(app, origins='http://localhost:3000', supports_credentials=True)
#App context 내에서 db 생성
with app.app_context():
    db.create_all()
#Application run
if __name__ == '__main__':
    app.run(debug=True)
