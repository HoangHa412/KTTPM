from flask import Blueprint
from .services import (
    add_voucher,
    update_voucher,
    delete_voucher,
    delete_all_vouchers,
    get_voucher_by_code,
    get_all_vouchers
)

# Tạo Blueprint cho các API voucher
voucher_bp = Blueprint("Voucher", __name__)

@voucher_bp.route("/add_voucher", methods=['POST'])
def addd_voucher():
    return add_voucher()

@voucher_bp.route("/update_voucher/<string:makhuyenmai>", methods=['PUT'])
def updateee_voucher(makhuyenmai):
    return update_voucher(makhuyenmai)

@voucher_bp.route("/delete_voucher/<string:makhuyenmai>", methods=['DELETE'])
def deleteee_voucher(makhuyenmai):
    return delete_voucher(makhuyenmai)

@voucher_bp.route("/delete_all_vouchers", methods=['DELETE'])
def deletee_all_vouchers():
    return delete_all_vouchers()

@voucher_bp.route('/get_voucher_by_idid/<string:makhuyenmai>', methods=['GET'])
def get_voucher(makhuyenmai):
    return get_voucher_by_code(makhuyenmai)

@voucher_bp.route('/get_all_vouchers', methods=['GET'])
def get_vouchers():
    return get_all_vouchers()
