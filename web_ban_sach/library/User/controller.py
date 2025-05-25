from flask import Blueprint
from .services import (add_user_service, get_all_users_service, get_user_by_id_service, update_user_service, delete_user_service)

user_bp = Blueprint("User", __name__)

@user_bp.route("/add_user", methods=['POST'])
def add_user():
    return add_user_service()

@user_bp.route("/users", methods=['GET'])
def get_all_users():
    return get_all_users_service()

@user_bp.route("/user/<int:user_id>", methods=['GET'])
def get_user_by_id(user_id):
    return get_user_by_id_service(user_id)

@user_bp.route("/user/<int:user_id>", methods=['PUT'])
def update_user(user_id):
    return update_user_service(user_id)

@user_bp.route("/user/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    return delete_user_service(user_id)
