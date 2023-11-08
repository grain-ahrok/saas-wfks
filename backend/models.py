from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    domain_address = db.Column(db.String(255))
    IP_address = db.Column(db.String(15))
    Port_number = db.Column(db.String(15))
    membership = db.Column(db.String(20))

    @classmethod
    def create(cls, **kwargs):
        hashed_password = bcrypt.generate_password_hash(kwargs['password']).decode('utf-8')
        del kwargs['password']  # Remove plain text password from kwargs
        kwargs['password'] = hashed_password
        user = cls(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def change_password(self, new_password):
        self.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        
#각 특성에 맞는 7개의 필드로 구성된 User 클래스
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
#각 특성에 맞는 3개의 필드로 구성된 Admin 클래스

#db 내에서 테이블에 저장된 개별적인 항목이나 행을 가리키는 레코드를 고유하게 식별하는 primary key는
#User와 Admin 둘다 id로 식별을 하기로 하였음.