from flask import Blueprint
from flask import request, jsonify
from .services import (get_user_account_and_password,update_admin_password,get_admin_account_and_password,add_admin_account,add_user_account)

quan_tri_bp = Blueprint("Quantri", __name__)
@quan_tri_bp.route('/get_user_credentials/<string:account_user>', methods=['GET'])
def user_credentials(account_user):
    result = get_user_account_and_password(account_user)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "User not found"}), 404


@quan_tri_bp.route('/get_admin_credentials/<string:account_admin>', methods=['GET'])
def admin_credentials(account_admin):
    result = get_admin_account_and_password(account_admin)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Admin not found"}), 404

@quan_tri_bp.route('/update_admin_password', methods=['PUT'])
def update_password():
    data = request.get_json()
    account_admin = data.get('account_admin')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    return update_admin_password(account_admin, current_password, new_password)

@quan_tri_bp.route('/add_admin_account', methods=['POST'])
def create_admin():
    data = request.json
    account_admin = data.get('account_admin')
    password_admin = data.get('password_admin')
    if not account_admin or not password_admin:
        return {"message": "Invalid input. Both account_admin and password_admin are required."}, 400
    return add_admin_account(account_admin, password_admin)


@quan_tri_bp.route('/add_user_account', methods=['POST'])
def create_user():
    data = request.json
    
    # Lấy thông tin từ body của request
    name = data.get('name')
    address = data.get('address')
    phone_numbers = data.get('phone_numbers')
    account_user = data.get('account_user')
    password_user = data.get('password_user')

    # Kiểm tra thông tin đầu vào
    if not name or not address or not phone_numbers or not account_user or not password_user:
        return {"message": "Invalid input. All fields are required."}, 400

    return add_user_account(name, address, phone_numbers, account_user, password_user)
