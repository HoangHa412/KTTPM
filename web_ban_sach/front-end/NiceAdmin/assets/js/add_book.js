const getBookApi = "http://127.0.0.1:5000/book-management/books";
const addBookApi = "http://127.0.0.1:5000/book-management/book";

// Hàm khởi tạo
function start() {
    handleCreateForm(); // Đăng ký hàm xử lý form
}

// Hàm validation chi tiết
function validateBookForm(name, pageCount, authorId, categoryId) {
    // Kiểm tra tên sách
    if (!name || name.trim() === '') {
        alert("❌ Lỗi: Tên sách không được để trống!");
        return false;
    }
    
    if (name.length > 100) {
        alert("❌ Lỗi: Tên sách không được quá 100 ký tự!");
        return false;
    }

    // Kiểm tra số trang
    if (!pageCount || pageCount === '') {
        alert("❌ Lỗi: Số trang không được để trống!");
        return false;
    }
    
    if (isNaN(pageCount)) {
        alert("❌ Lỗi: Số trang phải là số nguyên!");
        return false;
    }
    
    const pageNum = parseInt(pageCount);
    if (pageNum <= 0) {
        alert("❌ Lỗi: Số trang phải lớn hơn 0!");
        return false;
    }
    
    if (pageNum > 10000) {
        alert("❌ Lỗi: Số trang không thể quá 10,000 trang!");
        return false;
    }

    // Kiểm tra ID tác giả
    if (!authorId || authorId.trim() === '') {
        alert("❌ Lỗi: ID tác giả không được để trống!");
        return false;
    }
    
    // Kiểm tra ký tự đặc biệt trong ID tác giả (chỉ cho phép chữ, số, _, -)
    const authorIdRegex = /^[a-zA-Z0-9_-]+$/;
    if (!authorIdRegex.test(authorId.trim())) {
        alert("❌ Lỗi: ID tác giả chỉ được chứa chữ cái, số, dấu gạch dưới (_) và gạch ngang (-)!");
        return false;
    }

    // Kiểm tra thể loại
    if (!categoryId || categoryId === '') {
        alert("❌ Lỗi: Thể loại không được để trống!");
        return false;
    }
    
    if (isNaN(categoryId)) {
        alert("❌ Lỗi: Thể loại phải là số nguyên!");
        return false;
    }
    
    const catNum = parseInt(categoryId);
    if (catNum <= 0) {
        alert("❌ Lỗi: Thể loại phải lớn hơn 0!");
        return false;
    }
    
    if (catNum > 1000) {
        alert("❌ Lỗi: Thể loại vượt quá giới hạn cho phép (tối đa 1000)!");
        return false;
    }

    return true;
}

// Hàm xử lý khi gửi form
function handleCreateForm() {
    var form = document.getElementById('book-form');

    form.onsubmit = function(e) {
        e.preventDefault(); // Ngăn chặn hành động gửi form mặc định

        // Lấy dữ liệu từ các trường trong form
        var name = document.getElementById('bookName').value;
        var pageCount = document.getElementById('pageCount').value;
        var author_name = document.getElementById('authorId').value;
        var categoryId = document.getElementById('categoryId').value;

        // Validation chi tiết
        if (!validateBookForm(name, pageCount, author_name, categoryId)) {
            return; // Dừng lại nếu validation thất bại
        }

        // Nếu validation thành công, tạo data object
        const data = {
            name: name.trim(),
            page_count: parseInt(pageCount),
            author_name: author_name.trim(),
            category_id: parseInt(categoryId)
        };
        
        // Hiển thị thông báo đang xử lý
        alert("⏳ Đang xử lý thêm sách...");
        
        createBook(data); // Gửi dữ liệu tới API để thêm sách
    }
}

// Hàm gửi yêu cầu thêm sách đến API
function createBook(data) {
    const options = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    fetch(addBookApi, options)
        .then(response => {
            if (!response.ok) {
                // Xử lý các mã lỗi HTTP khác nhau
                if (response.status === 400) {
                    throw new Error('❌ Dữ liệu không hợp lệ. Vui lòng kiểm tra lại thông tin!');
                } else if (response.status === 409) {
                    throw new Error('❌ Sách đã tồn tại trong hệ thống!');
                } else if (response.status === 500) {
                    throw new Error('❌ Lỗi server. Vui lòng thử lại sau!');
                } else {
                    throw new Error(`❌ Lỗi HTTP ${response.status}: ${response.statusText}`);
                }
            }
            return response.json();
        })
        .then(data => {
            console.log("Sách đã được thêm thành công:", data);
            alert("✅ Thêm sách mới thành công!\n\n📚 Tên sách: " + data.name + "\n📄 Số trang: " + data.page_count + "\n✍️ Tác giả: " + data.author_name + "\n📂 Thể loại ID: " + data.category_id);
            
            // Reset form sau khi thành công
            document.getElementById('book-form').reset();
        })
        .catch(error => {
            console.error('Lỗi khi thêm sách:', error);
            alert(error.message || "❌ Không thể thêm sách. Vui lòng kiểm tra lại thông tin và thử lại!");
        });
}

// Thêm validation real-time cho các trường
function addRealTimeValidation() {
    // Validation tên sách
    const bookNameField = document.getElementById('bookName');
    bookNameField.addEventListener('blur', function() {
        const value = this.value.trim();
        if (value && value.length > 100) {
            alert("⚠️ Cảnh báo: Tên sách quá dài (tối đa 100 ký tự)!");
        }
    });

    // Validation số trang
    const pageCountField = document.getElementById('pageCount');
    pageCountField.addEventListener('blur', function() {
        const value = parseInt(this.value);
        if (this.value && (isNaN(value) || value <= 0)) {
            alert("⚠️ Cảnh báo: Số trang phải là số nguyên dương!");
        } else if (value > 10000) {
            alert("⚠️ Cảnh báo: Số trang không thể quá 10,000!");
        }
    });

    // Validation ID tác giả
    const authorIdField = document.getElementById('authorId');
    authorIdField.addEventListener('blur', function() {
        const value = this.value.trim();
        const regex = /^[a-zA-Z0-9_-]+$/;
        if (value && !regex.test(value)) {
            alert("⚠️ Cảnh báo: ID tác giả chỉ được chứa chữ cái, số, dấu gạch dưới (_) và gạch ngang (-)!");
        }
    });

    // Validation thể loại
    const categoryIdField = document.getElementById('categoryId');
    categoryIdField.addEventListener('blur', function() {
        const value = parseInt(this.value);
        if (this.value && (isNaN(value) || value <= 0)) {
            alert("⚠️ Cảnh báo: Thể loại phải là số nguyên dương!");
        } else if (value > 1000) {
            alert("⚠️ Cảnh báo: Thể loại vượt quá giới hạn (tối đa 1000)!");
        }
    });
}

// Gọi hàm khởi tạo
start();
// Thêm validation real-time sau khi DOM load
document.addEventListener('DOMContentLoaded', addRealTimeValidation);
