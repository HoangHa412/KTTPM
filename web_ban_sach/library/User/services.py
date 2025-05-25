from library.extension import db
from library.library_ma import Hoa_DonSchema
from library.model import User, Books, Cart, Hoa_Don
from flask import request, jsonify

def add_user_service():
    data = request.json
    print("Received data:", data)  # Kiểm tra dữ liệu đầu vào
    if data and ('name' in data) and ('address' in data) and ('phone_numbers' in data):
        name = data['name']
        address = data['address']
        phone_numbers = data['phone_numbers']

        new_user = User(name=name, address=address, phone_numbers=phone_numbers)

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User added successfully!"}), 201
        except Exception as e:
            db.session.rollback()
            print("Error occurred:", str(e))  # Ghi lại lỗi
            return jsonify({"message": "Cannot add user!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Request error"}), 400

def get_all_users_service():
    users = User.query.all()
    if users:
        user_list = [{"id": user.id, "name": user.name, "address": user.address, "phone_numbers": user.phone_numbers} for user in users]
        count_user = len(user_list)
        return jsonify({'tongSoLuonguser': count_user}), 200
    else:
        return jsonify({"message": "No users found!"}), 404

def get_user_by_id_service(user_id):
    user = User.query.get(user_id)
    if user:
        user_details = {
            "id": user.id,
            "name": user.name,
            "address": user.address,
            "phone_numbers": user.phone_numbers
        }
        return jsonify(user_details), 200
    else:
        return jsonify({"message": "User not found!"}), 404

def update_user_service(user_id):
    data = request.json
    user = User.query.get(user_id)

    if user:
        if 'name' in data:
            user.name = data['name']
        if 'address' in data:
            user.address = data['address']
        if 'phone_numbers' in data:
            user.phone_numbers = data['phone_numbers']

        try:
            db.session.commit()
            return jsonify({"message": "User updated successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot update user!", "error": str(e)}), 400
    else:
        return jsonify({"message": "User not found!"}), 404

def delete_user_service(user_id):
    user = User.query.get(user_id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot delete user!", "error": str(e)}), 400
    else:
        return jsonify({"message": "User not found!"}), 404
