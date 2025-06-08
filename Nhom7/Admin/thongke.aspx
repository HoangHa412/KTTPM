<%@ Page Title="" Language="C#" MasterPageFile="~/Admin/Admin.Master" AutoEventWireup="true" CodeBehind="thongke.aspx.cs" Inherits="Nhom7.Admin.thongke" %>

<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
    body {
        font-family: Arial, sans-serif;
        margin: 20px;
        background-color: #f9f9f9;
    }

    h2 {
        text-align: center;
        color: #333;
    }

    form {
        max-width: 800px;
        margin: 0 auto;
        background: #fff;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }

    .gridview {
        margin: 20px 0;
        border-collapse: collapse;
        width: 100%;
    }

    .gridview th, .gridview td {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: center;
    }

    .gridview th {
        background-color: #007BFF;
        color: white;
        font-weight: bold;
    }

    .gridview tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    .gridview tr:hover {
        background-color: #eaf1f8;
    }

    .button-container {
        text-align: center;
        margin-top: 20px;
    }

    .button-container a,
    .button-container input {
        text-decoration: none;
        color: white;
        background-color: #007BFF;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }

    .button-container a:hover,
    .button-container input:hover {
        background-color: #0056b3;
    }
</style>
    <div>
     <h2>Thống kê doanh thu theo ngày</h2>
     <asp:GridView ID="gvThongKe" runat="server" AutoGenerateColumns="False" CssClass="gridview">
         <Columns>
             <asp:BoundField DataField="Ngay" HeaderText="Ngày" DataFormatString="{0:dd/MM/yyyy}" />
             <asp:BoundField DataField="TongTienBanDuoc" HeaderText="Tổng tiền bán được" DataFormatString="{0:#,##0 VNĐ}"/>
         </Columns>
     </asp:GridView>
     <div>&nbsp;</div>
     <div class="button-container">
         <asp:Button ID="btnDonHang" Text="Danh sách đơn hàng" PostBackUrl="/Admin/DanhSach.aspx" runat="server" />
     </div>

 </div>
</asp:Content>
