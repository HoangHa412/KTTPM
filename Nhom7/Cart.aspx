<%@ Page Title="" Language="C#" MasterPageFile="~/SitePage.Master" AutoEventWireup="true" CodeBehind="Cart.aspx.cs" Inherits="Nhom7.Cart" %>

<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" />

    <style>
        .cart-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #ddd;
            padding: 10px 0;
        }

        .cart-item img {
            width: 180px;
            height: auto;
        }

        .cart-item .item-info {
            flex: 1;
            margin-left: 10px;
        }

        .cart-item .item-info h4 {
            margin: 0;
            font-size: 16px;
        }

        .cart-item .item-info p {
            margin: 5px 0 0;
            font-size: 14px;
            color: #555;
        }

        .total-row {
            text-align: right;
            font-weight: bold;
            margin-top: 20px;
        }

        .cart-actions {
            display: flex;
            gap: 10px;
        }
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
    <div class="container mt-4">
        <h2 class="text-center mb-4">Giỏ Hàng</h2>

        <!-- Repeater hiển thị các mặt hàng trong giỏ hàng -->
        <asp:Repeater ID="rptCart" runat="server">
            <ItemTemplate>
                <div class="row cart-item border-bottom py-3">
                    <div class="col-md-2">
                        <!-- <img src='<%# ResolveUrl("~/image/" + Eval("Anh")) %>' alt="Book Image" class="img-fluid" /> -->
                        <img src='<%# Eval("Anh") %>' alt="Book Image" />
                    </div>
                    <div class="col-md-6">
                        <h5><%# Eval("TenSach") %></h5>
                        <p>Giá: <strong><%# Eval("Gia", "{0}") %> VND</strong></p>
                        <p>
                            Số lượng: 
                            <asp:TextBox ID="txtQuantity" runat="server" Text='<%# Eval("SoLuong") %>' CssClass="form-control w-25" />
                        </p>
                        <p>
                            Tổng: <strong><%# ((decimal)Eval("Gia") * (int)Eval("SoLuong")).ToString() %> VND</strong>
                        </p>
                    </div>
                    <div class="col-md-4 d-flex align-items-center justify-content-end">
                        <asp:Button ID="btnUpdate" runat="server" Text="Cập nhật" CommandName="Update" CommandArgument='<%# Eval("ID_Sach") %>' OnClick="btnUpdate_Click" CssClass="btn btn-warning me-2" />
                        <asp:Button ID="btnDelete" runat="server" Text="Xóa" CommandName="Delete" CommandArgument='<%# Eval("ID_Sach") %>' OnClick="btnDelete_Click" CssClass="btn btn-danger" OnClientClick="return confirm('Bạn có chắc chắn muốn xóa không?');"/>
                    </div>
                </div>
            </ItemTemplate>
        </asp:Repeater>

        <!-- Tổng tiền -->
        <div class="total-row text-end mt-4">
            <h4><strong>Tổng cộng: </strong><asp:Label ID="lblTotal" runat="server" CssClass="text-success"></asp:Label></h4>
        </div>

        <!-- Thanh toán -->
        <div class="text-center mt-4 mb-4">
            <asp:Button ID="btnCheckout" runat="server" Text="Thanh Toán" OnClick="btnCheckout_Click" CssClass="btn btn-primary" />
        </div>
    </div>

    <!-- Thêm Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</asp:Content>
