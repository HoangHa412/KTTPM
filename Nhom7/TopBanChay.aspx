<%@ Page Title="" Language="C#" MasterPageFile="~/SitePage.Master" AutoEventWireup="true" CodeBehind="TopBanChay.aspx.cs" Inherits="Nhom7.TopBanChay" %>
<asp:Content ID="Content1" ContentPlaceHolderID="TitleContent" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
        .products {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            margin: 20px 50px;
        }
        .product {
            width: 250px;
            height: 350px;
            margin: 20px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.1s, box-shadow 0.1s;
            padding: 20px;
            background-color: #fff;
            text-align: center;
        }
        .product img {
            object-fit: cover;
            border-radius: 3px;
        }
        .product p {
            margin: 10px 0;
            color: #333;
        }
        .product strong {
            font-size: 18px;
            color: #1E90FF;
        }
        .product:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }
        .product .price {
            color: #FF6347;
            font-weight: bold;
            font-size: 17px;
        }
        /* Phần thông tin "đã bán" */
        .sold-info {
            background-color: rgba(128, 128, 128, 0.6);
            color: white;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 14px;
            width: 70px;
            height: 20px;
            line-height: 20px;
            margin-left: -10px;
        }
        img {
            width: 100%;
            height: 65%;
            object-fit: cover;
            border-radius: 3px;
        }
    </style>
    <h3 style="padding-left: 20px; margin-bottom: 5px">Top sản phẩm bán chạy</h3>
    <hr style="border: none; height: 3px; background-color: #007bff; margin-left: 20px; width: 100%;"/>
    <div class="products">
        <asp:Repeater ID="RepeaterBooks" runat="server">
            <ItemTemplate>
                <a href="ProductDetail.aspx?ID_Sach=<%# Eval("ID_Sach") %>" style="text-decoration: none; color: inherit;">
                    <div class="product">
                        <!-- Thông tin đã bán -->
                        <div class="sold-info">
                            Đã bán: <%# Eval("TongSoLuongBan") %>
                        </div>
                         <!--<img src='<%# ResolveUrl("~/image/" + Eval("Anh")) %>' alt="Book Image" />-->
                        <img src='<%# Eval("Anh") %>' alt="Book Image" />
                        <p><strong><%# Eval("TenSach") %></strong></p>
                        <p class="price"><%# Eval("Gia", "{0:N0}") %> VND</p>
                    </div>
                </a>
            </ItemTemplate>
        </asp:Repeater>
    </div>
</asp:Content>
