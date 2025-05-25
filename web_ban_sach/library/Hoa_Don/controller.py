from flask import Blueprint
from .services import (add_hoa_don_service,tu_choi_hoa_don,approve_all_hoa_don,approve_hoa_don,count_invoices_for_specific_year,count_invoices_for_specific_month,count_invoices_for_specific_day, get_invoices_by_user_service,get_all_hoa_don_service, get_hoa_don_by_id_service, update_hoa_don_service, delete_hoa_don_service)

hoa_don_bp = Blueprint("HoaDon", __name__)

@hoa_don_bp.route("/add_hoa_don", methods=['POST'])
def add_hoa_don():
    return add_hoa_don_service()

@hoa_don_bp.route("/hoa_don", methods=['GET'])
def get_all_hoa_don():
    return get_all_hoa_don_service()

@hoa_don_bp.route("/hoa_don/<int:invoice_id>", methods=['GET'])
def get_hoa_don_by_id(invoice_id):
    return get_hoa_don_by_id_service(invoice_id)

@hoa_don_bp.route("/hoa_don/<int:invoice_id>", methods=['PUT'])
def update_hoa_don(invoice_id):
    return update_hoa_don_service(invoice_id)
#phê duyệt hóa đơn theo idid
@hoa_don_bp.route("/phe_duyet_hoa_don/<int:invoice_id>", methods=['PUT'])
def phe_duyet_hoa_don(invoice_id):
    return approve_hoa_don(invoice_id)
#phê duyệt hóa đơn theo idid
@hoa_don_bp.route("/tu_choi_hoa_don/<int:invoice_id>", methods=['PUT'])
def tu_choi_hoa_don_1(invoice_id):
    return tu_choi_hoa_don(invoice_id)
#Phê duyệt tất cả hóa đơn 
@hoa_don_bp.route("/phe_duyet_all_hoa_don", methods=['PUT'])
def phe_duyet_all_hoa_don():
    return approve_all_hoa_don()
#DELETE hoa don
@hoa_don_bp.route("/hoa_don/<int:invoice_id>", methods=['DELETE'])
def delete_hoa_don(invoice_id):
    return delete_hoa_don_service(invoice_id)
#Get hoa don theo user id
@hoa_don_bp.route("/hoa_don_user_id/<int:user_id>", methods=['GET'])
def get_hoa_don_user(user_id):
    return get_invoices_by_user_service(user_id)
#Lấy hóa đơn theo ngày
@hoa_don_bp.route("/hoa_don_date/<string:date_str>", methods=['GET'])
def count_hoa_don_by_date( date_str):
    return count_invoices_for_specific_day( date_str)

#Lấy hóa đơn theo tháng
@hoa_don_bp.route("/hoa_don_month/<string:date_str>", methods=['GET'])
def count_hoa_don_by_month( date_str):
    return count_invoices_for_specific_month(date_str)

@hoa_don_bp.route("/hoa_don_year/<string:date_str>", methods=['GET'])
def count_hoa_don_by_year( date_str):
    return count_invoices_for_specific_year(date_str)
