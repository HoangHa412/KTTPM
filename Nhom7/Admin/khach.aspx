<%@ Page Title="" Language="C#" MasterPageFile="~/Admin/Admin.Master" AutoEventWireup="true" CodeBehind="khach.aspx.cs" Inherits="Nhom7.Admin.khach" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f9;
        }

        h1 {
            text-align: center;
            color: #f2f2f2;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: #fff;
        }

        th, td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }

        th {
            background-color: #007bff;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        tr:hover {
            background-color: #f1f1f1;
        }

        .btn {
            padding: 5px 10px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }

        .btn-delete {
            background-color: #dc3545;
            color: white;
        }

            .btn-delete:hover {
                background-color: #c82333;
            }
    </style>

    <h1 style="color: #f2f2f2;">Quản lý khách hàng</h1>
    <table>
        <thead>
            <tr>
                <th>ID User</th>
                <th>Tên Người Dùng</th>
                <th>Email</th>
                <th>Số Điện Thoại</th>
                <th>Địa Chỉ</th>
                <th>Số Đơn Mua</th>
            </tr>
        </thead>
        <tbody>
            <asp:Repeater ID="RepeaterCustomer" runat="server">
                <ItemTemplate>
                    <tr>
                        <td><%# Eval("ID_User") %></td>
                        <td><%# Eval("TenNguoiDung") %></td>
                        <td><%# Eval("Email") %></td>
                        <td><%# Eval("SoDienThoai") %></td>
                        <td><%# Eval("DiaChi") %></td>
                        <td><%# Eval("SoDonMua") %></td>
                    </tr>
                </ItemTemplate>
            </asp:Repeater>
        </tbody>
    </table>
</asp:Content>
