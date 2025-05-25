import requests
import base64

def send_image_to_api_base64(image_path):
    # Đọc ảnh và chuyển thành base64
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
    
    # Gửi yêu cầu POST lên API với ảnh base64
    url = 'http://localhost:5000/image-management/add_img'  # Đảm bảo URL này chính xác với API của bạn
    data = {
        'book_id': 1,  # Đảm bảo book_id tồn tại trong cơ sở dữ liệu
        'image_data': encoded_image  # Phải sử dụng đúng tên trường mà API mong đợi
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:  # Kiểm tra mã thành công là 200 như trong API
        print("Image uploaded successfully!")
    else:
        print(f"Failed to upload image. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Ví dụ sử dụng
send_image_to_api_base64('IMG_4766.jpg')
