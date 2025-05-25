// Khai báo các API
const getBookApi = "http://127.0.0.1:5000/book-management/books";
const getBookByIdApi = (id) => `http://127.0.0.1:5000/book-management/book/${id}`;
const addBookApi = "http://127.0.0.1:5000/book-management/book";
const getAuthorApi = "http://127.0.0.1:5000/author-management/authors";
const getCategoryApi = "http://127.0.0.1:5000/category-management/categories";
const getCartApi = "http://127.0.0.1:5000/cart_all";
const addCartApi = "http://127.0.0.1:5000/add_cart";

// Biến lưu trữ giỏ hàng
let cart = [];

// Hàm bắt đầu chương trình
function start() {
    loadBook();
    handleCreateForm();
    loadAuthor();
    loadCategory();
    loadCart();
}

start();

// Hàm cập nhật giỏ hàng trên giao diện
function updateCartDisplay(cartItems) {
    const cartTableBody = document.querySelector("#cart-table tbody");
    cartTableBody.innerHTML = ""; // Xóa nội dung cũ

    // Hiển thị từng sách trong giỏ hàng
    cartItems.forEach(item => {
        const totalPrice = item.price * item.quantity; // Thành tiền của mỗi sách
        const row = `
            <tr>
                <td><img src="path/to/book-image/${item.id}.jpg" alt="${item.name}" style="width: 50px; height: auto;"></td>
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>${item.price} VNĐ</td>
                <td>${totalPrice} VNĐ</td>
            </tr>
        `;
        cartTableBody.insertAdjacentHTML("beforeend", row); // Thêm dòng vào bảng
    });

    // Cập nhật số lượng sách trong giỏ hàng trên badge
    document.getElementById("cart-count").textContent = cartItems.reduce((sum, item) => sum + item.quantity, 0);
}

// Hàm tải giỏ hàng
async function loadCart() {
    try {
        const response = await fetch(getCartApi);
        if (!response.ok) {
            throw new Error('Cart not found');
        }

        const cartItems = await response.json();
        console.log(cartItems);
        updateCartDisplay(cartItems); // Cập nhật hiển thị giỏ hàng
        
    } catch (error) {
        console.error('Error fetching cart:', error);
    }
}

// Hàm lấy thông tin sách theo ID và xử lý khi nhấn nút "Add to Cart"
async function getBookById(id_sach, id_html_name, id_salary, id_html_page_count, id_add_to_cart_button,id_author_name) {
    try {
        const response = await fetch(getBookByIdApi(id_sach));

        if (!response.ok) {
            throw new Error('Book not found');
        }

        const book = await response.json();

        // Hiển thị tên sách
        const bookNameElement = document.getElementById(id_html_name);
        if (bookNameElement) {
            bookNameElement.textContent = `Tên sách: ${book.name}`;
        }
        // Hiển thị tên tác giả
        const authorNameElement = document.getElementById(id_author_name);
        if (authorNameElement) {
            authorNameElement.textContent = `Tên tác giả: ${book.author_name}`;
        }
        

        // Hiển thị số tiền
        const salary = parseInt(book.page_count) * 1000; // Tính tiền sách
        const bookSalaryElement = document.getElementById(id_salary);
        if (bookSalaryElement) {
            bookSalaryElement.textContent = `Giá bán: ${salary} VNĐ`;
        }

        // Hiển thị số trang
        const bookPageCountElement = document.getElementById(id_html_page_count);
        if (bookPageCountElement) {
            bookPageCountElement.textContent = `Số trang: ${book.page_count}`;
        }

        // Xử lý nút "Add to Cart"
        const addToCartButton = document.getElementById(id_add_to_cart_button);
        if (addToCartButton) {
            // Khi nhấn nút, gọi hàm addToCart và truyền vào thông tin sách
            addToCartButton.onclick = () => addToCart(book);
        }

    } catch (error) {
        console.error('Error fetching book:', error);
    }
}

