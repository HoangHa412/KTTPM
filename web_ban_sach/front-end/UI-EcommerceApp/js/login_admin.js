// Lắng nghe sự kiện khi người dùng nhấn nút "Login"
document.querySelector("form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Ngăn chặn form reload trang

    // Lấy dữ liệu từ form
    const name = document.querySelector('input[placeholder="Name"]').value;
    const password = document.querySelector('input[placeholder="Password"]').value;

    // Kiểm tra dữ liệu đầu vào
    if (!name || !password) {
        alert("Please enter both Name and Password.");
        return;
    }

    try {
        // Gửi yêu cầu GET tới API để kiểm tra thông tin tài khoản
        const response = await fetch(
            `http://127.0.0.1:5000/get_admin_credentials/${encodeURIComponent(name)}`
        );

        // Kiểm tra phản hồi từ API
        if (response.ok) {
            const data = await response.json();

            // Kiểm tra mật khẩu từ phản hồi của API
            if (data.password_admin === password) {
                alert("Welcome to the Admin Panel!");

                // Chuyển hướng đến giao diện admin
                window.location.href = "http://127.0.0.1:5501/web_ban_sach/front-end/NiceAdmin/index.html";
            } else {
                alert("Incorrect password. Please try again.");
            }
        } else {
            alert("Admin not found. Please check your credentials.");
        }
    } catch (error) {
        console.error("Error during login:", error);
        alert("An error occurred. Please try again later.");
    }
});
