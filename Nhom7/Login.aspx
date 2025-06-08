<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Login.aspx.cs" Inherits="Nhom7.Login" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Login</title>
    <!-- Thêm Bootstrap vào trang -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" />
    <style>
        body {
            background-image: url('<%= ResolveUrl("~/image/14.jpg") %>');
            background-fit: cover;
            background-position: center;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .login-container {
            background-color: rgba(255, 255, 255, 0.9); /* Màu nền bán trong suốt */
            padding: 60px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            min-width: 400px;
            width: 100%;
        }

        .login-container h2 {
            text-align: center;
            margin-bottom: 20px;
        }

        .login-container label {
            font-weight: bold;
            font-size: 14px;
        }

        .login-container .form-control {
            margin-bottom: 15px;
            width: 100%;

        }

        .login-container .btn {
            width: 100%;
            padding: 10px;
            font-size: 16px;
        }

        .login-container a {
            display: block;
            text-align: center;
            margin-top: 15px;
            text-decoration: none;
            font-size: 14px;
            color: #007bff;
        }

        .login-container a:hover {
            text-decoration: underline;
        }

                /* CSS cho các thông báo lỗi */
        .error-message {
            display: none; /* Ẩn mặc định thông báo */
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-size: 14px;
            color: white;
        }

        .error-message.error {
            background-color: #f44336; /* Màu đỏ cho thông báo lỗi */
            border: 1px solid #d32f2f;
        }

        .error-message.success {
            background-color: #4CAF50; /* Màu xanh cho thông báo thành công */
            border: 1px solid #388E3C;
        }

        .error-message.warning {
            background-color: #ff9800; /* Màu cam cho thông báo cảnh báo */
            border: 1px solid #f57c00;
        }

        .error-message.info {
            background-color: #2196F3; /* Màu xanh dương cho thông báo thông tin */
            border: 1px solid #1976D2;
        }

        /* Thêm hiệu ứng fade-in khi hiển thị thông báo */
        .error-message.show {
            display: block;
            animation: fadeIn 0.5s ease-in-out;
        }

        /* Hiệu ứng fade-in */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

    </style>
</head>
<body>
    <form id="form1" runat="server">
        <div class="login-container">
            <h2>Login</h2>
            
            <!-- Username Field -->
            <label for="txtUsername">Username:</label>
            <asp:TextBox ID="txtUsername" runat="server" CssClass="form-control" placeholder="Nhập tài khoản" />

            <!-- Password Field -->
            <label for="txtPassword">Password:</label>
            <asp:TextBox ID="txtPassword" runat="server" TextMode="Password" CssClass="form-control" placeholder="Nhập password" />

            <!-- Role Dropdown -->
            <label for="ddlRole">Role:</label>
            <asp:DropDownList ID="ddlRole" runat="server" CssClass="form-select">
                <asp:ListItem Value="1" Text="Admin" />
                <asp:ListItem Value="2" Text="Khách hàng" />
            </asp:DropDownList>

            <!-- Login Button -->
            <asp:Button ID="btnLogin" runat="server" Text="Login" OnClick="btnLogin_Click" CssClass="btn btn-primary" />

            <!-- Link to Signup -->
            <a href="Signup.aspx">Bạn chưa có tài khoản? Đăng ký</a>

            <!-- Error message label -->
            <asp:Label ID="lblMessage" runat="server" CssClass="error-message" />
            <asp:Label ID="lblDebugQuery" runat="server" CssClass="error-message" />
        </div>
    </form>

    <!-- Thêm Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