// Hàm thêm sách vào giỏ hàng với số lượng
async function addToCart(book) {
    const newBook = {
        ...book,
        quantity: 1,
        price: parseInt(book.page_count) * 1000 // Tính giá tiền dựa trên số trang
    };

    // Thêm sách mới vào giỏ hàng
    cart.push(newBook);

    // Cập nhật giỏ hàng trên giao diện
    updateCart();

    // Gọi API để thêm sách vào giỏ hàng
    await addToCartApi(newBook);

    alert("Bạn đã thêm thành công cuốn sách vào giỏ hàng");
    console.log(cart); // Kiểm tra giỏ hàng trên console
}

// Hàm gửi dữ liệu lên API thêm vào giỏ hàng
async function addToCartApi(book) {
    const options = {
        method: 'POST',
        body: JSON.stringify(book),
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await fetch(addCartApi, options);
        if (!response.ok) {
            throw new Error('Error adding book to cart');
        }
        const result = await response.json();
        console.log('Added to cart:', result);
    } catch (error) {
        console.error('Error sending to addCartApi:', error);
    }
}

// Hàm cập nhật giỏ hàng và hiển thị trên giao diện
function updateCart() {
    const cartTableBody = document.querySelector("#cart-table tbody");
    cartTableBody.innerHTML = ""; // Xóa nội dung cũ

    // Hiển thị từng sách trong giỏ hàng
    cart.forEach(item => {
        const totalPrice = item.price * item.quantity; // Thành tiền của mỗi sách
        const row = `
            <tr>
                <td><img src="path/to/book-image/${item.id}.jpg" alt="${item.name}" style="width: 50px; height: auto;"></td>
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>${item.price} VNĐ</td>
                <td>${totalPrice} VNĐ</td>
            </tr>
        `;
        cartTableBody.insertAdjacentHTML("beforeend", row); // Thêm dòng vào bảng
    });

    // Cập nhật số lượng sách trong giỏ hàng trên badge
    document.getElementById("cart-count").textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
}

// Hàm tải danh sách sách
function loadBook() {
    const titleTable = "<tr><th>Id</th><th>Name</th><th>Page Count</th></tr>";
    fetch(getBookApi)
        .then(response => response.json())
        .then(books => {
            const htmls = books.map(book => `
                <tr>
                    <td>${book.id}</td>
                    <td>${book.name}</td>
                    <td>${book.page_count}</td>
                    <td>${book.author_name}<td>
                </tr>
            `);
            document.getElementById("book-block").innerHTML = titleTable + htmls.join('');
        })
        .catch(error => {
            console.error("Error loading books:", error);
        });
}

// Hàm tải danh sách tác giả
function loadAuthor() {
    fetch(getAuthorApi)
        .then(response => response.json())
        .then(authors => {
            const htmls = authors.map(author => `<option value="${author.id}">${author.name}</option>`);
            document.getElementById("author").innerHTML = '<option value=""></option>' + htmls.join('');
        })
        .catch(error => {
            console.error("Error loading authors:", error);
        });
}

// Hàm tải danh sách thể loại
function loadCategory() {
    fetch(getCategoryApi)
        .then(response => response.json())
        .then(categories => {
            const htmls = categories.map(category => `<option value="${category.id}">${category.name}</option>`);
            document.getElementById("category").innerHTML = '<option value=""></option>' + htmls.join('');
        })
        .catch(error => {
            console.error("Error loading categories:", error);
        });
}

// Xử lý form thêm sách
function handleCreateForm() {
    const submit = document.querySelector('input[type="submit"]');
    submit.onclick = function() {
        const name = document.querySelector('input[name="name"]').value;
        const pageCount = document.querySelector('input[name="page-count"]').value;
        const authorId = document.querySelector('select[name="author"]').value;
        const categoryId = document.querySelector('select[name="category"]').value;

        if (name && pageCount && authorId && categoryId) {
            const data = {
                name: name,
                page_count: pageCount,
                author_id: parseInt(authorId),
                category_id: parseInt(categoryId)
            };
            console.log(data);
            createBook(data, loadBook);
        } else {
            alert("Invalid value");
        }
    };
}

// Hàm tạo sách mới
function createBook(data, callback) {
    const options = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    };
    fetch(addBookApi, options)
        .then(response => response.json())
        .then(callback)
        .catch(error => {
            console.error("Error creating book:", error);
        });
}
