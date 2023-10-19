# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pi5neer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Pi5neer123!@#'
#SQLAlchemy가 사용할 데이터베이스의 URI를 설정
#SQLAlchemy의 수정 추적 기능을 비활성화하도록 설정-> 메모리를 절약
#Flask 애플리케이션의 세션 및 암호화를 위한 비밀 키를 설정
