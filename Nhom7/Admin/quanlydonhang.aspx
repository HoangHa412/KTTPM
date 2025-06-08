<%@ Page Title="" Language="C#" MasterPageFile="~/Admin/Admin.Master" AutoEventWireup="true" CodeBehind="quanlydonhang.aspx.cs" Inherits="Nhom7.Admin.quanlydonhang" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
     .content-container {
         margin: 20px;
     }

     h2 {
         text-align: center;
         font-size: 24px;
         color: #f2f2f2;
     }

     .gridview-container {
         margin-top: 20px;
     }

     table, th, td {
         border: 1px solid #ddd;
         border-collapse: collapse;
         padding: 12px;
         text-align: left;
         margin-left:auto;
         margin-right:auto;
         background-color: #f2f2f2;

     }

     th {
         background-color: #f2f2f2;
         font-weight: bold;
     }

     .dropdown-status {
         width: 150px;
     }

     .update-button {
         background-color: #4CAF50;
         color: white;
         border: none;
         padding: 8px 16px;
         cursor: pointer;
         border-radius: 5px;
     }

     .update-button:hover {
         background-color: #45a049;
     }

     .message {
         color: red;
         text-align: center;
         font-weight: bold;
     }
 </style>
    <div class="content-container">
    <h2>Danh sách Đơn Hàng</h2>
    <asp:GridView ID="gvOrders" runat="server" AutoGenerateColumns="False" 
                  DataKeyNames="ID_Order" OnRowCommand="gvOrders_RowCommand" 
                  OnRowEditing="gvOrders_RowEditing" OnRowCancelingEdit="gvOrders_RowCancelingEdit"
                  OnRowUpdating="gvOrders_RowUpdating">
        <Columns>
            <asp:BoundField DataField="ID_Order" HeaderText="Mã Đơn Hàng" ReadOnly="True" />
            <asp:BoundField DataField="NgayTao" HeaderText="Ngày Tạo" ReadOnly="True" />
            <asp:BoundField DataField="TongTien" HeaderText="Tổng Tiền" ReadOnly="True" />
            <asp:BoundField DataField="TrangThai" HeaderText="Trạng Thái" ReadOnly="True" />
            
            <asp:TemplateField HeaderText=" Trạng Thái">
                <ItemTemplate>
                    <asp:Label ID="lblTrangThai" runat="server" Text='<%# Eval("TrangThai") %>' />
                </ItemTemplate>
                <EditItemTemplate>
                    <asp:DropDownList ID="ddlTrangThai" runat="server" >
                        <asp:ListItem Text="Chưa giao" Value="Chưa giao" />
                        <asp:ListItem Text="Đang xử lý" Value="Đang xử lý" />
                        <asp:ListItem Text="Đã giao" Value="Đã giao" />
                        <asp:ListItem Text="Đã hủy" Value="Đã hủy" />
                    </asp:DropDownList>
                </EditItemTemplate>
            </asp:TemplateField>
                    <asp:CommandField ShowEditButton="True" ButtonType="Button" EditText="Cập nhật" />
        </Columns>
    </asp:GridView>
    <asp:Label ID="lblMessage" runat="server" CssClass="message" Visible="false" />
</div>
</asp:Content>
