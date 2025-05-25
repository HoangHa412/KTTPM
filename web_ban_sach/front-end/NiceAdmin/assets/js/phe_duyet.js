const apiBaseURL = "http://127.0.0.1:5000"; // Địa chỉ máy chủ

// Hàm gọi API để lấy tất cả hóa đơn
async function loadOrders() {
    try {
        const response = await fetch(`${apiBaseURL}/hoa_don`);
        const orders = await response.json();
        renderOrders(orders);
    } catch (error) {
        console.error("Lỗi khi tải hóa đơn:", error);
    }
}

// Hàm render dữ liệu lên bảng
function renderOrders(orders) {
    const tableBody = document.getElementById("order-body");
    tableBody.innerHTML = ""; // Xóa dữ liệu cũ

    orders.forEach(order => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.user_id}</td>
            <td>${renderOrderDetails(order.information)}</td>
            <td>${order.sum_price.toLocaleString()} VNĐ</td>
            <td>${order.tt_hoadon}</td>
            <td><button onclick="rejectOrder(${order.id})">Từ chối</button></td>
            <td><button onclick="approveOrder(${order.id})">Phê duyệt</button></td>
        `;
        tableBody.appendChild(row);
    });
}

// Hàm chuyển đổi thông tin đơn hàng JSON thành chuỗi dễ đọc
function renderOrderDetails(information) {
    try {
        const details = JSON.parse(information);
        return details.map(item => `${item.book_name} (SL: ${item.quantity})`).join(", ");
    } catch (error) {
        console.error("Lỗi khi chuyển đổi thông tin đơn hàng:", error);
        return "Không có thông tin";
    }
}

// Hàm phê duyệt tất cả hóa đơn
async function approveAll() {
    try {
        const response = await fetch(`${apiBaseURL}/phe_duyet_all_hoa_don`, {
            method: "PUT"
        });
        if (response.ok) {
            alert("Đã phê duyệt tất cả hóa đơn!");
            loadOrders(); // Tải lại danh sách
        }
    } catch (error) {
        console.error("Lỗi khi phê duyệt tất cả:", error);
    }
}

// Hàm phê duyệt đơn hàng cụ thể
async function approveOrder(orderId) {
    try {
        const response = await fetch(`${apiBaseURL}/phe_duyet_hoa_don/${orderId}`, {
            method: "PUT"
        });
        if (response.ok) {
            alert(`Đã phê duyệt đơn hàng ${orderId}`);
            loadOrders(); // Tải lại danh sách
        } else {
            console.error(`Lỗi: Phê duyệt đơn hàng ${orderId} thất bại.`);
        }
    } catch (error) {
        console.error(`Lỗi khi phê duyệt đơn hàng ${orderId}:`, error);
    }
}

// Hàm từ chối đơn hàng cụ thể
async function rejectOrder(orderId) {
    try {
        const response = await fetch(`${apiBaseURL}/tu_choi_hoa_don/${orderId}`, {
            method: "PUT"
        });
        if (response.ok) {
            alert(`Đã từ chối đơn hàng ${orderId}`);
            loadOrders(); // Tải lại danh sách
        } else {
            console.error(`Lỗi: Từ chối đơn hàng ${orderId} thất bại.`);
        }
    } catch (error) {
        console.error(`Lỗi khi từ chối đơn hàng ${orderId}:`, error);
    }
}

// Tải dữ liệu hóa đơn khi trang được load
window.onload = loadOrders;
