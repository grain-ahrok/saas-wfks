from flask import Blueprint, request, jsonify, redirect, url_for
from models import Admin
from utils import bcrypt

admin = Blueprint('admin', __name__, url_prefix='/admin')

# 관리자 로그인 API
@admin.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    #admin 변수는 db 쿼리 결과로서 Admin객체를 나타냄.
    admin = Admin.query.filter_by(username=username).first()

    if admin:
        if bcrypt.check_password_hash(admin.password, password):
            # 로그인에 성공했을 때 필요하면 로직 구현
            # 관리자 페이지로 리다이렉션합니다.
            return redirect(url_for('admin.admin_page'))
        else:
            return jsonify({"message": "Login failed. Invalid credentials."}), 401
    else:
        return jsonify({"message": "Login failed. User not found."}), 401

@admin.route('/admin_page', methods=['GET'])
def admin_page():
    # 관리자 페이지에 대한 로직을 여기에 추가
    return "Welcome to the admin page!"
