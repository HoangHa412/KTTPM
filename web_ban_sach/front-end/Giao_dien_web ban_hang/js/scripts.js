// Khai báo các API
const getBookApi = "http://127.0.0.1:5000/book-management/books";
const getBookByIdApi = (id) => `http://127.0.0.1:5000/book-management/book/${id}`;
const addBookApi = "http://127.0.0.1:5000/book-management/book";
const getAuthorApi = "http://127.0.0.1:5000/author-management/authors";
const getCategoryApi = "http://127.0.0.1:5000/category-management/categories";
const getCartApi = "http://127.0.0.1:5000/cart_all";
const addCartApi = "http://127.0.0.1:5000/add_cart";
const removeCartApi = (cartItemId) => `http://127.0.0.1:5000/remove_cart/${cartItemId}`;
const updateCartApi = (cartItemId) => `http://127.0.0.1:5000/update_cart_item/${cartItemId}`; // API cập nhật giỏ hàng

// Biến lưu trữ giỏ hàng
let cart = [];

// Hàm bắt đầu chương trình
function start() {
    dia_chi_giao_hang();
    loadBooks();//Gọi ra các thông tin của book từ api
    add_hoadon();
    handleOrderModal();
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

    let totalAmount = 0; // Biến để tính tổng số tiền

    // Hiển thị từng sách trong giỏ hàng
    cartItems.forEach(item => {
        const totalPrice = item.price * item.quantity; // Thành tiền của mỗi sách
        totalAmount += totalPrice; // Cộng vào tổng số tiền

        // Kiểm tra xem item.image_data có phải là chuỗi base64 hợp lệ không
        const isBase64 = item.image_data && item.image_data.startsWith('data:image/');

        // Nếu image_data không có tiền tố 'data:image/', thêm tiền tố này
        const imageSrc = isBase64 ? item.image_data : `data:image/png;base64,${item.image_data}`;

        const row = `
            <tr>
                <td style="text-align: center;"> <!-- Căn giữa hình ảnh -->
                    <img src="${imageSrc}" alt="${item.name}" style="width: 60px; height: auto;"/> <!-- Hiển thị hình ảnh -->
                </td>
                <td>${item.book_id}</td>
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>${item.price} VNĐ</td>
                <td>${totalPrice} VNĐ</td>
                <td>
                    <button style="border: none; background: none; color: blue; cursor: pointer;" onclick="removeFromCart(${item.id})">Delete</button>
                    <button style="border: none; background: none; color: blue; cursor: pointer;" onclick="showUpdateQuantityModal(${item.id}, ${item.quantity})">Sửa số lượng</button>
                </td>
            </tr>
        `;
        cartTableBody.insertAdjacentHTML("beforeend", row); // Thêm dòng vào bảng
    });

    // Hiển thị tổng số tiền vào dòng mới dưới cùng
    const totalRow = `
        <tr>
            <td colspan="5" style="text-align: right;">Tổng giá trị giỏ hàng:</td>
            <td>${totalAmount} VNĐ</td>
            <td></td>
        </tr>
    `;
    cartTableBody.insertAdjacentHTML("beforeend", totalRow);

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
async function getBookById(id_sach, id_html_name, id_salary, id_html_page_count, id_add_to_cart_button, id_author_name, img_id) {
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
            addToCartButton.onclick = () => addToCart(book);
        }

        // Lấy ảnh sách
        const imageResponse = await fetch(`http://localhost:5000/images/${id_sach}`);
        if (imageResponse.ok) {
            const imageData = await imageResponse.json();
            // console.log(imageData); // Debug để xem dữ liệu trả về

            // Kiểm tra nếu có ảnh trả về
            if (imageData.images && imageData.images.length > 0) {
                const base64Image = imageData.images[0]; // Lấy ảnh đầu tiên từ danh sách
                const imgElement = document.getElementById(img_id);
                if (imgElement) {
                    imgElement.src = `data:image/jpeg;base64,${base64Image}`; // Hiển thị ảnh
                }
            } else {
                console.error('No images found for this book.');
            }
        } else {
            console.warn(`Failed to fetch images for book with ID ${id_sach}`);
        }

    } catch (error) {
        console.error('Error fetching book:', error);
    }
}


// Hàm thêm sách vào giỏ hàng với số lượng
async function addToCart(book) {
    const userId = 1; // Thay đổi thành ID người dùng thực tế
    const newBook = {
        user_id: userId,
        book_id: book.id,
        quantity: 1 // Giả định là thêm 1 cuốn sách
    };

    // Gọi API để thêm sách vào giỏ hàng
    const result = await addToCartApi(newBook);

    if (result) {
        alert("Bạn đã thêm thành công cuốn sách vào giỏ hàng");
        loadCart(); // Tải lại giỏ hàng
    }
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
        return result;
    } catch (error) {
        console.error('Error sending to addCartApi:', error);
        return null; // Trả về null nếu có lỗi
    }
}

