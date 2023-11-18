from flask import Blueprint, session, jsonify, request
import requests
from utils import make_api_request
import json
import urllib3
from models.domain import Domain,datetime
from models.log import Log
import base64
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

@customer.route('/app/<int:app_id>/logs', methods=['GET'])
def security_logs(app_id):
    # Check if logs are already present in the database
    existing_logs = Log.query.all()

    # Filtering parameters
    timestamp_filter = request.args.get('timestamp')
    category_filter = request.args.get('category')
    url_filter = request.args.get('url')
    host_filter = request.args.get('host')
    action_filter = request.args.get('action')

    if existing_logs:

        log_s = [
                    {
                        'no': log.no,
                        'timestamp': log.timestamp,
                        'category': log.category,
                        'app_name': log.app_name,
                        'risk_level': log.risk_level,
                        'sig_level': log.sig_level,
                        'host': log.host,
                        'url': log.url,
                        'attacker_ip': log.attacker_ip,
                        'server_ip_port': log.server_ip_port,
                        'country': log.country,
                        'action': log.action,
                        'app_id': log.app_id
                    }
                    for log in existing_logs
                ]
        
        
        # Apply filters to existing logs
        filtered_logs = [log for log in log_s if
                        (not timestamp_filter or timestamp_filter == log.get('timestamp')) and
                        (not category_filter or category_filter == log.get('category')) and
                        (not url_filter or url_filter == log.get('url')) and
                        (not host_filter or host_filter == log.get('host')) and
                        (not action_filter or action_filter == log.get('action'))
                        ]
        
        # 페이지네이션 적용
        limit = int(request.args.get('limit', 10))
        page = int(request.args.get('page', 1))

        # 전체 페이지 수 계산
        total_pages = (len(filtered_logs) + limit - 1) // limit

        # 페이지 범위 계산
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit

        # 현재 페이지에 해당하는 로그만 추출
        paginated_logs = filtered_logs[start_idx:end_idx]

        
            
        # Return filtered logs from the database with pagination and unique hosts
        return jsonify({
            "database_logs": filtered_logs,
            "hosts": list(set(log.host for log in existing_logs)),
            "total_pages": total_pages
        }), 200
    else:
        # Fetch logs from the external API
        url = 'https://wf.awstest.piolink.net:8443/cgi-bin/logviewer/'
        headers = {'Cookie': 'PB_LANG=ko; UI=wafwaf'}
        data = {'log_type': 'security',
                'param': 'eyJhY3Rpb24iOiJzZWxlY3QiLCJmaWx0ZXIiOnsiZGV0YWlsIjp7fSwiYmFzaWMiOnt9LCJwZXJpb2QiOiIyNTkyMDAwIn0sImxpbWl0IjoxMDAsInBhZ2VQYXJhbSI6bnVsbH0='}

        response = requests.post(url, data=data, verify=False, headers=headers)

        if response.status_code == 200:
            data = response.json()
            app_name = request.args.get('app_name', 'pweb')  # 일단 테스트용

            # 'logs' 키 확인 추가
            logs_data = data.get('result', {}).get('logs', [])

            # 'rows' 안에 있는 데이터에서 "Application"이 주어진 `app_name`과 일치하는 로그를 추출
            app_logs = [log for log_data in logs_data for log in log_data.get("rows", []) if log[3] == app_name]

            # Save logs to the database
            for log_data in app_logs:
                decoded_url = base64.b64decode(log_data[6]).decode('utf-8')
                timestamp = datetime.fromtimestamp(log_data[1])
                host = base64.b64decode(log_data[7])
                formatted_log = {
                    'no': log_data[0],
                    'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # 수정된 부분
                    'category': log_data[2]['text'],  # 수정된 부분
                    'app_name': log_data[3],
                    'risk_level': log_data[4]['text'],  # 수정된 부분
                    'sig_level': log_data[5]['text'],  # 수정된 부분
                    'host': host,
                    'url': decoded_url,
                    'attacker_ip': log_data[8],
                    'server_ip_port': log_data[9],
                    'country': log_data[10]['text'],  # 수정된 부분
                    'action': log_data[11]['text'],  # 수정된 부분
                    'app_id' : app_id
                }
                Log.add_log(formatted_log)
            
            existing_logs = Log.query.all()

            log_s = [
                    {
                        'no': log.no,
                        'timestamp': log.timestamp,
                        'category': log.category,
                        'app_name': log.app_name,
                        'risk_level': log.risk_level,
                        'sig_level': log.sig_level,
                        'host': log.host,
                        'url': log.url,
                        'attacker_ip': log.attacker_ip,
                        'server_ip_port': log.server_ip_port,
                        'country': log.country,
                        'action': log.action,
                        'app_id': log.app_id
                    }
                    for log in existing_logs
                ]
        
        
            # Apply filters to existing logs
            filtered_logs = [log for log in log_s if
                            (not timestamp_filter or timestamp_filter == log.get('timestamp')) and
                            (not category_filter or category_filter == log.get('category')) and
                            (not url_filter or url_filter == log.get('url')) and
                            (not host_filter or host_filter == log.get('host')) and
                            (not action_filter or action_filter == log.get('action'))
            ]  
            
            # 페이지네이션 적용
            limit = int(request.args.get('limit', 10))
            page = int(request.args.get('page', 1))

            # 전체 페이지 수 계산
            total_pages = (len(filtered_logs) + limit - 1) // limit

            # 페이지 범위 계산
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit

           
            # 현재 페이지에 해당하는 로그만 추출
            paginated_logs = app_logs[start_idx:end_idx]
                       
            # 응답 헤더에 전체 페이지 수 추가
            headers['X-Total-Pages'] = str(total_pages)
            
            # Return both logs from the database and external API with pagination and unique hosts
            return jsonify({
                "database_logs": filtered_logs,
                "hosts": list(set(log.host for log in existing_logs)),
                "total_pages": total_pages
            }), 200
        else:
            return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500


    



@customer.route('/domain-settings', methods=['GET', 'PUT', 'POST','DELETE'])
def manage_domain_settings():
    url = f"https://wf.awstest.piolink.net:8443/kui/api/v3/{session['app_id']}/general/domain_list"
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





