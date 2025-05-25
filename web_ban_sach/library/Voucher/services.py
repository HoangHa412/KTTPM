from library.extension import db
from library.library_ma import Hoa_DonSchema
from library.model import User, Books, Cart, Hoa_Don, Voucher
from flask import request, jsonify

def add_voucher():
    data = request.json
    makhuyenmai = data.get('makhuyenmai')
    tylekm = data.get('tylekm')

    if not makhuyenmai or tylekm is None:
        return jsonify({"message": "Cần cung cấp mã khuyến mãi và tỷ lệ khuyến mãi!"}), 400

    # Kiểm tra mã khuyến mãi đã tồn tại chưa
    existing_voucher = Voucher.query.filter_by(makhuyenmai=makhuyenmai).first()
    if existing_voucher:
        return jsonify({"message": "Mã khuyến mãi đã tồn tại!"}), 400

    # Thêm voucher mới
    new_voucher = Voucher(makhuyenmai=makhuyenmai, tylekm=tylekm)
    db.session.add(new_voucher)
    try:
        db.session.commit()
        return jsonify({"message": "Thêm mã khuyến mãi thành công!", "voucher": {"makhuyenmai": makhuyenmai, "tylekm": tylekm}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Không thể thêm mã khuyến mãi!", "error": str(e)}), 400

def update_voucher(makhuyenmai):
    data = request.json
    tylekm = data.get('tylekm')

    if tylekm is None:
        return jsonify({"message": "Cần cung cấp tỷ lệ khuyến mãi!"}), 400

    # Tìm voucher cần cập nhật
    voucher = Voucher.query.filter_by(makhuyenmai=makhuyenmai).first()
    if not voucher:
        return jsonify({"message": "Mã khuyến mãi không tồn tại!"}), 404

    # Cập nhật tỷ lệ khuyến mãi
    voucher.tylekm = tylekm
    try:
        db.session.commit()
        return jsonify({"message": "Cập nhật mã khuyến mãi thành công!", "voucher": {"makhuyenmai": makhuyenmai, "tylekm": tylekm}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Không thể cập nhật mã khuyến mãi!", "error": str(e)}), 400

def delete_voucher(makhuyenmai):
    # Tìm voucher cần xóa
    voucher = Voucher.query.filter_by(makhuyenmai=makhuyenmai).first()
    if not voucher:
        return jsonify({"message": "Mã khuyến mãi không tồn tại!"}), 404

    # Xóa voucher
    db.session.delete(voucher)
    try:
        db.session.commit()
        return jsonify({"message": "Xóa mã khuyến mãi thành công!", "makhuyenmai": makhuyenmai}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Không thể xóa mã khuyến mãi!", "error": str(e)}), 400

def delete_all_vouchers():
    try:
        # Xóa tất cả các bản ghi trong bảng Voucher
        num_deleted = db.session.query(Voucher).delete()
        db.session.commit()
        return jsonify({"message": f"Đã xóa thành công {num_deleted} mã khuyến mãi!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Không thể xóa tất cả mã khuyến mãi!", "error": str(e)}), 400

def get_voucher_by_code(makhuyenmai):
    # Tìm voucher theo makhuyenmai
    voucher = Voucher.query.filter_by(makhuyenmai=makhuyenmai).first()
    
    if not voucher:
        return jsonify({"message": "Mã khuyến mãi không tồn tại!"}), 404

    # Trả về thông tin voucher dưới dạng JSON
    return jsonify({
        "makhuyenmai": voucher.makhuyenmai,
        "tylekm": voucher.tylekm
    }), 200

def get_all_vouchers():
    # Lấy tất cả các voucher từ cơ sở dữ liệu
    vouchers = Voucher.query.all()

    if not vouchers:
        return jsonify({"message": "Không có mã khuyến mãi nào!"}), 404

    # Trả về danh sách voucher dưới dạng JSON
    vouchers_list = []
    for voucher in vouchers:
        vouchers_list.append({
            "makhuyenmai": voucher.makhuyenmai,
            "tylekm": voucher.tylekm
        })

    return jsonify(vouchers_list), 200
