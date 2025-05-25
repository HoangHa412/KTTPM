const updateBookApi = "http://127.0.0.1:5000/book-management/update_book";

// Hàm khởi tạo
function start() {
    handleUpdateButton(); // Đăng ký hàm xử lý sự kiện nút cập nhật
}

// Hàm xử lý khi nhấn nút cập nhật
function handleUpdateButton() {
    var button = document.getElementById('cap_nhat'); // Lấy nút "Cập nhật" theo ID

    button.onclick = function(e) {
        e.preventDefault(); // Ngăn chặn hành động mặc định của nút

        // Lấy dữ liệu từ các trường trong form
        var id = parseInt(document.getElementById('bookid').value); // ID sách cần cập nhật
        var name = document.getElementById('bookName').value;
        var pageCount = parseInt(document.getElementById('pageCount').value);
        var authorId = parseInt(document.getElementById('authorId').value);
        var categoryId = parseInt(document.getElementById('categoryId').value);

        // Kiểm tra nếu các trường đều có giá trị hợp lệ
        if (id && name && !isNaN(pageCount) && !isNaN(authorId) && !isNaN(categoryId)) {
            const data = {
                name: name,
                page_count: pageCount,
                author_id: authorId,
                category_id: categoryId
            };
            updateBook(id, data); // Gửi yêu cầu cập nhật thông tin sách
        } else {
            alert("Vui lòng điền đầy đủ thông tin hợp lệ"); // Thông báo nếu có trường không hợp lệ
        }
    }
}

// Hàm gửi yêu cầu cập nhật sách đến API
function updateBook(id, data) {
    const options = {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    };
    // Đường dẫn API cho yêu cầu PUT, sử dụng id sách để cập nhật
    const url = `${updateBookApi}/${id}`;

    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Sách đã được cập nhật thành công:", data); // Thông báo thành công
            alert("Cập nhật sách thành công!"); // Thông báo thành công cho người dùng
        })
        .catch(error => {
            console.error('Lỗi khi cập nhật sách:', error);
            alert("Không thể cập nhật sách. Vui lòng kiểm tra lại.");
        });
}

// Gọi hàm khởi tạo
start();
