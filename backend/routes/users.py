# routes.py
from flask import Blueprint, request, jsonify, current_app
from models import db, User
import jwt
import time
from utils import hash_password, bcrypt, invalid_tokens

app = Blueprint('users', __name__, url_prefix='/users')

# 회원 가입 API
@app.route('/signup', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = hash_password(data['password'])
    # None 상태로 저장하지 않고 빈 문자열로 변경
    membership = ''
    new_user = User(
        companyName=data['companyName'],
        email=data['email'],
        password=hashed_password,
        domain_address=data['domain_address'],
        IP_address=data['IP_address'],
        membership=membership
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201

# 엑세스 토큰 생성 함수 (유효시간 30분)
def generate_access_token(membership):
    if membership == '':
        membership = "비회원"
    expiration_time = time.time() + 1800
    token = {
        "membership": membership,
        "exp": expiration_time
    }
    access_token = jwt.encode(token, current_app.config['SECRET_KEY'], algorithm='HS256')
    return access_token

# 로그인 API
@app.route('/login', methods=['POST'])
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
@app.route('/users', methods=['GET'])
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

# API 엔드포인트: 사용자 정보 조회
@app.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            'id': user.id,
            'companyName': user.companyName,
            'email': user.email,
            'password': user.password,
            'domain_address': user.domain_address,
            'IP_address': user.IP_address,
            'membership': user.membership
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found.'}), 404

# API 엔드포인트: 사용자 정보 수정
@app.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if user:
        user.companyName = data.get('companyName', user.companyName)
        user.email = data.get('email', user.email)
        user.domain_address = data.get('domain_address', user.domain_address)
        user.IP_address = data.get('IP_address', user.IP_address)
        user.membership = data.get('membership', user.membership)

        db.session.commit()
        return jsonify({'message': 'User updated successfully.'}), 200
    else:
        return jsonify({'message': 'User not found.'}), 404

# API 엔드포인트: 비밀번호 변경
@app.route('/<int:user_id>/change_password', methods=['POST'])
def change_password(user_id):
    data = request.get_json()
    new_password = data.get('new_password')

    user = User.query.get(user_id)
    if user:
        user.password = hash_password(new_password)
        db.session.commit()
        return jsonify({'message': 'Password changed successfully.'}), 200
    else:
        return jsonify({'message': 'User not found.'}), 404

# API 엔드포인트: 로그아웃 (토큰 무효화)
@app.route('/logout', methods=['POST'])
def logout():
    access_token = request.headers.get('Authorization')
    if access_token and access_token.startswith('Bearer '):
        access_token = access_token.split(' ')[1]
        invalid_tokens.add(access_token)
        return jsonify({'message': 'Logout successful.'}), 200
    else:
        return jsonify({'message': 'Invalid access token.'}), 400

# 회원 탈퇴 API
@app.route('/<int:user_id>', methods=['DELETE'])
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
