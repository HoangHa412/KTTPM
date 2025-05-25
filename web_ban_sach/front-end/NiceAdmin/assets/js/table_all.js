const getBooksApi = "http://127.0.0.1:5000/book-management/books";

// Hàm lấy tất cả sách
function loadBooks() {
    return fetch(getBooksApi)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
}

// Hàm hiển thị sách trong bảng
function displayBooksInTable(books) {
    const tableBody = document.querySelector('.datatable tbody');
    tableBody.innerHTML = ''; // Xóa dữ liệu cũ

    if (books && books.length > 0) {
        const htmls = books.map((book, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${book.name}</td>
                <td>${book.page_count || 'N/A'}</td>
                <td>${book.author_name}</td>
                <td>${book.category_name || 'N/A'}</td> 
            </tr>
        `).join('');
        tableBody.innerHTML = htmls;
    } else {
        tableBody.innerHTML = '<tr><td colspan="5">Không có sách nào.</td></tr>';
    }
}

// Hàm khởi tạo
function start() {
    loadBooks()
        .then(books => displayBooksInTable(books))
        .catch(error => console.error('Error loading books:', error));
}

// Gọi hàm khởi tạo khi trang đã tải xong
document.addEventListener('DOMContentLoaded', start);
