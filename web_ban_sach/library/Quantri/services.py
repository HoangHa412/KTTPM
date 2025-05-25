from datetime import datetime
from library.extension import db
from library.library_ma import BookSchema, AuthorSchema
from library.model import QuanTriAdmin,Quantriuser,User
from flask import request, jsonify
from sqlalchemy.sql import func
import json
# def get_admin_credentials():
#     admins = QuanTriAdmin.query.all()
#     return [{"account_admin": admin.account_admin, "password_admin": admin.password_admin} for admin in admins]
# def get_user_credentials():
#     users = Quantriuser.query.all()
#     return [{"account_user": user.account_user, "password_user": user.password_user} for user in users]
def get_admin_account_and_password(account_admin):
    """
    Lấy tài khoản và mật khẩu của Admin dựa trên account_admin.
    """
    admin_account = QuanTriAdmin.query.filter_by(account_admin=account_admin).first()
    if admin_account:
        return {
            "account_admin": admin_account.account_admin,
            "password_admin": admin_account.password_admin
        }
    return None
def get_user_account_and_password(account_user):
    """
    Lấy tài khoản và mật khẩu của User dựa trên user_id.
    """
    user_account = Quantriuser.query.filter_by(account_user=account_user).first()
    if user_account:
        return {
            "account_user": user_account.account_user,
            "password_user": user_account.password_user
        }

def add_admin_account(account_admin, password_admin):
    """
    Thêm tài khoản admin mới vào cơ sở dữ liệu.
    """
    # Kiểm tra nếu tài khoản admin đã tồn tại
    existing_admin = QuanTriAdmin.query.filter_by(account_admin=account_admin).first()
    if existing_admin:
        return {"message": "Admin account already exists."}, 400

    # Thêm tài khoản admin mới
    new_admin = QuanTriAdmin(account_admin=account_admin, password_admin=password_admin)
    db.session.add(new_admin)
    db.session.commit()
    return {"message": "Admin account added successfully."}, 201

def update_admin_password(account_admin, current_password, new_password):
    """
    Đổi mật khẩu cho tài khoản admin dựa trên account_admin.
    """
    # Tìm tài khoản admin trong cơ sở dữ liệu
    admin_account = QuanTriAdmin.query.filter_by(account_admin=account_admin).first()

    if not admin_account:
        return {"message": "Admin account not found."}, 404

    # Kiểm tra mật khẩu hiện tại có đúng không
    if admin_account.password_admin != current_password:
        return {"message": "Current password is incorrect."}, 400

    # Cập nhật mật khẩu mới
    admin_account.password_admin = new_password
    db.session.commit()

    return {"message": "Admin password updated successfully."}, 200


# Hàm thêm tài khoản người dùng mới
def add_user_account(name, address, phone_numbers, account_user, password_user):
    """
    Thêm tài khoản user mới vào cơ sở dữ liệu.
    """
    # Kiểm tra nếu tài khoản user đã tồn tại
    existing_user_account = Quantriuser.query.filter_by(account_user=account_user).first()
    if existing_user_account:
        return {"message": "User account already exists."}, 400

    # Tạo đối tượng User mới
    new_user = User(name=name, address=address, phone_numbers=phone_numbers)
    db.session.add(new_user)
    db.session.flush()  # Lấy ID mới tạo nhưng chưa commit

    # Tạo tài khoản người dùng mới
    new_user_account = Quantriuser(user_id=new_user.id, account_user=account_user, password_user=password_user)
    db.session.add(new_user_account)
    db.session.commit()

    return {"message": "User account added successfully.", "user_id": new_user.id}, 201

