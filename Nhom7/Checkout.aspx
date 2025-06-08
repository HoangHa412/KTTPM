<%@ Page Title="" Language="C#" MasterPageFile="~/SitePage.Master" AutoEventWireup="true" CodeBehind="Checkout.aspx.cs" Inherits="Nhom7.Checkout" %>
<asp:Content ID="Content1" ContentPlaceHolderID="TitleContent" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
    /* General styling */
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        background-color: #f4f4f4;
        padding: 20px;
    }

    .checkout-container {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin: 0 auto;
    }

    h2, h3 {
        color: #333;
        font-size: 22px;
        margin-bottom: 15px;
    }

    .total-price {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Table Styling */
    .info-table, .order-details-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }

    .info-table td, .order-details-table th, .order-details-table td {
        padding: 10px;
        text-align: left;
    }

    .info-table td {
        font-size: 16px;
    }

    .order-details-table th {
        background-color: #f1f1f1;
        text-align: center;
    }

    .order-details-table td {
        text-align: center;
    }

    .input-field {
        width: 100%;
        padding: 8px;
        margin-top: 5px;
        font-size: 14px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .btn-update, .btn-payment {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        text-align: center;
        display: inline-block;
    }

    .btn-update:hover, .btn-payment:hover {
        background-color: #45a049;
    }

    /* Payment Dropdown Styling */
    .dropdown {
        width: 100%;
        padding: 8px;
        margin-top: 5px;
        font-size: 14px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    /* Message Label Styling */
    .message {
        font-size: 14px;
        color: red;
        margin-top: 10px;
    }

    /* Responsive Design */
    @media screen and (max-width: 768px) {
        .checkout-container {
            padding: 20px;
        }

        h2, h3 {
            font-size: 20px;
        }

        .info-table td, .order-details-table th, .order-details-table td {
            font-size: 14px;
        }
    }
</style>
   <div class="checkout-container">
        <!-- Total Price Label -->
        <div class="total-price">
            <asp:Label ID="lblTotalPrice" runat="server" Text="Tổng tiền:"></asp:Label>
        </div>

        <!-- Payment Information Section -->
        <h2>Thông Tin Thanh Toán</h2>
        <asp:Label ID="lblMessage" runat="server" ForeColor="Red"></asp:Label>

        <h3>Cập Nhật Thông Tin Cá Nhân</h3>
        <div class="form-container">
            <table class="info-table">
                <tr>
                    <td>Tên Người Dùng:</td>
                    <td><asp:TextBox ID="txtTenNguoiDung" runat="server" class="input-field"></asp:TextBox></td>
                </tr>
                <tr>
                    <td>Email:</td>
                    <td><asp:TextBox ID="txtEmail" runat="server" class="input-field"></asp:TextBox></td>
                </tr>
                <tr>
                    <td>Số Điện Thoại:</td>
                    <td><asp:TextBox ID="txtSoDienThoai" runat="server" class="input-field"></asp:TextBox></td>
                </tr>
                <tr>
                    <td>Địa Chỉ:</td>
                    <td><asp:TextBox ID="txtDiaChi" runat="server" class="input-field"></asp:TextBox></td>
                </tr>
                <tr>
                    <td colspan="2" align="center">
                        <asp:Button ID="btnUpdate" runat="server" Text="Cập Nhật Thông Tin" OnClick="btnUpdate_Click" class="btn-update" />
                    </td>
                </tr>
            </table>
        </div>

        <!-- Order Details Section -->
        <h3>Thông Tin Đơn Hàng</h3>
        <asp:Repeater ID="RepeaterCartItems" runat="server">
            <HeaderTemplate>
                <table class="order-details-table">
                    <tr>
                        <th>Tên Sách</th>
                        <th>Giá</th>
                        <th>Số Lượng</th>
                        <th>Thành Tiền</th>
                    </tr>
            </HeaderTemplate>
            <ItemTemplate>
                <tr>
                    <td><%# Eval("TenSach") %></td>
                    <td><%# Eval("Gia", "{0}") %>VND</td>
                    <td><%# Eval("SoLuong") %></td>
                    <td><%# Eval("Tong", "{0}") %> VND</td>
                </tr>
            </ItemTemplate>
            <FooterTemplate>
                </table>
            </FooterTemplate>
        </asp:Repeater>

        <!-- Payment Method Dropdown -->
        <div class="payment-method">
            <label for="ddlPaymentMethod">Phương thức thanh toán:</label>
            <asp:DropDownList ID="ddlPaymentMethod" runat="server" class="dropdown">
                <asp:ListItem Text="Tiền mặt" Value="TienMat"></asp:ListItem>
                <asp:ListItem Text="Thẻ tín dụng" Value="TheTinDung"></asp:ListItem>
                <asp:ListItem Text="Ví điện tử" Value="ViDienTu"></asp:ListItem>
            </asp:DropDownList>
        </div>

        <!-- Payment Button -->
        <div class="payment-button-container">
            <asp:Button ID="btnThanhToan" runat="server" Text="Thanh Toán" OnClick="btnThanhToan_Click" class="btn-payment" />
        </div>
    </div>
</asp:Content>
