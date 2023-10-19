# models.py
from flask_sqlalchemy import SQLAlchemy
#db 객체를 통해 SQLAlchemy 초기화
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    domain_address = db.Column(db.String(255))
    IP_address = db.Column(db.String(15))
    membership = db.Column(db.String(20))
    
#각 특성에 맞는 7개의 필드로 구성된 User 클래스

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
#각 특성에 맞는 3개의 필드로 구성된 Admin 클래스

#db 내에서 테이블에 저장된 개별적인 항목이나 행을 가리키는 레코드를 고유하게 식별하는 primary key는
#User와 Admin 둘다 id로 식별을 하기로 하였음.
