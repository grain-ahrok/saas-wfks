from flask import Blueprint, request, jsonify,session
from models import db, User
from utils import bcrypt,login_with_external_server

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/signup', methods=['POST'])
def register():
    data = request.get_json()
    user = User.create(**data)
    return jsonify({"message": "User registered successfully.", "user_id": user.id}), 201
    # /kui/api/v3/system/account/manager/user_list waf사이트 아이디 생성 API
@users.route('/signin', methods=['POST'])
def login():
    data = request.get_json()
    companyName = data.get('companyName')
    password = data.get('password')

    user = User.query.filter_by(companyName=companyName).first()

    if user and bcrypt.check_password_hash(user.password, password):
        if user.membership == 'Basic':
            try:
                #토큰 생성
                access_token, refresh_token = login_with_external_server()

                if access_token and refresh_token:
                    session['token'] = access_token
                    session['refresh_token'] = refresh_token
                    session['id'] = user.id
                    session['ip'] = user.IP_address
                    return jsonify({"id": user.id, "message": "Login successful."}), 200
                else:
                    return jsonify({"message": "Login failed. External server error."}), 401
            except Exception as e:
                # 예외 처리: 원격 서버와의 통신에 문제가 있을 경우
                return jsonify({"message": f"Login failed. {str(e)}"}), 401
        else:
            return jsonify({"message": "Login failed. Membership is not 'basic'."}), 401
    else:
        return jsonify({"message": "Login failed. Invalid credentials."}), 401

@users.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [
        {
            'id': user.id,
            'companyName': user.companyName,
            'email': user.email,
            'password': user.password,
            'domain_address': user.domain_address,
            'IP_address': user.IP_address,
            'Port_number': user.Port_number,
            'membership': user.membership
        } for user in users
    ]
    return jsonify({'users': user_list}), 200

@users.route('/<int:user_id>', methods=['GET'])
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
            'Port_number': user.Port_number,
            'membership': user.membership
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found.'}), 404

@users.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.update(**data)
        return jsonify({'message': 'User updated successfully.'}), 200
    else:
        return jsonify({'message': 'User not found.'}), 404

@users.route('/<int:user_id>/change_password', methods=['POST'])
def change_password(user_id):
    data = request.get_json()
    new_password = data.get('new_password')
    user = User.query.get(user_id)
    if user:
        user.change_password(new_password)
        return jsonify({'message': 'Password changed successfully.'}), 200
    else:
        return jsonify({'message': 'User not found.'}), 404

@users.route('/logout', methods=['POST'])
def logout():
    # Implement your logout logic here
    return jsonify({'message': 'Logout successful.'}), 200

@users.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user_id} deleted successfully."}), 200
    else:
        return jsonify({"error": "User not found."}), 404
    
