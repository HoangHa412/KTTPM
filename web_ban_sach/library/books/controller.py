from flask import Blueprint, jsonify
from library.extension import db
from library.model import Author, Books, Category
from .services import (
    add_book_service,
    get_book_by_id_service,
    get_all_books_service,
    update_book_by_id_service,
    delete_book_by_id_service,
    get_books_by_author_service,
    get_books_by_category_id_service,
    count_books
)

books = Blueprint("Books", __name__)

# Route thêm sách
@books.route("/book-management/book", methods=['POST'])
def add_book():
    return add_book_service()

# Route lấy sách theo ID
@books.route("/book-management/book/<int:id>", methods=['GET'])
def get_book_by_id(id):
    return get_book_by_id_service(id)

# Route lấy tất cả sách
@books.route("/book-management/books", methods=['GET'])
def get_all_books():
    return get_all_books_service()

# Route cập nhật sách theo ID
@books.route("/book-management/update_book/<int:id>", methods=['PUT'])
def update_book_by_id(id):
    return update_book_by_id_service(id)

# Route xóa sách theo ID
@books.route("/book-management/delete_book/<int:id>", methods=['DELETE'])
def delete_book_by_id(id):
    return delete_book_by_id_service(id)

# Route lấy sách theo tên tác giả
@books.route("/book-management/author/<string:author>", methods=['GET'])
def get_book_by_author(author):
    return get_books_by_author_service(author)

# Route lấy sách theo thể loại
@books.route("/book-management/category/<int:author>", methods=['GET'])
def get_book_by_category(author):
    return get_books_by_category_id_service(author)

#Route lay count_books
@books.route("/book-management/count_book", methods=['GET'])
def count_book():
    return count_books()

# @books.route("/book-management/count_book", methods=['GET'])
# def count_book():
#     total_books = db.session.query(Books).count()
#     return jsonify({"tongSoLuongSach": total_books})


