from flask import Blueprint, session, jsonify, request
import requests
from utils import make_api_request,generate_token
import json
import urllib3
from models.domain import Domain,datetime
from models.log import Log
from models.user_application import UserApplication
from models.security_policy import SecurityPolicy
import base64
from models import *
from datetime import datetime, timedelta
from collections import Counter
from sqlalchemy import func
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required
app = Blueprint('app', __name__, url_prefix='/app')
app.before_request(jwt_required())
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #지우시요 나중에

@app.route('/<int:app_id>/dashboard', methods=['GET'])
def dashboard(app_id):
    response_data = fetch_dashboard_data("data_timeline")

    if response_data:
        
        return jsonify(response_data), 200

    return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500

def fetch_dashboard_data(app_id):
    current_time = datetime(2023, 11, 18, 5, 25, 15)
    start_time_1hour_interval = current_time - timedelta(hours=1)
    log_1hour = get_logs_by_time_range(start_time_1hour_interval, current_time)
    data_timeline_response = count_occurrences_in_intervals(log_1hour, start_time_1hour_interval, 15)
    data_pie_response =  count_category_occurrences(log_1hour)
    start_time_1years_interval = current_time - timedelta(days=365)
    log_1year = get_logs_by_year_range(start_time_1years_interval, current_time)
    response_data = {"detect_attack": data_timeline_response,
                     "attack_name": data_pie_response,
                     "tarffic":log_1year}
    return response_data

def count_category_occurrences(logs):
    # Extract category values from logs
    categories = [log.category for log in logs]

    # Use Counter to count occurrences of each category
    category_counts = Counter(categories)

    return category_counts
def get_logs_by_time_range(start_time, end_time):
    # Retrieve all logs within the time range
    logs = db.session.query(Log).filter(
        Log.timestamp >= start_time,
        Log.timestamp < end_time
    ).all()
    return logs

def get_logs_by_year_range(start_time, end_time):
    result = db.session.query(
    func.DATE_FORMAT(Log.timestamp, '%Y-%m').label('month'),
    func.count().label('count')
    ).filter(
        Log.timestamp >= start_time
    ).group_by(func.DATE_FORMAT(Log.timestamp, '%Y-%m')).all()

    # Create a dictionary to store month-wise log counts
    month_counts = {month: count for month, count in result}

    # Output the dictionary
    print(month_counts)
    return month_counts

def count_occurrences_in_intervals(logs, end_time, interval_minutes):
    current_time = end_time
    start_time = current_time + timedelta(minutes=60)

    # Create a list to store counts for each interval
    interval_counts = []

    # Iterate over each minute interval

    while current_time !=start_time:
        interval_start = current_time
        interval_end = current_time + timedelta(minutes=interval_minutes)
        print(interval_start,interval_end)
        # Count occurrences within the current interval
        count = sum(1 for log in logs if interval_start <= datetime.strptime(log.timestamp, '%Y-%m-%d %H:%M:%S') < interval_end)
        interval_counts.append({"interval": f"{interval_start} - {interval_end}", "count": count})
        current_time = interval_end

    #print(interval_counts)
    return interval_counts


@app.route('/<int:app_id>/logs', methods=['GET'])
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
            "database_logs": paginated_logs,
            "hosts": list(set(log.host for log in existing_logs)),
            "total_pages": total_pages
        }), 200
    else:
        # Fetch logs from the external API
        url = 'https://wf.awstest.piolink.net:8443/cgi-bin/logviewer/'
        headers = {'Cookie': 'PB_LANG=ko; UI=wafwaf'}
        encoded_string = "eyJhY3Rpb24iOiJzZWxlY3QiLCJmaWx0ZXIiOnsiZGV0YWlsIjp7fSwiYmFzaWMiOnsiYXBwX2lkIjpbIjEiXX0sInBlcmlvZCI6IjI1OTIwMDAifSwibGltaXQiOjEwMCwicGFnZVBhcmFtIjpudWxsfQ="

        # Decode the Base64 string
        decoded_bytes = base64.urlsafe_b64decode(encoded_string + '=' * (-len(encoded_string) % 4))

        # Decode the bytes to UTF-8 string
        decoded_string = decoded_bytes.decode('utf-8')
        # JSON 문자열을 파이썬 객체로 변환
        decoded_data = json.loads(decoded_string)

        # app_id 업데이트
        decoded_data['filter']['basic']['app_id'] = [app_id]

        # 다시 JSON 문자열로 변환
        updated_encoded_string = json.dumps(decoded_data)
        
        # Encode the UTF-8 string to bytes
        encoded_bytes = decoded_string.encode('utf-8')

        # Encode the bytes to Base64
        encoded_string = base64.urlsafe_b64encode(encoded_bytes).decode()

   
        data = {
            'log_type': 'security',
            'param': encoded_string
        }


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
                host = base64.b64decode(log_data[7])
                formatted_log = {
                    'no': log_data[0],
                    'timestamp': log_data[1],  # 수정된 부분
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
                "database_logs": paginated_logs,
                "hosts": list(set(log.host for log in existing_logs)),
                "total_pages": total_pages
            }), 200
        else:
            return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500



