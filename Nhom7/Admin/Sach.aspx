<%@ Page Title="" Language="C#" MasterPageFile="~/Admin/Admin.Master" AutoEventWireup="true" CodeBehind="Sach.aspx.cs" Inherits="Nhom7.Admin.Sach" %>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
        /* File Content/Styles.css */

        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }

        li{
            list-style:none;
        }

        /* Tiêu đề trang */
        h2 {
            font-size: 24px;
            color: #fff;
            margin-bottom: 20px;
        }

        /* Thanh tìm kiếm và nút */
        .search-container {
            margin-bottom: 20px;
            display: flex;
/*            justify-content:space-between;*/
            align-items: center;
/*            border: 1px solid #333;*/
            border-radius: 10px;
            max-width: 50%;
        }

        .search-container input[type="text"] {
            padding: 10px;
            margin-right: 10px;
            width: 250px;
            border: 0px solid #ccc;
            border-radius: 4px;
            outline:none;
            /*background-color: rgba(255, 255, 255, 0.7);*/ /* Nền trắng với độ trong suốt */
        }

        .search-container .btnSearch {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }

        .search-container button:hover {
            background-color: #45a049;
        }

 
        table {
            width: 100%;
/*            border-collapse: collapse;*/
            margin-top: 20px;
            border: 2px solid #ddd;
            border-radius: 10px;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: #f2f2f2;
            color: #333;
        }

        td {
            background-color: #fff;
        }

/*        td input {
            padding: 5px 10px;
            background-color: #0026ff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }*/

        .bntedit {
            padding: 5px 10px;
            background-color: #0026ff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 10px;
        }

        .bntde{
            padding: 5px 10px;
            background-color: #ff0000;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 10px;

        }

        td .be:hover {
            background-color: #00ff21;
        }
        .btnAddNew{
            padding: 6px 14px;
            background-color: #0026ff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom:10px;
        }
        /* Panel Sửa/Thêm sách */
        .edit-panel{
            display: none;
        }
        .titlemain{
            font-size: 40px;
        }
    </style>
    <div>
        <h2 class="titlemain" >Quản lý sách</h2>
        <asp:Label ID="lblMessage" runat="server" ForeColor="Red"></asp:Label>
        <asp:Button ID="btnAddNew" CssClass="btnAddNew" runat="server" Text="Thêm sách mới" OnClick="btnAddNew_Click" />

        <!-- Tìm kiếm sách -->
        <div class="search-container">
            <asp:TextBox ID="txtSearch" runat="server" placeholder="Tìm kiếm sách" />
            <asp:Button ID="btnSearch" CssClass="btnSearch" runat="server" Text="Tìm kiếm" OnClick="btnSearch_Click" />
        </div>

        <!-- Danh sách sách -->
        <asp:Repeater ID="RepeaterBooks" runat="server">
            <HeaderTemplate>
                <table>
                    <tr>
                        <th>Tên Sách</th>
                        <th>Mô Tả</th>
                        <th>Giá</th>
                        <th>Số Lượng Tồn</th>
                        <th>Danh Mục</th>
                        <th>Ảnh</th>
                        <th>Ngày Xuất Bản</th>
                        <th>Hành Động</th>
                    </tr>
            </HeaderTemplate>
            <ItemTemplate>
                <tr>
                    <td><%# Eval("TenSach") %></td>
                    <td><%# Eval("MoTa") %></td>
                    <td><%# Eval("Gia") %></td>
                    <td><%# Eval("SoLuongTon") %></td>
                    <td><%# Eval("TenDanhMuc") %></td> <!-- Hiển thị tên danh mục -->
                    <td><img src='<%# Eval("Anh") %>' alt="Book Image"  style="width:100px;"/></td>
                    
                    <td><%# Eval("NgayXuatBan", "{0:dd/MM/yyyy}") %></td>
                    <td>
                        <asp:Button ID="btnEdit" CssClass="bntedit be" runat="server" Text="Sửa" CommandArgument='<%# Eval("ID_Sach") %>' OnClick="btnEdit_Click" />
                        <asp:Button ID="btnDelete" runat="server" CssClass="bntde be" Text="Xóa" CommandArgument='<%# Eval("ID_Sach") %>' OnClick="btnDelete_Click"  OnClientClick="return confirm('Bạn có chắc chắn muốn xóa không?');"/>
                    </td>
                </tr>
            </ItemTemplate>
            <FooterTemplate>
                </table>
            </FooterTemplate>
        </asp:Repeater>

        <!-- Panel sửa/thêm sách -->
        <asp:Panel ID="pnlEdit" runat="server" Visible="false" CssClass="edit-panel">
            <h3>Sửa/Thêm sách</h3>
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
            <asp:FileUpload ID="fuAnh" runat="server" />
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