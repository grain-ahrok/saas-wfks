from flask import Blueprint, session, jsonify, request
import requests
import utils
import json
import urllib3

customer = Blueprint('customer', __name__, url_prefix='/customer')

# 공통 URL
api_base_url = "https://wf.awstest.piolink.net:8443/api/v3/"
dashboard_data_url = 'https://wf.awstest.piolink.net:8443/kui/api/cgi-bin/dashboard/'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #지우시요 나중에

def send_api_request(url, method='GET', data=None):
    headers = {"Authorization": session['token']}
    if method == 'GET':
        response = requests.get(url, headers=headers, verify=False)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=data, verify=False)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data, verify=False)
    return response.json()

@customer.route('/dashboard', methods=['POST'])
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

@customer.route('/security-logs')
def security_logs():
    url = "https://wf.awstest.piolink.net:8443/cgi-bin/logviewer/"
    param_data = {
        "action": "select",
        "filter": {
            "detail": {},
            "basic": {},
            "period": "86400",
        },
        "limit": 100,
        "pageParam": None
    }

    data = {
        "log_type": "security",
        "param": json.dumps(param_data)
    }
    
    response = send_api_request(url, 'POST', data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500

@customer.route('/security-settings/exception-urls',method=['GET','POST','PUT','DELETE'])
def exception_urls():
    if request.method == 'GET':
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow", method='GET'))    
    elif request.method == 'POST':
        data = request.json
        post_data : {
            "status": "enable",
            "url": "/*",
            "desc": "default"
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow", method='POST', data=post_data))    
    elif request.method == 'PUT':
        data = request.json
        put_data : {
            "id": 1,
            "status": "enable",
            "url": "/*",
            "desc": "default"
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow", method='PUT', data=put_data))    
    elif request.method == 'DELETE':
        data = request.json
        delete_data : {
            "id" : 1
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow", method='DELETE',data=delete_data))    

@customer.route('/security-settings/apply-urls',method=['GET','POST','PUT','DELETE'])
def apply_urls():
    if request.method == 'GET':
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_url_list", method='GET'))    
    elif request.method == 'POST':
        data = request.json
        post_data = {
            "status": "enable",
            "url": "/*/test",
            "desc": "desc"
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_url_list", method='POST', data=post_data))    
    elif request.method == 'PUT':
        data = request.json
        put_data = {
            "id": 2,
            "status": "enable",
            "url": "/*/test2",
            "desc": "default"
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_url_list", method='PUT', data=put_data))    
    elif request.method == 'DELETE':
        data = request.json
        delete_data = {
            "id": 2
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_url_list", method='DELETE', data=delete_data))    
 
@customer.route('/security-settings/exception-ips',method=['GET','POST','PUT','DELETE'])
def exception_ips():
    if request.method == 'GET':
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/exception_ip_list", method='GET'))    
    elif request.method == 'POST':
        data = request.json
        post_data = {
            "status": "enable",
            "version": "ipv4",
            "client_ip": "192.168.231.168",
            "client_mask": 0,
            "server_ip": "192.168.216.109",
            "server_mask": 0,
            "desc": "desc"
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/exception_ip_list", method='POST', data=post_data))    
    elif request.method == 'PUT':
        data = request.json
        put_data = {
            "id":1,
            "status": "enable",
            "version": "ipv4",
            "client_ip": "192.168.231.167",
            "client_mask": 0,
            "server_ip": "192.168.216.109",
            "server_mask": 0,
            "desc": "desc"
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/exception_ip_list", method='PUT', data=put_data))    
    elif request.method == 'DELETE':
        data = request.json
        delete_data = {
            "id": 1
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/exception_ip_list", method='DELETE', data=delete_data))    

@customer.route('/security-settings/apply-ips',method=['GET','POST','PUT','DELETE'])
def apply_ips():
    if request.method == 'GET':
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_ip_list", method='GET'))    
    elif request.method == 'POST':
        post_data = {
            "status": "enable",
            "version": "ipv4",
            "client_ip": "192.168.231.168",
            "client_mask": 0,
            "server_ip": "192.168.216.109",
            "server_mask": 0,
            "desc": "desc"
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_ip_list", method='POST', data=post_data)) 
    elif request.method == 'PUT':
        data = request.json
        put_data = {
            "id":3,
            "status": "enable",
            "version": "ipv4",
            "client_ip": "192.168.231.168",
            "client_mask": 0,
            "server_ip": "192.168.216.109",
            "server_mask": 0,
            "desc": "desc"
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_ip_list", method='PUT', data=put_data)) 
    elif request.method == 'DELETE':
        data = request.json
        delete_data = {
            "id": 1
        }
        return jsonify(send_api_request(api_base_url + f"security_policy/{session['id']}/buffer_overflow/apply_ip_list", method='DELETE', data=delete_data)) 

@customer.route('/security-settings/blocked-ips',method=['GET','POST','PUT','DELETE'])
def blocked_ips():
    url = api_base_url + f"system/block_ip_filter/ip_list"
    if request.method == 'GET':
        return jsonify(send_api_request(url, method='GET')) 
    elif request.method == 'POST':
        data = request.json
        post_data = {
            "client_ip": data.get('client_ip'),
            "client_mask": data.get('client_mask'),
            "desc":"none"
        }
        return jsonify(send_api_request(url, method='POST',data=post_data)) 
    elif request.method == 'PUT':
        data = request.json
        put_data = {
            "id": data.get('id'),
            "client_ip": data.get('client_ip'),
            "client_mask": data.get('client_mask'),
            "time": 15,
            "timeunit": "second",
            "permanent_status": "disable",
            "desc": "none"
        }
        return jsonify(send_api_request(url, method='PUT',data=put_data)) 
    elif request.method == 'DELETE':
        data = request.json
        delete_data = {
            "id": data.get('id'),
        }
        return jsonify(send_api_request(url, method='DELETE',data=delete_data))
    
@customer.route('/security-settings/policy-details/<policy_name>', methods=['GET','POST','PUT','DELETE'])
def get_policy_details(policy_name):
    if request.method == 'GET':
        return jsonify(utils.get_policy_data(policy_name, method='GET'))
    elif request.method == 'PUT':
        data = request.json
        return jsonify(utils.get_policy_data(policy_name,method='PUT',data=data))
    

@customer.route('/security-settings/policy-details/<policy_name>/information', methods=['GET'])
def get_policy_infomation_signature(policy_name):
    return jsonify(utils.get_policy_information())

@customer.route('/domain-settings', methods=['GET', 'PUT', 'POST'])
def manage_domain_settings():
    if request.method == 'GET':
        url = api_base_url + f"{session['id']}/general/domain_list"
        return jsonify(send_api_request(url, method='GET'))
    elif request.method == 'PUT':
        data = request.json
        id = data.get("id")
        status = data.get("status")
        domain = data.get("domain")
        desc = data.get("desc")
        data = {
            "status": status,
            "domain": domain,
            "desc": desc
        }
        url = api_base_url + f"{session['id']}/general/domain_list"
        return jsonify(send_api_request(url, method='PUT', data=data))
    elif request.method == 'POST':
        data = request.json
        id = data.get("id")
        main_ip = data.get("main_ip")
        setting_ip = data.get("setting_ip")
        port_number = data.get("port_number")
        domain = data.get("domain")
        setting_domain = data.get("setting_domain")
        desc = data.get("desc")
        data = {
            "status": "enable",
            "domain": domain,
            "desc": desc
        }
        url = api_base_url + f"{session['id']}/general/domain_list"
        return jsonify(send_api_request(url, method='PUT', data=data))  

def fetch_dashboard_data(data_type):
    url = 'https://wf.awstest.piolink.net:8443/kui/api/cgi-bin/dashboard/'
    with open('dashboard_data.json', 'r') as json_file:
        dashboard_data = json.load(json_file)
    data = dashboard_data.get(data_type)
    return utils.fetch_dashboard_data(url, data)