// Hàm xóa sản phẩm khỏi giỏ hàng
async function removeFromCart(cartItemId) {
    try {
        const response = await fetch(removeCartApi(cartItemId), {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Error removing item from cart');
        }

        await loadCart(); // Tải lại giỏ hàng
        alert("Bạn đã xóa thành công cuốn sách khỏi giỏ hàng");
    } catch (error) {
        console.error('Error removing item from cart:', error);
    }
}

// Hàm hiển thị modal cập nhật số lượng
function showUpdateQuantityModal(cartItemId, currentQuantity) {
    console.log("showUpdateQuantityModal called with:", cartItemId, currentQuantity); // Kiểm tra đầu vào
    const modal = document.getElementById("update-quantity-modal");
    const quantityInput = document.getElementById("update-quantity-input");
    quantityInput.value = currentQuantity; // Đặt giá trị hiện tại vào ô nhập

    // Thêm sự kiện cho nút xác nhận
    document.getElementById("confirm-update-button").onclick = async () => {
        const newQuantity = parseInt(quantityInput.value);
        if (newQuantity > 0) {
            await updateCartItem(cartItemId, newQuantity);
            modal.style.display = "none"; // Ẩn modal sau khi cập nhật
        } else {
            alert("Số lượng phải lớn hơn 0!");
        }
    };

    modal.style.display = "block"; // Hiển thị modal
}

// Hàm cập nhật số lượng
async function updateCartItem(cartItemId, newQuantity) {
    const updatedItem = { quantity: newQuantity }; // Chỉ cần truyền số lượng mới

    try {
        const response = await fetch(updateCartApi(cartItemId), {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedItem)
        });

        if (!response.ok) {
            throw new Error('Error updating quantity');
        }

        await loadCart(); // Tải lại giỏ hàng
        alert("Số lượng đã được cập nhật thành công!");
    } catch (error) {
        console.error('Error updating quantity:', error);
    }
}

// Hàm tải danh sách sách
function loadBook() {
    const titleTable = "<tr><th>Id</th><th>Name</th><th>Page Count</th><th>Author</th></tr>";
    fetch(getBookApi)
        .then(response => response.json())
        .then(books => {
            const htmls = books.map(book => `
                <tr>
                    <td>${book.id}</td>
                    <td>${book.name}</td>
                    <td>${book.page_count}</td>
                    <td>${book.author_name}</td>
                </tr>
            `);
            document.querySelector('#book-table tbody').innerHTML = titleTable + htmls.join('');
        })
        .catch(err => console.log(err));
}

// Hàm tải danh sách tác giả
async function loadAuthor() {
    try {
        const response = await fetch(getAuthorApi);
        const authors = await response.json();
        const authorSelect = document.getElementById("author-select");

        authors.forEach(author => {
            const option = document.createElement("option");
            option.value = author.id;
            option.textContent = author.name;
            authorSelect.appendChild(option);
        });

    } catch (error) {
        console.error('Error fetching authors:', error);
    }
}

// Hàm tải danh sách thể loại
async function loadCategory() {
    try {
        const response = await fetch(getCategoryApi);
        const categories = await response.json();
        const categorySelect = document.getElementById("category-select");

        categories.forEach(category => {
            const option = document.createElement("option");
            option.value = category.id;
            option.textContent = category.name;
            categorySelect.appendChild(option);
        });

    } catch (error) {
        console.error('Error fetching categories:', error);
    }
}

// Hàm click nút để hiển thị ra form thanh toán
function handleCreateForm() {
    const createBookForm = document.getElementById("create-book-form");
    createBookForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Ngăn chặn hành vi mặc định của form
        const bookData = {
            name: document.getElementById("book-name").value,
            author_id: document.getElementById("author-select").value,
            category_id: document.getElementById("category-select").value,
            page_count: document.getElementById("page-count").value
        };

        const response = await fetch(addBookApi, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookData)
        });

        if (response.ok) {
            alert("Sách đã được tạo thành công!");
            loadBook(); // Tải lại danh sách sách
        } else {
            alert("Có lỗi xảy ra khi tạo sách.");
        }
    });
}
// Hàm xử lý hiển thị modal đặt hàng
function handleOrderModal() {
    document.getElementById('dat_hang').addEventListener('click', function () {
        // Ẩn modal giỏ hàng (nếu đang mở)
        const cartModal = document.getElementById('cartModal');
        if (cartModal) {
            const bootstrapModal = bootstrap.Modal.getInstance(cartModal);
            bootstrapModal.hide();
        }

        // Hiển thị modal đặt hàng
        const orderModal = new bootstrap.Modal(document.getElementById('orderModal'));
        orderModal.show();
    });
}

