<%@ Page Title="" Language="C#" MasterPageFile="~/Admin/Admin.Master" AutoEventWireup="true" CodeBehind="suasach.aspx.cs" Inherits="Nhom7.Admin.suasach" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
     <style>
     .edit-panel {
         background-color: white;
         padding: 20px;
         border-radius: 4px;
         box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
         margin-top: 30px;
     }

     .edit-panel label {
         display: block;
         margin-bottom: 10px;
         font-weight: bold;
     }

     .edit-panel input[type="text"] {
         width: 100%;
         padding: 10px;
         margin-bottom: 15px;
         border: 1px solid #ccc;
         border-radius: 4px;
     }

     .edit-panel button {
         padding: 10px 20px;
         background-color: #4CAF50;
         color: white;
         border: none;
         border-radius: 4px;
         cursor: pointer;
         margin-right: 10px;
     }

     .edit-panel button:hover {
         background-color: #0026ff;
     }

     .edit-panel .cancel-button {
         background-color: #f44336;
     }

     .edit-panel .cancel-button:hover {
         background-color: #e53935;
     }
 </style>
<div>
     <h2><%# string.IsNullOrEmpty(Request.QueryString["ID_Sach"]) ? "Thêm Sách Mới" : "Sửa Sách" %></h2>
     <asp:Label ID="lblMessage" runat="server" ForeColor="Red"></asp:Label>
     <asp:Panel ID="pnlEdit" runat="server" CssClass="edit-panel">
         <asp:Label ID="lblID" runat="server" Text="ID Sách: " Visible="false"></asp:Label>
         <asp:TextBox ID="txtID" runat="server" Visible="false"></asp:TextBox>
         <br />
         <asp:Label ID="lblTenSach" runat="server" Text="Tên Sách: "></asp:Label>
         <asp:TextBox ID="txtTenSach" runat="server"></asp:TextBox>
         <br />
         <asp:Label ID="lblMoTa" runat="server" Text="Mô Tả: "></asp:Label>
         <asp:TextBox ID="txtMoTa" runat="server"></asp:TextBox>
         <br />
         <asp:Label ID="lblGia" runat="server" Text="Giá: "></asp:Label>
         <asp:TextBox ID="txtGia" runat="server"></asp:TextBox>
         <br />
         <asp:Label ID="lblSoLuongTon" runat="server" Text="Số Lượng Tồn: "></asp:Label>
         <asp:TextBox ID="txtSoLuongTon" runat="server"></asp:TextBox>
         <br />
         <asp:Label ID="lblAnh" runat="server" Text="Ảnh: "></asp:Label>
        <asp:FileUpload ID="fileUpload" runat="server" />
        <asp:Image ID="imgPreview" runat="server" Width="200px" />
        <br />
         <asp:Label ID="lblNgayXuatBan" runat="server" Text="Ngày Xuất Bản: "></asp:Label>
         <asp:TextBox ID="txtNgayXuatBan" runat="server"></asp:TextBox>
         <br />
         <asp:Label ID="lblDanhMuc" runat="server" Text="Danh Mục: "></asp:Label>
         <asp:DropDownList ID="ddlDanhMuc" runat="server"></asp:DropDownList>
         <br />
         <asp:Button ID="btnSave" runat="server" Text="Lưu" OnClick="btnSave_Click" />
         <asp:Button ID="btnCancel" runat="server" Text="Hủy" OnClick="btnCancel_Click" CssClass="cancel-button" />
     </asp:Panel>
 </div>
</asp:Content>