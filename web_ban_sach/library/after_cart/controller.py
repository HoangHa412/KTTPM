# from flask import Blueprint
# from .services import (add_after_cart_service, get_all_after_cart_service)

# After_Cart_bp = Blueprint("AfterCart", __name__)

# @After_Cart_bp.route("/add_after_cart", methods=['POST'])
# def add_after_cart():
#     return add_after_cart_service()

# @After_Cart_bp.route("/get_all_after_cart/<int:id>", methods=['GET'])
# def get_all_after_cart(id):
#     return get_all_after_cart_service(id)