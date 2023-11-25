from response.headers import create_response
from flask import Blueprint, session, jsonify, request
from response.dto.security_policy_dto import SecurityPolicyDto
import requests
from utils import make_api_request,generate_token
import json
import urllib3
from models.domain import Domain,datetime
from models.log import Log
from models.user_application import UserApplication
from models.security_policy import SecurityPolicy
import base64
from flask_jwt_extended import jwt_required

security_policy_ = Blueprint('security_policy', __name__, url_prefix='/security_policy')
base_url = 'https://wf.awstest.piolink.net:8443/api/v3'
token = generate_token()
headers = {'Authorization': 'token ' + generate_token()}

# @security_policy_.before_request
# def before_request():
#     jwt_required()  # Call jwt_required directly within the before_request function

def createHeader() :
    return {'Authorization': 'token ' + generate_token()}


## 정책 상세 괸리 - 시그니처 기반
## 정책 상세 관리 - SQL injection
@security_policy_.route('/<int:security_policy_id>/sql_injection', methods=['GET'])
def get_policy_sql_injection(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/sql_injection", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    

## 정책 상세 관리 - url_regex
@security_policy_.route('/<int:security_policy_id>/url_regex', methods=['GET'])
def get_policy_url_regex(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/url_regex", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - xss
@security_policy_.route('/<int:security_policy_id>/xss', methods=['GET'])
def get_policy_xss(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/xss", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - directory_listing
@security_policy_.route('/<int:security_policy_id>/directory_listing', methods=['GET'])
def get_policy_directory_listing(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/directory_listing", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    

## 정책 상세 관리 - shellcode
@security_policy_.route('/<int:security_policy_id>/shellcode', methods=['GET'])
def get_policy_shellcode(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/shellcode", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    

## 정책 상세 관리 - access_control
@security_policy_.route('/<int:security_policy_id>/access_control', methods=['GET'])
def get_policy_access_control(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/access_control", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## GET securilty-policty up-down load
@security_policy_.route('/<int:security_policy_id>/up_download', methods=['GET'])
def get_policy_updownload(security_policy_id) : 
    try : 
        response_down = make_api_request(f"{base_url}/security_policy/{security_policy_id}/download", method='GET', headers=createHeader())
        response_up = make_api_request(f"{base_url}/security_policy/{security_policy_id}/upload", method='GET', headers=createHeader())
        data_down = json.loads(response_down.content.decode('utf-8'))
        data_up = json.loads(response_up.content.decode('utf-8'))
        data = data_down['sig_list'] + data_up['sig_list']
        spDto = SecurityPolicyDto(status=data_down['sig_list'][0]['status'], sig_list=data)
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    

## 정책 상세 괸리 - 옵션 기반
## 정책 상세 관리 - evasion
@security_policy_.route('/<int:security_policy_id>/request_flood', methods=['GET'])
def get_policy_request_flood(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/request_flood", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['adv_options']['proxy_status'], adv_options=data['adv_options'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - evasion
@security_policy_.route('/<int:security_policy_id>/evasion', methods=['GET'])
def get_policy_evasion(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/evasion", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['adv_options']['enable_tildotslash'], adv_options=data['adv_options'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - credential_stuffing
@security_policy_.route('/<int:security_policy_id>/credential_stuffing', methods=['GET'])
def get_policy_credential_stuffing(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/credential_stuffing", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        adv_options = { "success_rule": data['success_rule'], "fail_rule" : data['fail_rule']}
        spDto = SecurityPolicyDto(status=data['success_rule']['action'], adv_options=adv_options)
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    

## 정책 상세 관리 - cookie_protection
@security_policy_.route('/<int:security_policy_id>/cookie_protection', methods=['GET'])
def get_policy_cookie_protection(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/cookie_protection", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['adv_options']['hijack_status'], adv_options=data['adv_options'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - buffer_overflow
@security_policy_.route('/<int:security_policy_id>/buffer_overflow', methods=['GET'])
def get_policy_buffer_overflow(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/buffer_overflow", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['adv_options']['header_length_status'], adv_options=data['adv_options'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #지우시요 나중에
policy_names = ["buffer_overflow","request_flood","evasion","cookie_protection","credential_stuffing"]
@security_policy_.route('/<int:security_policy_id>/<policy_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_policy_details(security_policy_id, policy_name):

    url = f'{base_url}/security_policy/{security_policy_id}/{policy_name}'
    filename = './json/security_policy_name.json'
    
    with open(filename, 'r') as json_file:
        policy_data_extractors = json.load(json_file)
    
    setting_names = policy_data_extractors[policy_name]
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

    try:

        if request.method == 'PUT':

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

            # sp = SecurityPolicy.update_security_policy_by_wf_id(security_policy_id, policy_name=status)
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
def exception_ip_list(security_policy_id):
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

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
def apply_url_list(security_policy_id):
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

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
def apply_ip_list(security_policy_id):
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

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
def block_ip_filter(security_policy_id):
    token = generate_token()
    headers = {'Authorization': 'token ' + token}

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
def get_policy_infomation_signature(policy_name):
    external_url = "https://wf.awstest.piolink.net:8443/api/kui/api/v3/information/signature"
    token = generate_token()
    headers = {'Authorization': 'token ' + token}
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
    