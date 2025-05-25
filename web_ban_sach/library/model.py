from .extension import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    phone_numbers = db.Column(db.Integer)

    def __init__(self, name, address, phone_numbers):
        self.name = name
        self.address = address
        self.phone_numbers = phone_numbers



class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    page_count = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, name, page_count, author_id, category_id):
        self.name = name
        self.page_count = page_count
        self.author_id = author_id
        self.category_id = category_id

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))  # Đảm bảo 'books.id' là đúng
    image_data = db.Column(db.String, nullable=False)

    def __init__(self, image_data, book_id):
        self.book_id = book_id
        self.image_data = image_data

    
class Quantriuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Thêm trường ID cho Quantriuser
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Liên kết đến bảng User
    account_user = db.Column(db.String, nullable=False, unique=True)
    password_user = db.Column(db.String, nullable=False)

    def __init__(self, user_id, account_user, password_user):
        self.user_id = user_id  # Lưu ID người dùng
        self.account_user = account_user
        self.password_user = password_user


class QuanTriAdmin(db.Model):
    account_admin = db.Column(db.String, primary_key=True)
    password_admin = db.Column(db.String)

    def __init__(self,account_admin,password_admin):
        self.account_admin = account_admin
        self.password_admin = password_admin

class Voucher(db.Model):
    makhuyenmai = db.Column(db.String,primary_key=True)
    tylekm = db.Column(db.Integer)

    def __init__(self,makhuyenmai,tylekm):
        self.makhuyenmai = makhuyenmai
        self.tylekm = tylekm

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Liên kết đến bảng User
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  # Số lượng sách
    price = db.Column(db.Integer, nullable=False)  # Giá sách

    def __init__(self, user_id, book_id, quantity, price):
        self.user_id = user_id
        self.book_id = book_id
        self.quantity = quantity
        self.price = price

class Hoa_Don(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Liên kết đến bảng User
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)  # Liên kết đến bảng Books
    quantity = db.Column(db.Integer, nullable=False)  # Số lượng sách
    price = db.Column(db.Integer, nullable=False)  # Giá sách
    information = db.Column(db.String(255), nullable=False)  # Trường information bắt buộc
    address = db.Column(db.String(255), nullable=False)  # Địa chỉ, bắt buộc
    phone_number = db.Column(db.String(20), nullable=False)  # Số điện thoại, bắt buộc
    sum_price = db.Column(db.Float, nullable=False)  # Tổng giá, bắt buộc
    date = db.Column(db.Date)  # Ngày
    tt_hoadon = db.Column(db.String(50), nullable=False)  # Trạng thái hóa đơn, bắt buộc
    loai_thanhtoan = db.Column(db.String(50), nullable=False)  # Loại thanh toán, bắt buộc

    def __init__(self, user_id, book_id, quantity,loai_thanhtoan, price, information, address, phone_number, sum_price, tt_hoadon, date=None):
        self.user_id = user_id
        self.book_id = book_id
        self.quantity = quantity
        self.price = price
        self.information = information  # Khởi tạo trường information
        self.address = address
        self.phone_number = phone_number
        self.sum_price = sum_price
        self.tt_hoadon = tt_hoadon  
        self.date = date
        self.loai_thanhtoan=loai_thanhtoan