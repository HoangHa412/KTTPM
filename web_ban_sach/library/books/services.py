from library.extension import db
from library.library_ma import BookSchema, AuthorSchema
from library.model import Author, Books, Category
from flask import request, jsonify
from sqlalchemy.sql import func

# Khởi tạo schema cho sách và tác giả
book_schema = BookSchema()
books_schema = BookSchema(many=True)
author_schema = AuthorSchema()

# def add_book_service():
#     data = request.json
#     if (data and ('name' in data) and ('page_count' in data)
#             and ('author_id' in data) and ('category_id' in data)):
#         name = data['name']
#         page_count = data['page_count']
#         author_id = data['author_id']
#         category_id = data['category_id']

#         new_book = Books(name=name, page_count=page_count, author_id=author_id, category_id=category_id)
#         try:
#             db.session.add(new_book)
#             db.session.commit()
#             return jsonify({"message": "Add success!", "book_id": new_book.id}), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"message": "Cannot add book!", "error": str(e)}), 400
#     else:
#         return jsonify({"message": "Request error"}), 400

def add_book_service():
    data = request.json
    if data and ('name' in data) and ('page_count' in data) and ('author_name' in data) and ('category_id' in data):
        name = data['name']
        page_count = data['page_count']
        author_name = data['author_name']
        category_id = data['category_id']

        # Kiểm tra hoặc thêm tác giả vào bảng Author
        try:
            author = Author.query.filter_by(name=author_name).first()
            if not author:
                # Nếu tác giả chưa tồn tại, thêm mới
                author = Author(name=author_name)
                db.session.add(author)
                db.session.commit()  # Commit để lấy ID mới
            author_id = author.id

            # Tạo và thêm sách vào bảng Books
            new_book = Books(name=name, page_count=page_count, author_id=author_id, category_id=category_id)
            db.session.add(new_book)
            db.session.commit()
            return jsonify({"message": "Add success!", "book_id": new_book.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot add book!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Request error"}), 400


def get_book_by_id_service(book_id):
    book = Books.query.get(book_id)
    if book:
        author = Author.query.get(book.author_id)
        author_name = author.name if author else "Unknown"
        book_data = book_schema.dump(book)
        book_data['author_name'] = author_name
        return jsonify(book_data), 200
    else:
        return jsonify({"message": "Book not found"}), 404


def get_all_books_service():
    books = Books.query.all()
    all_books_data = []
    if books:
        for book in books:
            author = Author.query.get(book.author_id)
            author_name = author.name if author else "Unknown"
            category = Category.query.get(book.category_id)
            category_name = category.name if category else "Unknown"
            book_data = book_schema.dump(book)
            book_data['author_name'] = author_name
            book_data['category_name'] = category_name
            all_books_data.append(book_data)
        return jsonify(all_books_data), 200
    else:
        return jsonify({"message": "No books found!"}), 404


def update_book_by_id_service(book_id):
    book = Books.query.get(book_id)
    data = request.json
    if book:
        if data:
            if "name" in data:
                book.name = data["name"]
            if "page_count" in data:
                book.page_count = data["page_count"]
            if "author_id" in data:
                book.author_id = data["author_id"]
            if "category_id" in data:
                book.category_id = data["category_id"]
            try:
                db.session.commit()
                return jsonify({"message": "Book updated successfully!"}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": "Cannot update book!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Book not found!"}), 404


def delete_book_by_id_service(book_id):
    book = Books.query.get(book_id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
            return jsonify({"message": "Book deleted successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot delete book!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Book not found!"}), 404


def get_books_by_author_service(author_name):
    books = Books.query.join(Author).filter(
        func.lower(Author.name) == author_name.lower()).all()
    if books:
        return books_schema.jsonify(books), 200
    else:
        return jsonify({"message": f"No books found by author: {author_name}"}), 404
    
def get_books_by_category_id_service(category_id):
    books = Books.query.filter_by(category_id=category_id).all()
    if books:
        all_books_data = []
        for book in books:
            author = Author.query.get(book.author_id)
            author_name = author.name if author else "Unknown"
            category = Category.query.get(book.category_id)
            category_name = category.name if category else "Unknown"
            book_data = book_schema.dump(book)
            book_data['author_name'] = author_name
            book_data['category_name'] = category_name
            all_books_data.append(book_data)
        return jsonify(all_books_data), 200
    else:
        return jsonify({"message": f"No books found in category: {category_id}"}), 404
        
def count_books():
    books = Books.query.all()
    all_books_data = []
    if books:
        for book in books:
            book_data = book_schema.dump(book)
            all_books_data.append(book_data)
        count_book = len(all_books_data)
        return jsonify({"tongSoLuongSach": count_book})
    else:
        return jsonify({"message": "No books found!"}), 404
