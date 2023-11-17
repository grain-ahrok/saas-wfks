from flask import Blueprint, session, jsonify, request
import requests
from utils import make_api_request
import json
import urllib3
from models.domain import Domain,datetime

customer = Blueprint('customer', __name__, url_prefix='/customer')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #지우시요 나중에

def fetch_dashboard_data(data_type):
    url = 'https://wf.awstest.piolink.net:8443/cgi-bin/dashboard/'
    with open('backend/json/dashboard_data.json', 'r', encoding='utf-8') as json_file:
        dashboard_data = json.load(json_file)

    data = dashboard_data.get(data_type)
    cookies = {'PB_LANG': 'ko', 'UI': 'wafwaf'}
    response = requests.post(url, data=data,verify=False,cookies=cookies)
    response.raise_for_status() 
    response_content = response.content.decode('utf-8')
    
    return json.loads(response_content)

@customer.route('/dashboard', methods=['GET'])
def dashboard():
    data_timeline_response = fetch_dashboard_data("data_timeline")
    data_pie_response = fetch_dashboard_data("data_pie")
    data_name_time_response = fetch_dashboard_data("data_name_time")
    
    if data_timeline_response and data_pie_response and data_name_time_response:
        response_data = {
            "timeline_data": data_timeline_response,
            "pie_data": data_pie_response,
            "name_time": data_name_time_response
        }
        return jsonify(response_data)

    return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500


