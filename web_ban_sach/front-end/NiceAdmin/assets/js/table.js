const getBooksByCategoryApi = "http://127.0.0.1:5000/book-management/category";

// Hàm lấy sách theo thể loại
function loadBooksByCategory(categoryId) {
    return fetch(`${getBooksByCategoryApi}/${categoryId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
}

// Hàm hiển thị sách trong bảng
function displayBooksInTable(categoryId, books) {
    const tableBody = document.querySelector(`#category-${categoryId}-table tbody`);
    tableBody.innerHTML = ''; // Xóa dữ liệu cũ

    if (books.length > 0) {
        const htmls = books.map((book, index) => `
            <tr>
                <th scope="row">${index + 1}</th>
                <td>${book.name}</td>
                <td>${book.page_count}</td>
                <td>${book.author_name}</td>
                <td>${book.category_name || 'N/A'}</td> 
            </tr>
        `).join('');
        tableBody.innerHTML = htmls;
    } else {
        tableBody.innerHTML = '<tr><td colspan="4">Không có sách nào trong thể loại này.</td></tr>';
    }
}

// Hàm khởi tạo
function start() {
    const categories = [1, 2, 3, 4, 5]; // Danh sách các thể loại
    categories.forEach(categoryId => {
        loadBooksByCategory(categoryId)
            .then(books => displayBooksInTable(categoryId, books))
            .catch(error => console.error(`Error loading books for category ${categoryId}:`, error));
    });
}

// Gọi hàm khởi tạo
start();

