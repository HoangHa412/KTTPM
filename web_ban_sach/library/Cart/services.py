from library.extension import db
from library.library_ma import BookSchema, CartSchema
from library.model import User, Books, Author, Img, Cart
from flask import request, jsonify
from sqlalchemy.sql import func
import json

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

# Thêm mục vào giỏ hàng
def add_cart_service():
    data = request.json
    if data and ('user_id' in data) and ('book_id' in data) and ('quantity' in data):
        user_id = data['user_id']
        book_id = data['book_id']
        quantity = data['quantity']

        try:
            # Kiểm tra xem mục đã tồn tại trong giỏ hàng của user chưa
            existing_item = Cart.query.filter_by(user_id=user_id, book_id=book_id).first()
            
            # Lấy thông tin sách từ bảng Books
            book = Books.query.get(book_id)
            if not book:
                return jsonify({"message": "Book not found!"}), 404

            # Tính giá dựa vào số trang
            price = book.page_count * 1000
            
            if existing_item:
                # Nếu đã tồn tại, tăng quantity
                existing_item.quantity += quantity
                db.session.commit()
                return jsonify({"message": f"Updated quantity for book ID '{book_id}' to {existing_item.quantity}!"}), 200
            else:
                # Nếu chưa có, tạo mục mới trong giỏ hàng
                new_cart_item = Cart(
                    user_id=user_id,
                    book_id=book_id,
                    quantity=quantity,
                    price=price  # Thêm giá vào đối tượng Cart
                )
                db.session.add(new_cart_item)
                db.session.commit()
                return jsonify({"message": "Item added to cart!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot add to cart!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Request error"}), 400
# Lấy danh sách tất cả các cuốn sách trong giỏ hàng theo user_id
def get_user_books_in_cart_service(user_id):
    # Lấy tất cả các mục trong giỏ hàng của người dùng theo user_id
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    books_in_cart = []

    if cart_items:
        for cart_item in cart_items:
            # Lấy thông tin sách từ bảng Books dựa trên book_id
            book = Books.query.get(cart_item.book_id)
            if book:
                # Thêm thông tin sách và số lượng trong giỏ hàng vào danh sách
                book_details = {
                    "book_id": book.id,
                    "name": book.name,
                    "page_count": book.page_count,
                    "author_id": book.author_id,
                    "category_id": book.category_id,
                    "quantity": cart_item.quantity,
                    "price": cart_item.price
                }
                books_in_cart.append(book_details)
        
        return jsonify(books_in_cart), 200
    else:
        return jsonify({"message": "No books found in cart for this user!"}), 404

# Lấy tất cả các mục trong giỏ hàng
def get_all_cart_service():
    carts = Cart.query.all()  # Lấy tất cả các mục trong giỏ hàng
    cart_items = []

    if carts:
        for cart in carts:
            book = Books.query.get(cart.book_id)  # Lấy thông tin sách từ bảng Books
            img = Img.query.filter_by(book_id=cart.book_id).first()  # Lấy thông tin hình ảnh từ bảng Img
            
            if book:
                item_details = {
                    "id": cart.id,
                    "user_id": cart.user_id,
                    "book_id": cart.book_id,
                    "name": book.name,
                    "page_count": book.page_count,
                    "author_id": book.author_id,
                    "category_id": book.category_id,
                    "price": cart.price,
                    "quantity": cart.quantity,
                    "image_data": img.image_data if img else None  # Thêm thông tin hình ảnh
                }
                cart_items.append(item_details)
        
        return jsonify(cart_items), 200
    else:
        return jsonify({"message": "Not found cart items!"}), 404
# Lấy giỏ hàng của một người dùng cụ thể
def get_user_cart_service(user_id):
    carts = Cart.query.filter_by(user_id=user_id).all()  # Lấy giỏ hàng của người dùng
    cart_items = []

    if carts:
        for cart in carts:
            book = Books.query.get(cart.book_id)  # Lấy thông tin sách từ bảng Books
            if book:
                item_details = {
                    "user_id": cart.user_id,
                    "book_id": cart.book_id,
                    "name": book.name,
                    "page_count": book.page_count,
                    "author_id": book.author_id,
                    "category_id": book.category_id,
                    "price": cart.price,
                    "quantity": cart.quantity
                }
                cart_items.append(item_details)
        
        return jsonify(cart_items), 200
    else:
        return jsonify({"message": "No items found in cart for this user!"}), 404
# update số lượng
def update_cart_item_service(cart_item_id):
    data = request.json
    cart_item = Cart.query.get(cart_item_id)

    if cart_item:
        if 'quantity' in data:
            new_quantity = data['quantity']
            cart_item.quantity = new_quantity

            # Cập nhật giá dựa trên số lượng mới
            book = Books.query.get(cart_item.book_id)
            if book:
                cart_item.price = book.page_count * 1000 * new_quantity  # Tính giá mới

            try:
                db.session.commit()
                return jsonify({"message": "Quantity updated successfully!", "new_quantity": cart_item.quantity}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": "Cannot update quantity!", "error": str(e)}), 400
        else:
            return jsonify({"message": "Request error, 'quantity' is required"}), 400
    else:
        return jsonify({"message": "Item not found in cart!"}), 404

# Xóa một mục khỏi giỏ hàng theo ID
def remove_cart_item_service(cart_item_id):
    cart_item = Cart.query.get(cart_item_id)  # Tìm mục giỏ hàng theo ID
    if cart_item:
        try:
            db.session.delete(cart_item)  # Xóa mục giỏ hàng
            db.session.commit()
            return jsonify({"message": "Item removed from cart!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot remove item from cart!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Item not found in cart!"}), 404
# Xóa tất cả các mục trong giỏ hàng theo user_id
def remove_all_cart_items_service(user_id):
    try:
        # Lấy tất cả các mục trong giỏ hàng của người dùng
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        
        if cart_items:
            # Xóa tất cả các mục trong giỏ hàng
            for item in cart_items:
                db.session.delete(item)
            db.session.commit()
            return jsonify({"message": f"All items removed from cart for user ID '{user_id}'!"}), 200
        else:
            return jsonify({"message": f"No items found in cart for user ID '{user_id}'!"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Cannot remove items from cart!", "error": str(e)}), 400

# Xóa một mục khỏi giỏ hàng
# def remove_cart_item_service():
#     data = request.json
#     if data and ('user_id' in data) and ('book_id' in data):
#         user_id = data['user_id']
#         book_id = data['book_id']

#         try:
#             cart_item = Cart.query.filter_by(user_id=user_id, book_id=book_id).first()
#             if not cart_item:
#                 return jsonify({"message": "Item not found in cart!"}), 404
            
#             db.session.delete(cart_item)
#             db.session.commit()
#             return jsonify({"message": "Item removed from cart!"}), 200
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"message": "Cannot remove item from cart!", "error": str(e)}), 400
#     else:
#         return jsonify({"message": "Request error"}), 400
