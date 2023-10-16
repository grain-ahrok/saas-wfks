from flask import Blueprint, request, jsonify
from models import db, Admin
from utils import bcrypt

app = Blueprint('admin', __name__, url_prefix='/admin')

# 관리자 로그인 API
@app.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()

    if admin and bcrypt.check_password_hash(admin.password, password):
        return jsonify({"message": "Login successful."}), 200
    else:
        return jsonify({"message": "Login failed. Invalid credentials."}), 401