@customer.route('/security-logs', methods=['GET'])
def security_logs():
    url = 'https://wf.awstest.piolink.net:8443/cgi-bin/logviewer/'
    headers = {'Cookie': 'PB_LANG=ko; UI=wafwaf'}
    data = {'log_type': 'security','param': 'eyJhY3Rpb24iOiJzZWxlY3QiLCJmaWx0ZXIiOnsiZGV0YWlsIjp7fSwiYmFzaWMiOnt9LCJwZXJpb2QiOiI4NjQwMCJ9LCJsaW1pdCI6MTAwLCJwYWdlUGFyYW0iOm51bGx9'} #parm :{"action":"select","filter":{"detail":{},"basic":{},"period":"86400"},"limit":100,"pageParam":null}

    response = requests.post(url, data=data,verify=False,headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500

@customer.route('/domain-settings', methods=['GET', 'PUT', 'POST'])
def manage_domain_settings():
    url = f"https://wf.awstest.piolink.net:8443/kui/api/v3/{session['user_application_id']}/general/domain_list"
    if request.method == 'GET':
        response = make_api_request(url,method='GET')
        return jsonify(response.json())
    elif request.method == 'PUT':
        data = request.json
        data = {
            "status": data.get("status"),
            "domain": data.get("domain"),
            "desc": data.get("desc")
        }
        domain_id = data.get("id")
        domain = Domain.get_domain_by_id(domain_id)
        
        response = make_api_request(url, method='POST', data=data)
        if response.status_code == 200:
            if domain:
                domain.update(
                    status=data.get("status"),
                    name=data.get("domain"),
                    desc=data.get("desc")
                )
                return jsonify({"message": f"Domain with id {domain_id} updated successfully."}), 200
            else:
                return jsonify({"error": f"Domain with id {domain_id} not found."}), 404
        return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500
    
    elif request.method == 'POST':
        data = request.json
        id = data.get("id")
        main_ip = data.get("main_ip")
        setting_ip = data.get("setting_ip")
        port_number = data.get("port_number")
        domain = data.get("domain")
        status = data.get("status")
        desc = data.get("desc")
        data = {
            "status": status,
            "domain": domain,
            "desc": desc
        }
        response = make_api_request(url, method='POST', data=data)
        

        if response.status_code == 200:
            
            new_domain = Domain.create(
                name=data.get("domain"),
                user_application_id=session['user_application_id'],
                updated_at=datetime.utcnow()
            )

        return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500

    elif request.method == 'DELETE':
        data = request.json
        id = data.get("id")
        data = {"id": id}    
        return jsonify(make_api_request(url, method='DELETE', data=data))  


# @customer.route('/security-settings/exception-urls', methods=['GET','POST','PUT','DELETE'])
# def exception_urls():
#     if request.method == 'GET':
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow", method='GET'))    
#     elif request.method == 'POST':
#         data = request.json
#         post_data : {
#             "status": "enable",
#             "url": data.get('url'),
#             "desc": "default"
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow", method='POST', data=post_data))    
#     elif request.method == 'PUT':
#         data = request.json
#         put_data : {
#             "id": data.get('id'),
#             "status": "enable",
#             "url": data.get('url'),
#             "desc": "default"
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow", method='PUT', data=put_data))    
#     elif request.method == 'DELETE':
#         data = request.json
#         delete_data : {
#             "id" : data.get('id')
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow", method='DELETE',data=delete_data))    

# @customer.route('/security-settings/apply-urls',methods=['GET','POST','PUT','DELETE'])
# def apply_urls():
#     if request.method == 'GET':
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_url_list", method='GET'))    
#     elif request.method == 'POST':
#         data = request.json
#         post_data = {
#             "status": "enable",
#             "url": data.get('url'),
#             "desc": "desc"
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_url_list", method='POST', data=post_data))    
#     elif request.method == 'PUT':
#         data = request.json
#         put_data = {
#             "id": data.get('id'),
#             "status": "enable",
#             "url": data.get('url'),
#             "desc": "default"
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_url_list", method='PUT', data=put_data))    
#     elif request.method == 'DELETE':
#         data = request.json
#         delete_data = {
#             "id": data.get('id')
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_url_list", method='DELETE', data=delete_data))    
 
# @customer.route('/security-settings/exception-urls',methods=['GET','POST','PUT','DELETE'])
# def exception_ips():
#     if request.method == 'GET':
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/exception_ip_list", method='GET'))    
#     elif request.method == 'POST':
#         data = request.json
#         post_data = {
#             "status": "enable",
#             "version": "ipv4",
#             "client_ip": data.get('client_ip'),
#             "client_mask": data.get('client_mask'),
#             "server_ip": data.get('server_ip'),
#             "server_mask": data.get('server_mask'),
#             "desc": "desc"
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/exception_ip_list", method='POST', data=post_data))    
#     elif request.method == 'PUT':
#         data = request.json
#         put_data = {
#             "id":data.get('id'),
#             "status": "enable",
#             "version": "ipv4",
#             "client_ip": data.get('client_ip'),
#             "client_mask": data.get('client_mask'),
#             "server_ip": data.get('server_ip'),
#             "server_mask": data.get('server_mask'),
#             "desc": "desc"
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/exception_ip_list", method='PUT', data=put_data))    
#     elif request.method == 'DELETE':
#         data = request.json
#         delete_data = {
#             "id": data.get('id')
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/exception_ip_list", method='DELETE', data=delete_data))    

# @customer.route('/security-settings/apply-ips',methods=['GET','POST','PUT','DELETE'])
# def apply_ips():
#     if request.method == 'GET':
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_ip_list", method='GET'))    
#     elif request.method == 'POST':
#         post_data = {
#             "status": "enable",
#             "version": "ipv4",
#             "client_ip": data.get('client_ip'),
#             "client_mask": data.get('client_mask'),
#             "server_ip": data.get('server_ip'),
#             "server_mask": data.get('server_mask'),
#             "desc": "desc"
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_ip_list", method='POST', data=post_data)) 
#     elif request.method == 'PUT':
#         data = request.json
#         put_data = {
#             "id":3,
#             "status": "enable",
#             "version": "ipv4",
#             "client_ip": data.get('client_ip'),
#             "client_mask": data.get('client_mask'),
#             "server_ip": data.get('server_ip'),
#             "server_mask": data.get('server_mask'),
#             "desc": "desc"
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_ip_list", method='PUT', data=put_data)) 
#     elif request.method == 'DELETE':
#         data = request.json
#         delete_data = {
#             "id": data.get('id')
#         }
#         return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_ip_list", method='DELETE', data=delete_data)) 

# @customer.route('/security-settings/blocked-ips',methods=['GET','POST','PUT','DELETE'])
# def blocked_ips():
#     url = api_base_url + f"system/block_ip_filter/ip_list"
#     if request.method == 'GET':
#         return jsonify(send_api_request(url, method='GET')) 
#     elif request.method == 'POST':
#         data = request.json
#         post_data = {
#             "client_ip": data.get('client_ip'),
#             "client_mask": data.get('client_mask'),
#             "desc":"none"
#         }
#         return jsonify(send_api_request(url, method='POST',data=post_data)) 
#     elif request.method == 'PUT':
#         data = request.json
#         put_data = {
#             "id": data.get('id'),
#             "client_ip": data.get('client_ip'),
#             "client_mask": data.get('client_mask'),
#             "time": 15,
#             "timeunit": "second",
#             "permanent_status": "disable",
#             "desc": "none"
#         }
#         return jsonify(send_api_request(url, method='PUT',data=put_data)) 
#     elif request.method == 'DELETE':
#         data = request.json
#         delete_data = {
#             "id": data.get('id'),
#         }
#         return jsonify(send_api_request(url, method='DELETE',data=delete_data))
    

# @customer.route('/security-settings/policy-details/<policy_name>', methods=['GET','POST','PUT','DELETE'])
# def get_policy_details(policy_name):
#     if request.method == 'GET':
#         return jsonify(utils.get_policy_data(policy_name, method='GET'))
#     elif request.method == 'PUT':
#         data = request.json
#         return jsonify(utils.get_policy_data(policy_name,method='PUT',data=data))
    

# @customer.route('/security-settings/policy-details/<policy_name>/information', methods=['GET'])
# def get_policy_infomation_signature(policy_name):
#     return jsonify(utils.get_policy_information())





