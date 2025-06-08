<%@ Page Title="Chi Tiết Sản Phẩm" Language="C#" MasterPageFile="~/SitePage.Master" AutoEventWireup="true" CodeBehind="ProductDetail.aspx.cs" Inherits="Nhom7.ProductDetail" %>

<asp:Content ID="TitleContent2" ContentPlaceHolderID="TitleContent" runat="server">
    Chi Tiết Sản Phẩm
</asp:Content>

<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
        .product-detail-container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            margin: 40px auto;
            gap: 40px;
            background: #f9f9f9;
            padding: 30px;
            padding-left: 70px;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
            max-width: 1200px;
        }
        .product-image {
            flex: 1;
            max-width: 40%;
            text-align: center;
        }
        .product-image img {
            width: 100%;
            max-width: 300px;
            height: 400px;
            object-fit: cover;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .product-info {
            flex: 2;
            max-width: 60%;
        }
        .product-info h1 {
            font-size: 28px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            border-bottom: 2px solid #1E90FF;
            padding-bottom: 10px;
        }
        .product-info p {
            font-size: 16px;
            line-height: 1.8;
            color: #555;
            margin-bottom: 15px;
        }
        .product-info .price {
            font-size: 20px;
            font-weight: bold;
            color: #FF4500;
            margin-top: 20px;
            margin-bottom: 30px;
        }
        .btn-add-to-cart {
            display: inline-block;
            padding: 12px 25px;
            background-color: #1E90FF;
            color: white;
            text-transform: uppercase;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .btn-add-to-cart:hover {
            background-color: #155b9a;
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2);
            transform: translateY(-2px);
        }
        @media screen and (max-width: 768px) {
            .product-detail-container {
                flex-direction: column;
                padding: 20px;
            }

            .product-image {
                max-width: 100%;
                margin-bottom: 20px;
            }

            .product-info {
                max-width: 100%;
            }

            .product-info h1 {
                font-size: 24px;
            }

            .product-info p {
                font-size: 14px;
            }

            .product-info .price {
                font-size: 18px;
            }

            .btn-add-to-cart {
                font-size: 14px;
            }
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

    <div class="product-detail-container">
        <asp:Repeater ID="RepeaterBook" runat="server">
            <ItemTemplate>
                <!-- Ảnh sản phẩm -->
                <div class="product-image">

                    <img src='<%# Eval("Anh") %>' alt="Book Image" />
                     <!-- uyenkaka -->
                     <%--<img src='<%# ResolveUrl("~/image/" + Eval("Anh")) %>' alt="Book Image" />--%>
                </div>

                <!-- Thông tin sản phẩm -->
                <div class="product-info">
                    <h1><%# Eval("TenSach") %></h1>
                    <p><strong>Mô tả:</strong> <%# Eval("MoTa") %></p>
              
                    <p><strong>Tác giả:</strong> <%# Eval("TenTacGia") %></p>
                    <p><strong>Danh mục:</strong> <%# Eval("TenDanhMuc") %></p>
                    <p><strong>Số lượng tồn:</strong> <%# Eval("SoLuongTon") %></p>
                    <p><strong>Ngày xuất bản:</strong> <%# Eval("NgayXuatBan", "{0:dd/MM/yyyy}") %></p>
                    <p class="price"><strong>Giá:</strong> <%# Eval("Gia", "{0:N0}") %> VND</p>

                    <!-- Nút thêm vào giỏ hàng -->
       

                    <asp:Button ID="btnAddToCart" runat="server" Text="Thêm vào giỏ hàng" CssClass="btn-add-to-cart" OnClick="btnAddToCart_Click"  CommandArgument='<%# Eval("ID_Sach") %>' />
                </div>
            </ItemTemplate>
        </asp:Repeater>
    </div>
</asp:Content>
