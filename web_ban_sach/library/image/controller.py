from flask import Blueprint, jsonify
from .services import (add_img_service,get_all_images_service,delete_images_by_book_id_service)
images = Blueprint("images", __name__)

@images.route("/image-management/add_img", methods=['POST'])
def add_img():
    return add_img_service()

@images.route('/images/<int:book_id>', methods=['GET'])
def get_img(book_id):
    try:
        # Gọi hàm lấy ảnh và trả về phản hồi
        response = get_all_images_service(book_id)
        return response  # Đảm bảo rằng phản hồi từ hàm là hợp lệ
    except Exception as e:
        print(f"Error in get_img: {str(e)}")
        return jsonify({"message": "Error fetching images.", "error": str(e)}), 500
    
@images.route('/delete_images/<int:book_id>', methods=['DELETE'])
def delete_images_by_book_id(book_id):
    return delete_images_by_book_id_service(book_id)
