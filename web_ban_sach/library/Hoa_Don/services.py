from datetime import datetime
from library.extension import db
from library.library_ma import BookSchema, AuthorSchema
from library.model import Author, Books, Category, Hoa_Don, User, Cart, Voucher
from flask import request, jsonify
from sqlalchemy.sql import func
import json

# Thêm hóa đơn mới
def add_hoa_don_service():
    user_id = request.json.get('user_id')
    address = request.json.get('address')
    makhuyenmai = request.json.get('makhuyenmai')  # Lấy mã khuyến mãi từ request
    payment_method = request.json.get('payment_method')

    if user_id and address:
        # Lấy thông tin người dùng từ bảng User
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Người dùng không tồn tại!"}), 404
        
        # Lấy tất cả sản phẩm trong giỏ hàng của người dùng này
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        book_info_list = []
        total_price = 0
        if not cart_items:
            return jsonify({"message": "Giỏ hàng trống!"}), 400

        # Tạo các bản ghi trong bảng After_Cart từ giỏ hàng
        for item in cart_items:
            # Lấy thông tin sách từ bảng Books
            book = Books.query.get(item.book_id)
            if book:
                total_price += item.quantity * item.price
                book_info = {
                    "book_id": book.id,
                    "book_name": book.name,
                    "quantity": item.quantity
                }
                book_info_list.append(book_info)

        # Tính toán giá trị giảm giá nếu có mã khuyến mãi
        discount = 0
        if makhuyenmai:
            voucher = Voucher.query.filter_by(makhuyenmai=makhuyenmai).first()
            if voucher:
                discount = (voucher.tylekm / 100) * total_price
            else:
                return jsonify({"message": "Mã khuyến mãi không hợp lệ!"}), 400

        sum_price = total_price - discount  # Tổng giá sau khi áp dụng giảm giá

        # Chuyển đổi thông tin sách và địa chỉ sang JSON
        information = json.dumps(book_info_list)
        address_json = json.dumps(address)

        # Tạo hóa đơn mới
        new_invoice = Hoa_Don(
            user_id=user_id,
            book_id=item.book_id,
            quantity=item.quantity,
            price=item.price,
            sum_price=sum_price,
            information=information,
            address=address_json,
            phone_number=user.phone_numbers,
            tt_hoadon="Chờ xác nhận",
            loai_thanhtoan=payment_method,
            # date = datetime(2024, 11, 10)
            date=datetime.utcnow()
        )

        db.session.add(new_invoice)
        try:
            db.session.commit()
            return jsonify({
                "message": "Hóa đơn đã được thêm thành công!", 
                "id_hoaDon": new_invoice.id, 
                "sum_price": sum_price,
                "discount_applied": discount
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Không thể thêm hóa đơn!", "error": str(e)}), 400

    return jsonify({"message": "Lỗi yêu cầu, cần user_id và address."}), 400

# Lấy tất cả hóa đơn
def get_all_hoa_don_service():
    invoices = Hoa_Don.query.all()
    if invoices:
        invoice_list = [{
            "id": invoice.id,
            "user_id": invoice.user_id,
            "book_id": invoice.book_id,
            "quantity": invoice.quantity,
            "price": invoice.price,
            "sum_price": invoice.sum_price,
            "information": invoice.information,
            "address": invoice.address,
            "phone_number": invoice.phone_number,
            "tt_hoadon": invoice.tt_hoadon,
            "date": invoice.date.strftime("%Y-%m-%d") if invoice.date else None
        } for invoice in invoices]
        return jsonify(invoice_list), 200
    return jsonify({"message": "Không tìm thấy hóa đơn nào!"}), 404


# Lấy hóa đơn theo ID
def get_hoa_don_by_id_service(invoice_id):
    invoice = Hoa_Don.query.get(invoice_id)
    if invoice:
        invoice_details = {
            "id": invoice.id,
            "user_id": invoice.user_id,
            "book_id": invoice.book_id,
            "quantity": invoice.quantity,
            "price": invoice.price,
            "sum_price": invoice.sum_price,
            "information": invoice.information,
            "address": invoice.address,
            "phone_number": invoice.phone_number,
            "tt_hoadon": invoice.tt_hoadon,
            "date": invoice.date.strftime("%Y-%m-%d") if invoice.date else None
        }
        return jsonify(invoice_details), 200
    return jsonify({"message": "Hóa đơn không tìm thấy!"}), 404


# Cập nhật hóa đơn
def update_hoa_don_service(invoice_id):
    data = request.json
    invoice = Hoa_Don.query.get(invoice_id)

    if invoice:
        invoice.user_id = data.get('user_id', invoice.user_id)
        invoice.book_id = data.get('book_id', invoice.book_id)
        invoice.quantity = data.get('quantity', invoice.quantity)
        invoice.price = data.get('price', invoice.price)
        invoice.sum_price = data.get('sum_price', invoice.sum_price)
        invoice.information = data.get('information', invoice.information)
        invoice.address = data.get('address', invoice.address)
        invoice.phone_number = data.get('phone_number', invoice.phone_number)
        invoice.tt_hoadon = data.get('tt_hoadon', invoice.tt_hoadon)
        invoice.date = datetime.strptime(data['date'], "%Y-%m-%d") if 'date' in data else invoice.date

        try:
            db.session.commit()
            return jsonify({"message": "Hóa đơn đã được cập nhật thành công!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Không thể cập nhật hóa đơn!", "error": str(e)}), 400
    return jsonify({"message": "Hóa đơn không tìm thấy!"}), 404


# Phê duyệt hóa đơn
def approve_hoa_don(invoice_id):
    invoice = Hoa_Don.query.get(invoice_id)
    if invoice:
        invoice.tt_hoadon = "Đã phê duyệt, chờ giao hàng"
        try:
            db.session.commit()
            return jsonify({"message": "Hóa đơn đã được phê duyệt thành công!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Không thể phê duyệt hóa đơn!", "error": str(e)}), 400
    return jsonify({"message": "Hóa đơn không tìm thấy!"}), 404

# tu choichoi hóa đơn
def tu_choi_hoa_don(invoice_id):
    invoice = Hoa_Don.query.get(invoice_id)
    if invoice:
        invoice.tt_hoadon = "Tù chối phục vụ"
        try:
            db.session.commit()
            return jsonify({"message": "Hóa đơn đã được phê duyệt thành công!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Không thể phê duyệt hóa đơn!", "error": str(e)}), 400
    return jsonify({"message": "Hóa đơn không tìm thấy!"}), 404

# Phê duyệt tất cả hóa đơn
def approve_all_hoa_don():
    invoices = Hoa_Don.query.filter_by(tt_hoadon="Chờ xác nhận").all()
    if not invoices:
        return jsonify({"message": "Không có hóa đơn nào cần phê duyệt!"}), 404

    for invoice in invoices:
        invoice.tt_hoadon = "Đã phê duyệt"

    try:
        db.session.commit()
        return jsonify({"message": "Tất cả hóa đơn đã được phê duyệt thành công!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Không thể phê duyệt hóa đơn!", "error": str(e)}), 400


# Xóa hóa đơn
def delete_hoa_don_service(invoice_id):
    invoice = Hoa_Don.query.get(invoice_id)
    if invoice:
        try:
            db.session.delete(invoice)
            db.session.commit()
            return jsonify({"message": "Hóa đơn đã được xóa thành công!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Không thể xóa hóa đơn!", "error": str(e)}), 400
    return jsonify({"message": "Hóa đơn không tìm thấy!"}), 404


# Lấy hóa đơn theo user_id
def get_invoices_by_user_service(user_id):
    invoices = Hoa_Don.query.filter_by(user_id=user_id).all()
    if invoices:
        invoice_list = [{
            "id": invoice.id,
            "book_id": invoice.book_id,
            "quantity": invoice.quantity,
            "price": invoice.price,
            "sum_price": invoice.sum_price,
            "information": invoice.information,
            "address": invoice.address,
            "phone_number": invoice.phone_number,
            "tt_hoadon": invoice.tt_hoadon,
            "date": invoice.date.strftime("%Y-%m-%d") if invoice.date else None
        } for invoice in invoices]
        return jsonify(invoice_list), 200
    return jsonify({"message": "Không tìm thấy hóa đơn nào cho người dùng này!"}), 404


# Đếm hóa đơn theo ngày
def count_invoices_for_specific_day(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    invoice_count = db.session.query(func.count(Hoa_Don.id)).filter(func.date(Hoa_Don.date) == date_obj.date()).scalar()
    return jsonify({"date": date_str, "total_invoices": invoice_count}), 200


# Đếm hóa đơn theo tháng
def count_invoices_for_specific_month(month_str):
    month_obj = datetime.strptime(month_str, "%Y-%m")
    invoice_count = db.session.query(func.count(Hoa_Don.id)).filter(
        func.extract('year', Hoa_Don.date) == month_obj.year,
        func.extract('month', Hoa_Don.date) == month_obj.month
    ).scalar()
    return jsonify({"month": month_str, "total_invoices": invoice_count}), 200

def count_invoices_for_specific_year(year_str):
    # Kiểm tra và chuyển đổi chuỗi năm thành số nguyên
    if not year_str:
        return jsonify({"message": "Vui lòng cung cấp năm!"}), 400
    try:
        year = int(year_str)
    except ValueError:
        return jsonify({"message": "Năm không hợp lệ!"}), 400

    # Truy vấn số lượng hóa đơn cho năm cụ thể từ bảng hoa_don mới
    invoice_count = db.session.query(func.count(Hoa_Don.id)) \
        .filter(func.extract('year', Hoa_Don.date) == year) \
        .scalar()

    # Kiểm tra và trả về kết quả
    if invoice_count and invoice_count > 0:
        return jsonify({
            "year": year_str,
            "total_invoices": invoice_count
        }), 200
    else:
        return jsonify({
            "message": f"Không có hóa đơn nào cho năm {year_str}!"
        }), 404
