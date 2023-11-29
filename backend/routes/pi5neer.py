from flask import Blueprint, request, jsonify, redirect, url_for
from response.headers import create_response
from flask_jwt_extended import jwt_required
from utils import bcrypt
from models.log import Log
from models.user import User
from models.domain import Domain
from models.user_application import UserApplication
from datetime import datetime, timedelta
from collections import Counter
from sqlalchemy import func
from models import *
from itertools import groupby

from utils import basic_auth,make_api_request
Pi5neer = Blueprint('pi5neer', __name__, url_prefix='/Pi5neer')
base_url = 'https://wf.awstest.piolink.net:8443/api/v3'




@Pi5neer.route('/dashboard/basic', methods=['GET'])
def dashboardAdmin():
    existing_logs = Log.query.all()
    if existing_logs:
        grouped_logs = {key: list(group) for key, group in groupby(existing_logs, key=lambda log: log.app_id)}
        response_data = {}
        for app_id, logs in grouped_logs.items():
            app_response = fetch_dashboard_data_admin(logs, app_id)
            response_data[app_id] = app_response
        return jsonify(response_data), 200
    return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500


@Pi5neer.route('/dashboard/traffic', methods=['GET'])
# @jwt_required
def dashboardAdmin2():
    existing_logs = Log.query.all()
    if existing_logs:
        grouped_logs = {key: list(group) for key, group in groupby(existing_logs, key=lambda log: log.app_id)}
        response_data = {}
        total_traffic = {"traffic": []}

        for app_id, logs in grouped_logs.items():
            app_response = fetch_dashboard_data2(logs, app_id)
            response_data[str(app_id)] = app_response
            total_traffic["traffic"] += app_response["traffic"]

        for app_id, app_response in response_data.items():
            app_response["traffic"] = sorted(app_response["traffic"], key=lambda x: x["interval"])

        total_count_per_interval = {}
        for entry in total_traffic["traffic"]:
            interval = entry["interval"]
            count = entry["count"]
            if interval in total_count_per_interval:
                total_count_per_interval[interval] += count
            else:
                total_count_per_interval[interval] = count

        total_traffic_response = {"total": {"traffic": []}}
        for interval, count in sorted(total_count_per_interval.items(), key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m')):
            total_traffic_response["total"]["traffic"].append({"count": count, "interval": interval})

        combined_response = response_data.copy()
        combined_response.update(total_traffic_response)
        return create_response(data=combined_response)

    return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500


@Pi5neer.route('/dashboard/resource', methods=['GET'])
@jwt_required
def getUsage() :
    url = base_url + '/system/monitoring/resource_info'
    response = make_api_request(url, method='GET', headers=basic_auth())
    return create_response(data=response.json()) 

@Pi5neer.route('/user-management_user', methods=['GET'])
# @jwt_required
def user_mgmt_user():
    existing_users = User.query.all()
    if existing_users:
        user_list = [
            {
                'id': user.id,
                'companyName': user.companyName,
            } for user in existing_users
        ]
        return jsonify({'users': user_list}), 200
    return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500

@Pi5neer.route('<int:user_id>/user-management_application', methods=['GET'])
# @jwt_required
def user_mgmt_app(user_id):
    existing_user_apps = UserApplication.get_apps_by_user_id(user_id)
    user_app_list = {}
    if existing_user_apps:

        for user_app in existing_user_apps:            
            domain_list = Domain.get_domains_by_app_id(user_app.id)
            
        return jsonify({'domain_list': domain_list}), 200
    return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500

@Pi5neer.route('/user-management', methods=['GET'])
# @jwt_required
def user_mgmt():
    existing_logs = Log.query.all()
    if existing_logs:
        grouped_logs = {key: [log.serialize() for log in group] for key, group in groupby(existing_logs, key=lambda log: log.app_id)}
        response_data = {}
        for app_id, logs in grouped_logs.items():
            app_response = fetch_dashboard_data_admin(logs, app_id)
            response_data[app_id] = app_response
        return jsonify(response_data), 200
    return jsonify({"error": "데이터를 가져오지 못했습니다."}), 500


def fetch_dashboard_data_admin(logs, app_id):
    current_time = datetime.datetime.now()
    start_time_1hour_interval = current_time - timedelta(days=7)
    
    log_1hour = get_logs_by_time_range(start_time_1hour_interval, current_time, app_id)
    
    data_timeline_response = count_occurrences_in_intervals_admin(log_1hour, start_time_1hour_interval, 15, app_id)
    data_pie_response = count_category_occurrences_admin(log_1hour, app_id)
    response_data = {"detect_attack": data_timeline_response, "attack_name": data_pie_response}
    return response_data

def fetch_dashboard_data2(logs, app_id):
    current_time = datetime.datetime.now()
    start_time_1years_interval = current_time - timedelta(days=365)
    log_1year = get_logs_by_year_range_admin(start_time_1years_interval, current_time, app_id)
    response_data = {"traffic": log_1year}
    return response_data

def count_category_occurrences_admin(logs, app_id):
    categories = [log.category for log in logs]

    category_counts = Counter(categories)

    return category_counts

def get_logs_by_time_range(start_time, end_time, app_id):
    logs = db.session.query(Log).filter(
        Log.app_id == app_id,
        Log.timestamp >= start_time,
        Log.timestamp < end_time
    ).all()
    return logs

def get_logs_by_year_range_admin(start_time, end_time, app_id):
    result = db.session.query(
        func.DATE_FORMAT(Log.timestamp, '%Y-%m').label('month'),
        func.count().label('count')
    ).filter(
        Log.app_id == app_id,
        Log.timestamp >= start_time
    ).group_by(func.DATE_FORMAT(Log.timestamp, '%Y-%m')).all()

    month_counts = [{"interval": month, "count": count} for month, count in result]
    
    def extract_date(interval):
        return datetime.datetime.strptime(interval, '%Y-%m')

    month_counts_sorted = sorted(month_counts, key=lambda x: extract_date(x["interval"]))
    return month_counts_sorted

def count_occurrences_in_intervals_admin(logs, end_time, interval_minutes, app_id):
    current_time = end_time
    start_time = current_time + timedelta(days=7)  # Adjust the starting point
    interval_counts = []

    while current_time < start_time:
        interval_start = current_time
        interval_end = current_time + timedelta(days=1)
        count = sum(1 for log in logs if interval_start <= log.timestamp < interval_end)
        interval_counts.append({"interval": f"{interval_start} - {interval_end}", "count": count})
        current_time = interval_end


    return interval_counts