//Hàm thêm hóa đơn và gửi lên api
async function add_hoadon() {
    // Khởi tạo các biến
    const codCheckbox = document.getElementById("cod1");
    const momoButton = document.getElementById("momo_payment");
    const vnpayButton = document.getElementById("vnpay_payment");
    const confirmOrderButton = document.getElementById("xac_nhan_dat_hang");
    const totalAmountElement = document.getElementById("total-amount");
    const addressInput = document.getElementById("address");
    const voucherInput = document.getElementById("voucher-code");
    const provinceSelect = document.getElementById("province");
    const districtSelect = document.getElementById("district");
    const wardSelect = document.getElementById("ward");
    const orderButton = document.getElementById("dat_hang"); // Nút Đặt hàng
    const orderModal = new bootstrap.Modal(document.getElementById("orderModal")); // Modal Đặt hàng

    let paymentMethod = "cod"; // Giá trị mặc định là COD

    // Xử lý chọn phương thức thanh toán
    momoButton.addEventListener("click", function () {
        paymentMethod = "momo";
        codCheckbox.checked = false;
        codCheckbox.disabled = true;
        momoButton.classList.add("btn-success");
        vnpayButton.classList.remove("btn-danger");
    });

    vnpayButton.addEventListener("click", function () {
        paymentMethod = "vnpay";
        codCheckbox.checked = false;
        codCheckbox.disabled = true;
        vnpayButton.classList.add("btn-danger");
        momoButton.classList.remove("btn-success");
    });

    codCheckbox.addEventListener("change", function () {
        if (codCheckbox.checked) {
            paymentMethod = "cod";
            codCheckbox.disabled = false;
            momoButton.classList.remove("btn-success");
            vnpayButton.classList.remove("btn-danger");
        }
    });

    // Khi click nút "Đặt hàng", tính tổng tiền và mở modal
    orderButton.addEventListener("click", async function () {
        await calculateTotalAmount(); // Tính tổng tiền ngay khi nhấn Đặt hàng
        orderModal.show(); // Mở modal
    });

    // Xử lý gửi đơn hàng khi click vào nút xác nhận
    confirmOrderButton.addEventListener("click", async function () {
        // Lấy dữ liệu từ form
        const detail_address = addressInput.value;
        const province = provinceSelect.value;
        const district = districtSelect.value;
        const ward = wardSelect.value;
        const totalAmount = totalAmountElement.textContent.replace(" VNĐ", "");
        const voucher = voucherInput.value;

        // Kiểm tra tính hợp lệ
        if (!detail_address || !province || !district || !ward) {
            alert("Vui lòng điền đầy đủ thông tin địa chỉ!");
            return;
        }

        if (!paymentMethod) {
            alert("Vui lòng chọn phương thức thanh toán!");
            return;
        }

        // Tạo đối tượng địa chỉ
        const fullAddress = {
            Tỉnh: province,
            Huyện: district,
            Xã: ward,
            Chi_tiet: detail_address
        };

        // Tạo đối tượng dữ liệu để gửi lên API
        const orderData = {
            address: fullAddress,
            user_id: 1,
            makhuyenmai: voucher || null,
            payment_method: paymentMethod,
        };

        try {
            // Gửi dữ liệu qua API đồng thời thêm hóa đơn và xóa giỏ hàng
            const [addHoaDonResponse, removeCartResponse] = await Promise.all([ 
                fetch("http://127.0.0.1:5000/add_hoa_don", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(orderData),
                }),
                fetch("http://127.0.0.1:5000/remove_all_cart/1", { method: "DELETE" }) // Xóa giỏ hàng của user_id = 1
            ]);

            if (!addHoaDonResponse.ok) {
                throw new Error("Có lỗi xảy ra khi gửi đơn hàng!");
            }

            const addHoaDonData = await addHoaDonResponse.json();
            if (addHoaDonData.message === "Hóa đơn đã được thêm thành công!") {
                alert(`Đơn hàng của bạn đã được gửi thành công! ID hóa đơn: ${addHoaDonData.id_hoaDon}`);

                // Kiểm tra nếu xóa giỏ hàng thành công
                if (removeCartResponse.ok) {
                    console.log("Giỏ hàng đã được xóa thành công.");
                } else {
                    console.error("Lỗi khi xóa giỏ hàng.");
                }

                // Đóng modal và reset form
                orderModal.hide();
                document.getElementById("order-form").reset();
            } else {
                alert(`Lỗi: ${addHoaDonData.message}`);
            }
        } catch (error) {
            console.error("Lỗi:", error);
            alert("Không thể gửi đơn hàng hoặc xóa giỏ hàng. Vui lòng thử lại sau.");
        }
    });
}

