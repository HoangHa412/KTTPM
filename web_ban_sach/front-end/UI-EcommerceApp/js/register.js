document.querySelector("form").addEventListener("submit", async function (event) {
  event.preventDefault(); // Ngăn chặn hành động submit mặc định

  // Lấy giá trị từ các trường nhập liệu trên form
  const name = document.querySelector("input[placeholder='name']").value;
  const address = document.querySelector("input[placeholder='address']").value;
  const phone_numbers = document.querySelector("input[placeholder='phone_numbers']").value;
  const account_user = document.querySelector("input[placeholder='account_user']").value;
  const password_user = document.querySelector("input[placeholder='password_user']").value;
  const confirm_password = document.querySelector("input[placeholder='confirm_password']").value;

  // Kiểm tra nếu các trường trống
  if (!name || !address || !phone_numbers || !account_user || !password_user || !confirm_password) {
    alert("All fields are required.");
    return;
  }

  // Kiểm tra mật khẩu và mật khẩu xác nhận
  if (password_user !== confirm_password) {
    alert("Password and Confirm Password do not match.");
    return;
  }

  // Dữ liệu cần gửi đến API
  const data = {
    name,
    address,
    phone_numbers,
    account_user,
    password_user,
  };

  try {
    // Gửi yêu cầu POST đến API
    const response = await fetch("http://127.0.0.1:5000/add_user_account", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    // Xử lý phản hồi từ server
    const result = await response.json();
    console.log(result); // Xem kết quả trả về từ server để kiểm tra thêm

    if (response.ok) {
      // alert("Account created successfully!");
      // Chuyển hướng đến trang đăng nhập
      window.location.href =
        "http://127.0.0.1:5501/web_ban_sach/front-end/UI-EcommerceApp/login.html"; // Đảm bảo đường dẫn đúng
    } else {
      alert(result.message || "Error creating account.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again later.");
  }
});
