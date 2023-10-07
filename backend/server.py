from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # 시크릿 키 설정
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
invalid_tokens = set()  # 유효하지 않은 토큰 저장을 위한 set

# User 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    domain_address = db.Column(db.String(255))
    IP_address = db.Column(db.String(15))
    membership = db.Column(db.String(20))

# 비밀번호 해시화 함수
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# 회원 가입 API
@app.route('/users/signup', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = hash_password(data['password'])  # 비밀번호를 해시화
    new_user = User(
        companyName=data['companyName'],
        email=data['email'],
        password=hashed_password,  # 해시화된 비밀번호 저장
        domain_address=data['domain_address'],
        IP_address=data['IP_address'],
        membership=data['membership']
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201

# 엑세스 토큰 생성 함수 (유효시간 30분)
def generate_access_token(membership):
    expiration_time = time.time() + 1800  # 현재 시간으로부터 30분 후
    token = {
        "membership": membership,
        "exp": expiration_time
    }
    access_token = jwt.encode(token, app.config['SECRET_KEY'], algorithm='HS256')
    return access_token

# 로그인 API
@app.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = generate_access_token(user.membership)
        return jsonify({"id": user.id, "accessToken": access_token}), 200
    else:
        return jsonify({"message": "Login failed. Invalid credentials."}), 401

# 모든 회원 정보 조회 API
@app.route('/users/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'companyName': user.companyName,
            'email': user.email,
            'password' : user.password,
            'domain_address': user.domain_address,
            'IP_address': user.IP_address,
            'membership': user.membership
        }
        user_list.append(user_data)

    return jsonify({'users': user_list}), 200

# 간단한 인증 미들웨어 (토큰 유효성 검증)
def authorize_user(request):
    access_token = request.headers.get('Authorization')
    if access_token and access_token.startswith('Bearer '):
        access_token = access_token.split(' ')[1]

        if access_token in invalid_tokens:
            return None

        try:
            decoded_token = jwt.decode(access_token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return access_token
        except jwt.ExpiredSignatureError:
            invalid_tokens.add(access_token)
            return None

    return None

# 회원 탈퇴 API
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    access_token = authorize_user(request)
    if not access_token:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        decoded_token = jwt.decode(access_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": f"User {user_id} deleted successfully."}), 200
        else:
            return jsonify({"error": "User not found."}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired. Please log in again."}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
