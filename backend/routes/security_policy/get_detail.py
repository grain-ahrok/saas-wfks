from flask import Flask
import json
from flask import Blueprint
from automic_setting import generate_token, make_api_request
from response.dto.security_policy_dto import SecurityPolicyDto
from response.headers import create_response


security_policy_detail_ = Blueprint('security_policy_detail', __name__, url_prefix='/security_policy')
base_url = 'https://wf.awstest.piolink.net:8443/api/v3'

def createHeader() :
    return {'Authorization': 'token ' + generate_token()}


## 정책 상세 괸리 - 시그니처 기반
## 정책 상세 관리 - SQL injection
@security_policy_detail_.route('/<int:security_policy_id>/sql_injection', methods=['GET'])
def get_policy_sql_injection(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/sql_injection", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    

## 정책 상세 관리 - url_regex
@security_policy_detail_.route('/<int:security_policy_id>/url_regex', methods=['GET'])
def get_policy_url_regex(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/url_regex", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - xss
@security_policy_detail_.route('/<int:security_policy_id>/xss', methods=['GET'])
def get_policy_xss(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/xss", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - directory_listing
@security_policy_detail_.route('/<int:security_policy_id>/directory_listing', methods=['GET'])
def get_policy_directory_listing(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/directory_listing", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    

## 정책 상세 관리 - shellcode
@security_policy_detail_.route('/<int:security_policy_id>/shellcode', methods=['GET'])
def get_policy_shellcode(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/shellcode", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    

## 정책 상세 관리 - access_control
@security_policy_detail_.route('/<int:security_policy_id>/access_control', methods=['GET'])
def get_policy_access_control(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/access_control", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['sig_list'][0]['status'], sig_list=data['sig_list'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## GET securilty-policty up-down load
@security_policy_detail_.route('/<int:security_policy_id>/up_download', methods=['GET'])
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
@security_policy_detail_.route('/<int:security_policy_id>/request_flood', methods=['GET'])
def get_policy_request_flood(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/request_flood", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['adv_options']['proxy_status'], adv_options=data['adv_options'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - evasion
@security_policy_detail_.route('/<int:security_policy_id>/evasion', methods=['GET'])
def get_policy_evasion(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/evasion", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['adv_options']['enable_tildotslash'], adv_options=data['adv_options'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - credential_stuffing
@security_policy_detail_.route('/<int:security_policy_id>/credential_stuffing', methods=['GET'])
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
@security_policy_detail_.route('/<int:security_policy_id>/cookie_protection', methods=['GET'])
def get_policy_cookie_protection(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/cookie_protection", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['adv_options']['hijack_status'], adv_options=data['adv_options'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)


## 정책 상세 관리 - buffer_overflow
@security_policy_detail_.route('/<int:security_policy_id>/buffer_overflow', methods=['GET'])
def get_policy_buffer_overflow(security_policy_id) : 
    try : 
        response = make_api_request(f"{base_url}/security_policy/{security_policy_id}/buffer_overflow", method='GET', headers=createHeader())
        data = json.loads(response.content.decode('utf-8'))
        spDto = SecurityPolicyDto(status=data['adv_options']['header_length_status'], adv_options=data['adv_options'])
        return create_response(data=spDto.__dict__)
    except Exception as e:
        return create_response(success=True, message=e, status_code = 500)
    