// Hàm tính tổng tiền
async function calculateTotalAmount() {
    try {
        const response = await fetch("http://127.0.0.1:5000/cart/1"); // Giả sử API này trả về giỏ hàng của user_id = 1
        const cartItems = await response.json();

        if (cartItems && cartItems.length > 0) {
            let totalAmount = 0;
            cartItems.forEach(item => {
                totalAmount += item.price * item.quantity; // Tính tổng tiền: giá * số lượng
            });

            // Cập nhật tổng tiền trong giao diện
            document.getElementById("total-amount").textContent = `${totalAmount.toLocaleString()} VNĐ`;
        } else {
            document.getElementById("total-amount").textContent = "0 VNĐ"; // Nếu giỏ hàng rỗng
        }
    } catch (error) {
        console.error("Lỗi khi tính tổng tiền:", error);
        document.getElementById("total-amount").textContent = "0 VNĐ"; // Đặt lại tổng tiền nếu có lỗi
    }
    
}

// Gọi hàm khi DOM đã sẵn sàng
// document.addEventListener("DOMContentLoaded", processOrder);

//Hàm load thông tin các books
function loadBooks() {
    // Lặp qua các sách từ 1 đến 12
    for (let i = 1; i <= 20; i++) {
        let name = `name_${i}`;
        let salary = `salary_${i}`;
        let page_count = `page_count_${i}`;
        let btn = `btn_${i}`;
        let author_name = `author_name_${i}`;
        let img = `img_${i}`;

        // Gọi hàm với các tham số động
        getBookById(i, name, salary, page_count, btn, author_name, img);

        // Gắn sự kiện onclick cho các phần tử với id là "onclick_i"
        const onclickElement = document.getElementById(`onclick_${i}`);
        if (onclickElement) {
            onclickElement.onclick = function () {
                goToDetailPage(i);  // Chuyển hướng đến trang chi tiết với bookId = i
            };
        }
    }

    // Thêm 1 sách đặc biệt (00)
    getBookById(1, 'name_00', 'salary_00', 'page_count_00', 'btn_00', 'author_name_00', 'img_00');

    // Gọi hàm loadCart nếu cần
    loadCart();
}

// Gọi hàm khi trang được tải xong
window.onload = function () {
    loadBooks();
};

function dia_chi_giao_hang() {
    // API URL
    const provinceAPI = "https://open.oapi.vn/location/provinces?page=0&size=30&query=";
    const districtAPI = "https://open.oapi.vn/location/districts/";
    const wardAPI = "https://open.oapi.vn/location/wards/";

    // Get DOM elements
    const provinceSelect = document.getElementById("province");
    const districtSelect = document.getElementById("district");
    const wardSelect = document.getElementById("ward");

    // Fetch provinces and populate the province select dropdown
    function fetchProvinces(query = "") {
        fetch(provinceAPI + query)
            .then(response => response.json())
            .then(data => {
                const provinces = data.data;
                provinceSelect.innerHTML = `<option value="" disabled selected>Chọn tỉnh/thành phố</option>`; // Reset options
                provinces.forEach(province => {
                    const option = document.createElement("option");
                    option.value = province.id;
                    option.textContent = province.name;
                    provinceSelect.appendChild(option);
                });
            });
    }

    // Fetch districts based on selected province and populate district select dropdown
    function fetchDistricts(provinceId, query = "") {
        fetch(districtAPI + provinceId + "?page=0&size=30&query=" + query)
            .then(response => response.json())
            .then(data => {
                const districts = data.data;
                districtSelect.innerHTML = `<option value="" disabled selected>Chọn quận/huyện</option>`; // Reset options
                districts.forEach(district => {
                    const option = document.createElement("option");
                    option.value = district.id;
                    option.textContent = district.name;
                    districtSelect.appendChild(option);
                });
            });
    }

    // Fetch wards based on selected district and populate ward select dropdown
    function fetchWards(districtId, query = "") {
        fetch(wardAPI + districtId + "?page=0&size=30&query=" + query)
            .then(response => response.json())
            .then(data => {
                const wards = data.data;
                wardSelect.innerHTML = `<option value="" disabled selected>Chọn phường/xã</option>`; // Reset options
                wards.forEach(ward => {
                    const option = document.createElement("option");
                    option.value = ward.id;
                    option.textContent = ward.name;
                    wardSelect.appendChild(option);
                });
            });
    }

    // Event listeners for province and district selects
    provinceSelect.addEventListener("change", function() {
        const selectedProvinceId = provinceSelect.value;
        fetchDistricts(selectedProvinceId);  // Fetch districts when province is selected
    });

    districtSelect.addEventListener("change", function() {
        const selectedDistrictId = districtSelect.value;
        fetchWards(selectedDistrictId);  // Fetch wards when district is selected
    });

    // Initial load of provinces
    fetchProvinces();
}

// Gọi hàm dia_chi_giao_hang khi DOM được tải xong
// document.addEventListener("DOMContentLoaded", dia_chi_giao_hang);