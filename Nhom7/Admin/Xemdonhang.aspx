<%@ Page Title="" Language="C#" MasterPageFile="~/Admin/Admin.Master" AutoEventWireup="true" CodeBehind="Xemdonhang.aspx.cs" Inherits="Nhom7.Admin.Xemdonhang" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
     .order-header {
         margin-bottom: 20px;
         border-bottom: 2px solid #ccc;
         padding-bottom: 10px;
         background: #fff;
     }
     .order-details {
         margin-top: 20px;
         background: #fff;
         
     }
 </style>

     <h2 style="color:#fff";>Thông tin đơn hàng</h2>

     <asp:Label ID="lblMessage" runat="server" ForeColor="Red" Visible="false"></asp:Label>
     <div class="order-header">
         <h4>Thông tin chung:</h4>
         <p><strong>Mã đơn hàng:</strong> <asp:Label ID="lblOrderID" runat="server"></asp:Label></p>
         <p><strong>Ngày tạo:</strong> <asp:Label ID="lblNgayTao" runat="server"></asp:Label></p>
         <p><strong>Tổng tiền:</strong> <asp:Label ID="lblTongTien" runat="server"></asp:Label></p>
         <p><strong>Trạng thái:</strong> <asp:Label ID="lblTrangThai" runat="server"></asp:Label></p>
     </div>

     <div class="order-details">
         <h4>Chi tiết đơn hàng:</h4>
         <asp:GridView ID="gvOrderDetails" runat="server" AutoGenerateColumns="False">
             <Columns>
                 <asp:BoundField DataField="ID_Sach" HeaderText="Mã sách" />
                 <asp:BoundField DataField="TenSach" HeaderText="Tên sách" />
                 <asp:BoundField DataField="SoLuong" HeaderText="Số lượng" />
                 <asp:BoundField DataField="GiaBan" HeaderText="Giá bán" DataFormatString="{0:C}" />
                 <asp:BoundField DataField="ThanhTien" HeaderText="Thành tiền" DataFormatString="{0:C}" />
             </Columns>
         </asp:GridView>
     </div>
</asp:Content>

