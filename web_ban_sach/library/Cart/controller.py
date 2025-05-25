from flask import Blueprint
from .services import (
    add_cart_service,
    get_all_cart_service,
    get_user_cart_service,
    remove_cart_item_service,
    update_cart_item_service,
    get_user_books_in_cart_service,
    remove_all_cart_items_service
)

cart = Blueprint("Cart", __name__)

# Route để thêm mục vào giỏ hàng
@cart.route("/add_cart", methods=['POST'])
def add_cart():
    return add_cart_service()
# Route để lấy tất cả các mục trong giỏ hàng theo user_id
@cart.route("/cart_userid/<int:user_id>", methods=['GET'])
def get_all_cart_id(user_id):
    return get_user_books_in_cart_service(user_id)

# Route để lấy tất cả các mục trong giỏ hàng
@cart.route("/cart_all", methods=['GET'])
def get_all_cart():
    return get_all_cart_service()

# Route để lấy giỏ hàng của một người dùng cụ thể
@cart.route("/cart/<int:user_id>", methods=['GET'])
def get_user_cart(user_id):
    return get_user_cart_service(user_id)

# Route để update giỏ hàng theo ID
@cart.route('/update_cart_item/<int:cart_item_id>', methods=['PUT'])
def update_cart_item(cart_item_id):
    return update_cart_item_service(cart_item_id)

# Route để xóa một mục khỏi giỏ hàng theo ID
@cart.route("/remove_cart/<int:cart_item_id>", methods=['DELETE'])
def remove_cart_item(cart_item_id):
    return remove_cart_item_service(cart_item_id)
#REMOVE theo user_id
@cart.route("/remove_all_cart/<int:user_id>", methods=['DELETE'])
def remove_cart_item_by_user_id(user_id):
    return remove_all_cart_items_service(user_id)

