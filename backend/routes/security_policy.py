from flask import Blueprint, session, jsonify, request
import requests
from utils import make_api_request,generate_token,determine_ip_version
import json
import urllib3
from models.domain import Domain,datetime
from models.log import Log
from models.user_application import UserApplication
from models.security_policy import SecurityPolicy
import base64

security_policy_ = Blueprint('security_policy', __name__, url_prefix='/security_policy')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #지우시요 나중에
policy_names = ["sql_injection","buffer_overflow","request_flood","evasion","cookie_protection","directory_listing","download","url_regex","xss","shellcode","upload","access_control","credential_stuffing"]
@security_policy_.route('/<int:security_policy_id>/<policy_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_policy_details(security_policy_id, policy_name):
    url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}'
    filename = 'backend/json/security_policy_name.json'
    
    with open(filename, 'r') as json_file:
        policy_data_extractors = json.load(json_file)
    
    setting_names = policy_data_extractors[policy_name]
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

    try:
        if request.method == 'GET':
            result = {'result': {'status': 'unknown'}}
            
            if isinstance(setting_names, list):
                for setting_name in setting_names:
                    ex_url = f'{url}/{setting_name}'
                    response = make_api_request(ex_url, method='GET', headers=headers)
                    data = response.json()
                    
                    if policy_name == 'credential_stuffing':
                        result['result'][setting_name] = data
                        result['result']['status'] = data.get('action', 'unknown')
                    else:
                        status_key_value_pair = next((item for item in data.items() if item[0].endswith("_status")), None)
                        
                        if status_key_value_pair:
                            _, status_value = status_key_value_pair
                            
                        result['result'][setting_name] = data
                        result['result']['status'] = status_value
                
                return result
            else:
                url = f'{url}/{setting_names}'
                response = make_api_request(url, method='GET', headers=headers)
                data = response.json()
                result['result'][setting_names] = data
                
                if setting_names == 'sig_list':
                    result['result']['status'] = data[0]['status']
                else:
                    status_key_value_pair = next((item for item in data.items() if item[0].endswith("_status")), None)
                    
                    if status_key_value_pair:
                        _, status_value = status_key_value_pair
                        
                    result['result']['status'] = status_value
                    
                return result

        elif request.method == 'PUT':
            data = request.json
            status = data.get('status')

            if isinstance(setting_names, list):
                for setting_name in setting_names:
                    ex_url = f'{url}/{setting_name}'
                    response = make_api_request(ex_url, "GET", headers)
                    security_policy_json = response.json()

                    if policy_name == 'credential_stuffing':
                        security_policy_json['action'] = status
                        response = make_api_request(ex_url, method='PUT', headers=headers, data=security_policy_json)
                    else:
                        if setting_name == "adv_options":
                            keys_to_include = ["session_user_define_time", "proxy_request_count", "session_request_count", "proxy_user_define_time"]
                            updated_data = {key: int(request.args.get(key)) for key in keys_to_include if request.args.get(key) is not None}
                            updated_data.update({key: status for key, value in security_policy_json.items() if key.endswith("_status") and isinstance(value, str)})
                            response = make_api_request(ex_url, method='PUT', headers=headers, data=updated_data)
                        else:
                            updated_data = {key: status for key, value in security_policy_json.items() if key.endswith("_status") and isinstance(value, str)}
                            response = make_api_request(ex_url, method='PUT', headers=headers, data=updated_data)
            else:
                ex_url = f'{url}/{setting_names}'
                response = make_api_request(ex_url, "GET", headers)
                security_policy_json = response.json()

                if setting_names == 'sig_list':
                    updated_data = [{"id": item.get("id"), "status": status, "block_id": item.get("block_id")} for item in security_policy_json]
                    response = make_api_request(ex_url, method='PUT', headers=headers, data=updated_data)
                elif isinstance(security_policy_json, dict):
                    updated_data = {key: status for key, value in security_policy_json.items() if key.endswith("_status") and isinstance(value, str)}
                    response = make_api_request(ex_url, method='PUT', headers=headers, data=updated_data)

            sp = SecurityPolicy.update_security_policy_by_wf_id(security_policy_id, policy_name=status)
            return response.json()

    except requests.exceptions.RequestException as e:
        # API 요청 중에 오류가 발생한 경우 처리
        error_message = f"API 요청 중 오류 발생: {str(e)}"
        print(f"Error: {error_message}")
        return jsonify({'error': error_message}), 500

    except Exception as e:
        # 기타 예외가 발생한 경우 처리
        error_message = f"알 수 없는 오류 발생: {str(e)}"
        print(f"Error: {error_message}")
        return jsonify({'error': error_message}), 500


@security_policy_.route('/<int:security_policy_id>/exception_url_list', methods=['GET', 'POST', 'PUT', 'DELETE'])
def exception_url(security_policy_id):
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

    try:
        if request.method == 'GET':
            url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/sql_injection/exception_url_list'
            response = make_api_request(url, method='GET', headers=headers)
            return response.json()

        elif request.method == 'POST':
            data = request.json
            for policy_name in policy_names:
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/exception_url_list'
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
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/exception_url_list'
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
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/exception_url_list'
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
def exception_ip_list(security_policy_id):
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

    try:
        if request.method == 'GET':
            url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/sql_injection/exception_ip_list'
            response = make_api_request(url, method='GET', headers=headers)
            return response.json()

        elif request.method == 'POST':
            data = request.json
            for policy_name in policy_names:
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/exception_ip_list'
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
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/exception_ip_list'
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
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/exception_ip_list'
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
def apply_url_list(security_policy_id):
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

    try:
        if request.method == 'GET':
            url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/sql_injection/apply_url_list'
            response = make_api_request(url, method='GET', headers=headers)
            return response.json()

        elif request.method == 'POST':
            data = request.json
            for policy_name in policy_names:
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/apply_url_list'
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
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/apply_url_list'
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
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/apply_url_list'
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
def apply_ip_list(security_policy_id):
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

    try:
        if request.method == 'GET':
            url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/sql_injection/apply_ip_list'
            response = make_api_request(url, method='GET', headers=headers)
            return response.json()

        elif request.method == 'POST':
            data = request.json
            for policy_name in policy_names:
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/apply_ip_list'
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
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/apply_ip_list'
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
                url = f'https://wf.awstest.piolink.net:8443/api/v3/security_policy/{security_policy_id}/{policy_name}/apply_ip_list'
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