<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Signup.aspx.cs" Inherits="Nhom7.Signup" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Đăng ký tài khoản</title>
    <!-- Bootstrap CDN -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet" />
    <link href="css/signupcss.css" rel="stylesheet" />
</head>

<style>
    body {
        background-image: url('<%= ResolveUrl("~/image/14.jpg") %>');
        background-size: cover;
        background-position: center;
        height: 100vh;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .container {
        background-color: rgba(255, 255, 255, 0.9); /* Nền bán trong suốt */
        padding: 60px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        min-width: 400px;
        width: 100%;
        animation: fadeIn 0.5s ease-in-out;
    }

    .container h2 {
        text-align: center;
        margin-bottom: 20px;
        color: #333;
    }

    .container label {
        font-weight: bold;
        font-size: 14px;
        color: #555;
    }

    .container .form-control {
        margin-bottom: 15px;
        width: 100%;
    }

    .container .btn {
        width: 100%;
        padding: 10px;
        font-size: 16px;
    }

    .container a {
        display: block;
        text-align: center;
        margin-top: 15px;
        text-decoration: none;
        font-size: 14px;
        color: #007bff;
    }

    .container a:hover {
        text-decoration: underline;
    }

    /* Thông báo lỗi và thành công */
    .error-message {
        display: none;
        padding: 10px;
        margin-top: 20px;
        border-radius: 5px;
        font-size: 14px;
    }

    .error-message.show {
        display: block;
        margin-top: 10px;
    }

    .error-message.error {
        background-color: #f44336;
        color: white;
        border: 1px solid #d32f2f;
    }

    .error-message.success {
        background-color: #4CAF50;
        color: white;
        border: 1px solid #388E3C;
    }

    .card-body{
        min-width: 350px;
    }
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    .su{
        min-width:400px;
    }

</style>

<body>
    <form id="form1" runat="server">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6 su">
                    <div class="card">
                        <div class="card-header text-center">
                            <h2>Đăng ký tài khoản</h2>
                        </div>
                        <div class="card-body">
                            <!-- Form đăng ký -->
                            <div class="form-group">
                                <label for="txtUsername">Username</label>
                                <asp:TextBox ID="txtUsername" runat="server" CssClass="form-control" />
                            </div>

                            <div class="form-group">
                                <label for="txtPassword">Password</label>
                                <asp:TextBox ID="txtPassword" runat="server" TextMode="Password" CssClass="form-control" />
                            </div>

                            <div class="form-group">
                                <label for="txtEmail">Email</label>
                                <asp:TextBox ID="txtEmail" runat="server" CssClass="form-control" />
                            </div>

                            <div class="form-group">
                                <label for="txtPhone">Phone Number</label>
                                <asp:TextBox ID="txtPhone" runat="server" CssClass="form-control" />
                            </div>

                            <div class="form-group">
                                <label for="txtAddress">Address</label>
                                <asp:TextBox ID="txtAddress" runat="server" CssClass="form-control" />
                            </div>

                            <div class="form-group">
                                <label for="ddlRole">Role</label>
                                <asp:DropDownList ID="ddlRole" runat="server" CssClass="form-control">
                                    <asp:ListItem Value="2" Text="Customer" />
                                </asp:DropDownList>
                            </div>

                            <div class="form-group">
                                <asp:Button ID="btnRegister" runat="server" Text="Đăng Ký" CssClass="btn btn-primary btn-block" OnClick="btnRegister_Click" />
                            </div>

                            <div class="text-center">
                                <a href="Login.aspx">Đã có tài khoản? Đăng nhập</a>
                            </div>
                        </div>
                    </div>

                    <!-- Thông báo lỗi hoặc thành công -->
                    <asp:Label ID="lblMessage" runat="server" CssClass="error-message" />
                </div>
            </div>
        </div>
    </form>

    <!-- Bootstrap JS và jQuery -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
