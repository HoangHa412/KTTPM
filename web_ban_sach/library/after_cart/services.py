# from datetime import datetime
# from library.extension import db
# from library.library_ma import BookSchema, AuthorSchema
# from library.model import Author, Books, Category, Hoa_Don, User, Cart,After_Cart
# from flask import request, jsonify
# from sqlalchemy.sql import func
# import json

# def add_after_cart_service():
#     user_id = request.json.get('user_id')

#     if user_id:
#         # Lấy thông tin người dùng từ bảng User
#         user = User.query.get(user_id)
#         if not user:
#             return jsonify({"message": "Người dùng không tồn tại!"}), 404
        
#         # Lấy tất cả sản phẩm trong giỏ hàng của người dùng này
#         cart_items = Cart.query.filter_by(user_id=user_id).all()
#         book_info_list =[]
#         total_price =0
#         if not cart_items:
#             return jsonify({"message": "Giỏ hàng trống!"}), 400

#         # Tạo các bản ghi trong bảng After_Cart từ giỏ hàng
#         for item in cart_items:
#             # Lấy thông tin sách từ bảng Books
#             book = Books.query.get(item.book_id)
#             if book:
#                 total_price += item.quantity*item.price
#                 # Tạo thông tin cho trường information
#                 book_info = {
#                     "book_id": book.id,
#                     "book_name": book.name,
#                     "quantity": item.quantity
#                 }
#                 book_info_list.append(book_info)

#                 # Tạo thông tin cho trường information
#                 information = json.dumps(book_info_list)  # Chuyển đổi danh sách thông tin thành chuỗi JSON
#         after_cart_entry = After_Cart(
#             user_id=user_id,
#             book_id=item.book_id,
#             quantity=item.quantity,
#             price=total_price,
#             information=json.dumps(information)  # Chuyển đổi thông tin thành chuỗi JSON
#         )
#         db.session.add(after_cart_entry)

#         try:
#             db.session.commit()
#             return jsonify({"message": "Các sản phẩm đã được thêm vào After_Cart thành công!"}), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"message": "Không thể thêm sản phẩm vào After_Cart!", "error": str(e)}), 400
#     else:
#         return jsonify({"message": "Lỗi yêu cầu, cần user_id."}), 400
    
# def get_all_after_cart_service(user_id):
#     after_cart_items = After_Cart.query.filter_by(user_id=user_id).all()
#     if after_cart_items:
#         after_cart_list = [{
#             "id": item.id,
#             "user_id": item.user_id,
#             "book_id": item.book_id,
#             "quantity": item.quantity,
#             "price": item.price,
#             "information": item.information
#         } for item in after_cart_items]
#         return jsonify(after_cart_list), 200
#     else:
#         return jsonify({"message": "Không tìm thấy sản phẩm nào trong After_Cart!"}), 404