@app.route('/<int:app_id>/domain-list', methods=['GET', 'PUT', 'POST','DELETE'])
def manage_domain_settings(app_id):
    url = f"https://wf.awstest.piolink.net:8443/api/v3/app/{app_id}/general/domain_list"
    url2 = f"https://wf.awstest.piolink.net:8443/api/v3/app/{app_id}/general/apply_ip_list"
    web_firewall_ip = "43.200.213.102"
    web_firewall_port = 8443  # 포트 정보
    token = generate_token()
    headers = {'Authorization': 'token ' + token}


    if request.method == 'GET':
        user_id = session['user_id']
        user_app = UserApplication.get_app_by_user_id(user_id=user_id)
        apps = [{
                "id" : item.id, 
                "ip" : item.ip_addr, 
                "port" : item.port, 
                "status" : item.status, 
                "server_name" : item.sever_name,
                "domain_list" : Domain.get_domains_by_app_id(item.id),
            } for item in user_app]
        return json.dumps(apps, indent=2)
    

    elif request.method == 'PUT':
        data = request.json
        
        if "apps" in data and data["apps"]:
            app_data = data["apps"][0]  # Assuming there's only one item in "apps" list

            # Extracting information from the nested dictionary
            app_info = {
                "id": app_data.get("id"),
                "ip": app_data.get("ip"),
                "port": app_data.get("port"),
                "status": app_data.get("status"),
                "domain": app_data.get("domain"),
                "server_name": app_data.get("server_name"),
            }

            # Extracting information from the nested list of dictionaries
            domain_list = []
            for domain_data in app_data.get("domain_list", []):
                domain_info = {
                    "name": domain_data.get("name"),
                    "id": domain_data.get("id"),
                    "desc": domain_data.get("desc", ""),  # Assuming "desc" might not always be present
                }
                domain_list.append(domain_info)
                response = make_api_request(domain_url, method='POST', data=domain_info)
            # Combining all extracted information
            result_data = {
                "app_info": app_info,
                "domain_list": domain_list
            }
        else:
            result_data = {}
            
        domain_id = data.get("domain")
        domain = Domain.get_domain_by_id(domain_id)
        if response.status_code == 200:
            if domain:
                domain.update(
                    name=data.get("domain"),
                )
                ip_lists = data.get('ip_list')
                app_data = UserApplication.get_app_by_id(app_id)
                
                for ip_list in ip_lists:
                    client_ip, mask_bits = ip_list.get('ip').split("/")
                    mask_bits = int(mask_bits)
                    ip_data = [
                        {
                            "id": request.args.get('id'),
                            "status": "enable",
                            "version": ip_list.get('version'),
                            "client_ip": client_ip,
                            "client_mask": mask_bits,
                            "ip": app_data.ip_addr,
                            "port": ip_list.get('port'),
                            "desc": ""
                        }
                    ]
                    response = make_api_request(url, method='POST', data=ip_data)
                    
                add_host_entry(web_firewall_ip,data.get("domain"),web_firewall_port)
                
            else:
                return jsonify({"error": f"Domain with id {domain_id} not found."}), 404
        return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500

 
    
    elif request.method == 'POST':
        data = request.json
        status = data.get("status")
        domain_list = data.get("domain_list")
        
        domains = [item.get("domain") for item in domain_list]
        app_table = UserApplication.get_app_by_wf_app_id(app_id)
        print(app_table.id)

        for domain in domains:
            data = {
                "status": status,
                "domain": domain,
                "desc": ""
            }
            response = make_api_request(domain_url, method='POST', headers=headers,data=data)
            
            if response.status_code == 200:
                new_domain = Domain.create(
                    name=domain,
                    user_application_id=app_table.id,
                    updated_at=datetime.utcnow()
                )

        # Server List
        server_list_url = f'https://wf.awstest.piolink.net:8443/api/v3/app/{app_id}/load_balance/server_list'
        server_list_data = [{"status": "enable", "version": data.get('version'), "server_name": data.get("servername"), "server_ip": data.get("ip"), "server_port": data.get('port'),  "desc": ""}]
        server_list_response = make_api_request(server_list_url,method="POST", headers=headers, data=server_list_data)
        if server_list_response.status_code == 200:
            return server_list_response.json()
        else:        
            return jsonify({"error": "server_list_response."}), 500

    elif request.method == 'DELETE':
        data = request.json
        id = data.get("id")
        data = [{"id": id}]
        response = make_api_request(url, method='DELETE', data=data)
        if response.status_code == 200:
            return response.json()  
        else:
            return jsonify({"error": "도메인 삭제에 실패하셨습니다.."}), 500



def add_host_entry(web_firewall_ip, domain, web_firewall_port=None):
    try:
        # hosts 파일 경로
        hosts_path = r'C:\\windows\\system32\\drivers\\etc\\hosts'

        # 추가할 엔트리
        if web_firewall_port:
            new_entry = f'\n{web_firewall_ip}:{web_firewall_port} {domain}'
        else:
            new_entry = f'\n{web_firewall_ip} {domain}'

        # hosts 파일 열기 (append 모드)
        with open(hosts_path, 'a') as hosts_file:
            hosts_file.write(new_entry)

        print(f'Successfully added entry: {web_firewall_ip}:{web_firewall_port} {domain} to hosts file.')
    except Exception as e:
        print(f'Error adding entry to hosts file: {str(e)}')


