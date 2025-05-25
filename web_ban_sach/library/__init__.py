from flask import Flask, request, Blueprint
from .books.controller import books
from .Cart.controller import cart
from .image.controller import images
from library.User.controller import user_bp
from library.Hoa_Don.controller import hoa_don_bp
from library.Quantri.controller import quan_tri_bp
from library.Voucher.controller import voucher_bp
# from library.after_cart.controller import After_Cart_bp
from .extension import db, ma
from .model import User, Books, Author, Category,Cart,Img
import os
from flask import Flask
from flask_cors import CORS



def create_db(app):
    if not os.path.exists("library/library.db"):
        with app.app_context():
            db.create_all()
            print("Created DB!")


def create_app(config_file="config.py"):
    app = Flask(__name__)
    CORS(app) #Khởi tạo cord để máy ngoài server cũng có thể truy cập vào
    app.config.from_pyfile(config_file)
    db.init_app(app)
    ma.init_app(app)
    create_db(app)
    app.register_blueprint(cart)
    app.register_blueprint(books)
    app.register_blueprint(images)
    app.register_blueprint(user_bp)
    app.register_blueprint(hoa_don_bp)
    app.register_blueprint(quan_tri_bp)
    app.register_blueprint(voucher_bp)
    # app.register_blueprint(After_Cart_bp)
    return app