from flask import Blueprint, jsonify, request
import requests
from utils import make_api_request,basic_auth
from flask_jwt_extended import jwt_required

security_policy_ = Blueprint('security_policy', __name__, url_prefix='/security_policy')
base_url = 'https://wf.awstest.piolink.net:8443/api/v3'

headers = basic_auth()

def createHeader() :
    return basic_auth()

# @security_policy_.before_request
# def before_request():
#     jwt_required()  # Call jwt_required directly within the before_request function

policy_names = ["buffer_overflow","request_flood","evasion","cookie_protection","credential_stuffing"]

@security_policy_.route('/<int:security_policy_id>/exception_url_list', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def exception_url(security_policy_id):
    
    headers = basic_auth()
    try:
        if request.method == 'GET':
            url = f'{base_url}/security_policy/{security_policy_id}/sql_injection/exception_url_list'
            response = make_api_request(url, method='GET', headers=headers)
            return response.json()

        elif request.method == 'POST':
            data = request.json
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/exception_url_list'
                post_data = [
                    {
                        "status": "enable",
                        "url": data.get('url'),
                        "desc": data.get('desc')
                    }
                ]
                response = make_api_request(url, method='POST', data=post_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
        elif request.method == 'PUT':
            data = request.json
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/exception_url_list'
                put_data = [
                    {
                        "status": "enable",
                        "id": request.args.get('id'),
                        "url": data.get('url'),
                        "desc": data.get('desc')
                    }
                ]
                response = make_api_request(url, method='PUT', data=put_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
        elif request.method == 'DELETE':
            data = request.json()
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/exception_url_list'
                ids = data.get('ids', [])  
                delete_data = [{'id': id} for id in ids]
                response = make_api_request(url, method='DELETE', data=delete_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
    except requests.exceptions.RequestException as e:
        # API 요청 중에 오류가 발생한 경우 처리
        error_message = f"API 요청 중 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500

    except Exception as e:
        # 기타 예외가 발생한 경우 처리
        error_message = f"알 수 없는 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500
    
@security_policy_.route('/<int:security_policy_id>/exception_ip_list', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def exception_ip_list(security_policy_id):
    headers = basic_auth()

    try:
        if request.method == 'GET':
            url = f'{base_url}/security_policy/{security_policy_id}/sql_injection/exception_ip_list'
            response = make_api_request(url, method='GET', headers=headers)
            return response.json()

        elif request.method == 'POST':
            data = request.json
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/exception_ip_list'
                post_data = [
                        {
                            "status": "enable",
                            "version": data.get('version'),
                            "client_ip": data.get('client_ip'),
                            "server_ip": data.get('server_ip'),
                            "desc": data.get('desc')
                        }
                ]
                response = make_api_request(url, method='POST', data=post_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
        elif request.method == 'PUT':
            data = request.json
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/exception_ip_list'
                put_data = [
                    {
                        "id": request.args.get('id'),
                        "status": "enable",
                        "version": data.get('version'),
                        "client_ip": data.get('client_ip'),
                        "client_mask": data.get('client_mask'),
                        "server_ip": data.get('server_ip'),
                        "server_mask": data.get('server_mask'),
                        "desc": data.get('desc')
                    }
                ]
                response = make_api_request(url, method='PUT', data=put_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
        elif request.method == 'DELETE':
            data = request.json()
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/exception_ip_list'
                ids = data.get('ids', [])  
                delete_data = [{'id': id} for id in ids]
                response = make_api_request(url, method='DELETE', data=delete_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
    except requests.exceptions.RequestException as e:
        # API 요청 중에 오류가 발생한 경우 처리
        error_message = f"API 요청 중 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500

    except Exception as e:
        # 기타 예외가 발생한 경우 처리
        error_message = f"알 수 없는 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500
    
@security_policy_.route('/<int:security_policy_id>/apply_url_list', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def apply_url_list(security_policy_id):
    headers = basic_auth()

    try:
        if request.method == 'GET':
            url = f'{base_url}/security_policy/{security_policy_id}/sql_injection/apply_url_list'
            response = make_api_request(url, method='GET', headers=headers)
            return response.json()

        elif request.method == 'POST':
            data = request.json
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/apply_url_list'
                post_data = [
                    {
                        "status": "enable",
                        "url": data.get('url'),
                        "desc": data.get('desc')
                    }
                ]
                response = make_api_request(url, method='POST', data=post_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
        elif request.method == 'PUT':
            data = request.json
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/apply_url_list'
                put_data = [
                    {
                        "status": "enable",
                        "id": request.args.get('id'),
                        "url": data.get('url'),
                        "desc": data.get('desc')
                    }
                ]
                response = make_api_request(url, method='PUT', data=put_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
        elif request.method == 'DELETE':
            data = request.json()
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/apply_url_list'
                ids = data.get('ids', [])  
                delete_data = [{'id': id} for id in ids]
                response = make_api_request(url, method='DELETE', data=delete_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
    except requests.exceptions.RequestException as e:
        # API 요청 중에 오류가 발생한 경우 처리
        error_message = f"API 요청 중 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500

    except Exception as e:
        # 기타 예외가 발생한 경우 처리
        error_message = f"알 수 없는 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500
    
    
@security_policy_.route('/<int:security_policy_id>/apply_ip_list', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def apply_ip_list(security_policy_id):
    headers = basic_auth()

    try:
        if request.method == 'GET':
            url = f'{base_url}/security_policy/{security_policy_id}/sql_injection/apply_ip_list'
            response = make_api_request(url, method='GET', headers=headers)
            return response.json()

        elif request.method == 'POST':
            data = request.json
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/apply_ip_list'
                post_data = [
                        {
                            "status": "enable",
                            "version": data.get('version'),
                            "client_ip": data.get('client_ip'),
                            "server_ip": data.get('server_ip'),
                            "desc": data.get('desc')
                        }
                ]
                response = make_api_request(url, method='POST', data=post_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
        elif request.method == 'PUT':
            data = request.json
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/apply_ip_list'
                put_data = [
                    {
                        "id": request.args.get('id'),
                        "status": "enable",
                        "version": data.get('version'),
                        "client_ip": data.get('client_ip'),
                        "client_mask": data.get('client_mask'),
                        "server_ip": data.get('server_ip'),
                        "server_mask": data.get('server_mask'),
                        "desc": data.get('desc')
                    }
                ]
                response = make_api_request(url, method='PUT', data=put_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
        elif request.method == 'DELETE':
            data = request.json()
            for policy_name in policy_names:
                url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}/apply_ip_list'
                ids = data.get('ids', [])  
                delete_data = [{'id': id} for id in ids]
                response = make_api_request(url, method='DELETE', data=delete_data, headers=headers)
                print(f"Policy: {policy_name}, Success: {response.content}")
            return response.json()
    except requests.exceptions.RequestException as e:
        # API 요청 중에 오류가 발생한 경우 처리
        error_message = f"API 요청 중 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500

    except Exception as e:
        # 기타 예외가 발생한 경우 처리
        error_message = f"알 수 없는 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500
    


@security_policy_.route('/<int:security_policy_id>/block_ip_filter/ip_list', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def block_ip_filter(security_policy_id):
    headers = basic_auth()

    try:
        if request.method == 'GET':
            url = f'{base_url}/system/block_ip_filter/ip_list'
            response = make_api_request(url, method='GET', headers=headers)
            return response.json()

        elif request.method == 'POST':
            data = request.json
            url = f'{base_url}/system/block_ip_filter/ip_list'
            post_data = {
                "client_ip": data.get('client_ip'),
                "client_mask":data.get('client_mask'),
                "desc":data.get('desc')
            }
            response = make_api_request(url, method='POST', data=post_data, headers=headers)
            print(f"block_ip_filter: {response.content}")
            return response.json()
        elif request.method == 'PUT':
            data = request.json
            
            url = f'{base_url}/system/block_ip_filter/ip_list'
            put_data = {
                "id": request.args.get('id'),
                "client_ip": data.get('client_ip'),
                "client_mask": data.get('client_mask'),
                "time": 15,
                "timeunit": "second",
                "permanent_status": "disable",
                "desc": data.get('desc')
            }
            response = make_api_request(url, method='PUT', data=put_data, headers=headers)
            print(f"block_ip_filter: {response.content}")
            return response.json()
        elif request.method == 'DELETE':
            data = request.json()
            url = f'{base_url}/system/block_ip_filter/ip_list'
            ids = data.get('ids', [])  
            delete_data = [{'id': id} for id in ids]
            response = make_api_request(url, method='DELETE', data=delete_data, headers=headers)
            print(f"block_ip_filter: {response.content}")
            return response.json()
    except requests.exceptions.RequestException as e:
        # API 요청 중에 오류가 발생한 경우 처리
        error_message = f"API 요청 중 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500

    except Exception as e:
        # 기타 예외가 발생한 경우 처리
        error_message = f"알 수 없는 오류 발생: {str(e)}"
        return jsonify({'error': error_message}), 500
    

    

@security_policy_.route('/security-settings/policy-details/<policy_name>/information', methods=['GET'])
@jwt_required()
def get_policy_infomation_signature(policy_name):
    external_url = "https://wf.awstest.piolink.net:8443/api/kui/api/v3/information/signature"
    headers = basic_auth()
    response = make_api_request(external_url, 'GET', headers)

    if response is not None and response.status_code == 200:
        data = response.json()
        print(data)
        # extracted_data = [
        #     {
        #         "origin_sig_id": item.get("origin_sig_id"),
        #         "severity": item.get("severity"),
        #         "ko_description": item.get("ko_description"),
        #         "poc_example": item.get("poc_example")
        #     }
        #     for item in data
        # ]
        return data
    return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500
    