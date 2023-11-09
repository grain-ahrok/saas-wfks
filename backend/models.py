from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Config:
    SQLALCHEMY_DATABASE_URI= 'mysql://username:password@localhost/db_name'# 여기에 자신의 MySQL 정보를 넣어주세요.
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(32))
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    membership = db.Column(db.Enum('basic', 'premium'))
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    
    #실제 데이터는 쌓이지 않고 관계를 나타내게 함으로써 메모리 사용량 줄이고 성능 향상
    domains = db.relationship('Domain', backref='user', lazy=True)
    applications = db.relationship('UserApplication', backref='user', lazy=True)
    
    
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
        

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_at = db.Column(db.TIMESTAMP)
    
class UserApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wf_app_id = db.Column(db.Integer)
    security_policy_id = db.Column(db.Integer, db.ForeignKey('security_policy.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    protocol = db.Column(db.Enum('http', 'https'))
    ip_ver = db.Column(db.Enum('ipv4', 'ipv6'))
    ip_addr = db.Column(db.String(40))
    port = db.Column(db.Integer)
    updated_at = db.Column(db.TIMESTAMP)
    
class SecurityPolicy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wf_security_policy_id = db.Column(db.Integer)
    request_count = db.Column(db.Integer)
    sql_injection = db.Column(db.Enum('exception', 'detect', 'block'))
    url_regex = db.Column(db.Enum('exception', 'detect', 'block'))
    xss = db.Column(db.Enum('exception', 'detect', 'block'))
    directory_listing = db.Column(db.Enum('exception', 'detect', 'block'))
    shellcode = db.Column(db.Enum('exception', 'detect', 'block'))
    download = db.Column(db.Enum('exception', 'detect', 'block'))
    uploadfile = db.Column(db.Enum('exception', 'detect', 'block'))
    access_control = db.Column(db.Enum('exception', 'detect', 'block'))
    evasion = db.Column(db.Enum('exception', 'detect', 'block'))
    credential_stuffing = db.Column(db.Enum('exception', 'detect', 'block'))
    cookie_protection = db.Column(db.Enum('exception', 'detect', 'block'))
    buffer_overflow = db.Column(db.Enum('exception', 'detect', 'block'))
    updated_at = db.Column(db.TIMESTAMP)
    
    urls = db.relationship('SpUrl', backref='security_policy', lazy=True)
    ips = db.relationship('SpIp', backref='security_policy', lazy=True)

class SpUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    security_policy_id = db.Column(db.Integer, db.ForeignKey('security_policy.id'), nullable=False)
    url = db.Column(db.String(256))
    classification = db.Column(db.Enum('apply', 'exception'))
    desc = db.Column(db.String(32))
    updated_at = db.Column(db.TIMESTAMP)
    
class SpIp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    security_policy_id = db.Column(db.Integer, db.ForeignKey('security_policy.id'), nullable=False)
    ip_ver = db.Column(db.Enum('ipv4', 'ipv6'))
    ip_addr = db.Column(db.String(40))
    subnet_mask = db.Column(db.String(40))
    classification = db.Column(db.Enum('block', 'apply', 'exception'))
    desc = db.Column(db.String(32))
    updated_at = db.Column(db.TIMESTAMP)
