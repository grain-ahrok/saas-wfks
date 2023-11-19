from flask import Blueprint, request, jsonify,session
from models.user import User
from models import *
from utils import *
import urllib3
import automic_setting

users = Blueprint('users', __name__, url_prefix='/users')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #지우시요 나중에

@users.route('/signup', methods=['POST'])
def register():
    data = request.get_json()
    user_data = {
        "companyName":data.get('companyName'),
        "email":data.get('email'),
        "password":data.get('password'),
        "membership":data.get('membership')
    }
    user = User.create(**user_data)
    automic_setting.automic_setting(data,user.id)
    
    return jsonify({"message": "User registered successfully.", "user_id": user.id}), 201
    
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
                token = generate_token()

                if token:
                    session['token'] = token
                    session['user_id'] = user.id
                    session['ip'] = data.get('IP_address')
                    session['companyName'] = data.get('companyName')
                    session['domain_address'] = data.get('doamin_address')
                    #session['app_id'] = 
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
    if 'user_id' in session:
        # Clear the user's session data
        session.pop('user_id', None)
        session.pop('token', None)
        session.pop('ip', None)
        session.pop('domain_address', None)
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
    

@users.route('/<int:user_id>/forgot_password', methods=['POST'])
def forgot_password(user_id):
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter((User.id == user_id) & (User.email == email)).first()

    if user:
        user.send_temporary_password()
        return jsonify({"message": "Temporary password sent successfully."}), 200
    else:
        return jsonify({"message": "User not found."}), 404
    
