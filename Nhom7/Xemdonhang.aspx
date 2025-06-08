<%@ Page Title="" Language="C#" MasterPageFile="~/SitePage.Master" AutoEventWireup="true" CodeBehind="Xemdonhang.aspx.cs" Inherits="Nhom7.Xemdonhang" %>
<asp:Content ID="Content1" ContentPlaceHolderID="TitleContent" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
        }

        .container {
            width: 80%;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }

        h2 {
            text-align: center;
            color: #333;
            font-size: 28px;
            margin-bottom: 20px;
        }

        h4 {
            font-size: 20px;
            color: #444;
            margin-bottom: 10px;
        }

        .order-header {
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f2f2f2;
            margin-top: 10px;
        }

        .order-header p {
            font-size: 16px;
            color: #555;
            margin: 5px 0;
        }

        .order-header strong {
            color: #333;
        }

        .order-details {
            margin-top: 20px;
        }

        .order-details h4 {
            font-size: 22px;
            color: #333;
            margin-bottom: 15px;
        }

        .gridview-container {
            margin-top: 20px;
            overflow-x: auto;
        }

        .gridview-container table {
            width: 100%;
            border-collapse: collapse;
        }

        .gridview-container th, .gridview-container td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
            font-size: 16px;
        }

        .gridview-container th {
            background-color: #f4f4f4;
            color: #333;
        }

        .gridview-container tr:hover {
            background-color: #f9f9f9;
        }

        .gridview-container td {
            color: #555;
        }

        .alert-message {
            color: red;
            font-weight: bold;
        }
    </style>

    <div class="container">
        <h2>Thông tin đơn hàng</h2>

        <asp:Label ID="lblMessage" runat="server" ForeColor="Red" Visible="false" CssClass="alert-message"></asp:Label>

        <div class="order-header">
            <h4>Thông tin chung:</h4>
            <p><strong>Mã đơn hàng:</strong> <asp:Label ID="lblOrderID" runat="server"></asp:Label></p>
            <p><strong>Ngày tạo:</strong> <asp:Label ID="lblNgayTao" runat="server"></asp:Label></p>
            <p><strong>Tổng tiền:</strong> <asp:Label ID="lblTongTien" runat="server"></asp:Label></p>
            <p><strong>Trạng thái:</strong> <asp:Label ID="lblTrangThai" runat="server"></asp:Label></p>
        </div>

        <div class="order-details">
            <h4>Chi tiết đơn hàng:</h4>

            <div class="gridview-container">
                <asp:GridView ID="gvOrderDetails" runat="server" AutoGenerateColumns="False" CssClass="gridview" BorderStyle="None">
                    <Columns>
                        <asp:BoundField DataField="ID_Sach" HeaderText="Mã sách" SortExpression="ID_Sach" />
                        <asp:BoundField DataField="TenSach" HeaderText="Tên sách" SortExpression="TenSach" />
                        <asp:BoundField DataField="SoLuong" HeaderText="Số lượng" SortExpression="SoLuong" />
                        <asp:BoundField DataField="GiaBan" HeaderText="Giá bán" DataFormatString="{0:C}" SortExpression="GiaBan" />
                        <asp:BoundField DataField="ThanhTien" HeaderText="Thành tiền" DataFormatString="{0:C}" SortExpression="ThanhTien" />
                    </Columns>
                </asp:GridView>
            </div>
        </div>
    </div>
</asp:Content>
