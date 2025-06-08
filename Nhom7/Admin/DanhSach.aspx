<%@ Page Title="" Language="C#" MasterPageFile="~/Admin/Admin.Master" AutoEventWireup="true" CodeBehind="DanhSach.aspx.cs" Inherits="Nhom7.Admin.DanhSach" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <asp:Label ID="lblMessage" runat="server" ForeColor="Red"></asp:Label>
    <style>
        .btn-view-history {
            background-color: #ffffff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            text-align: center;
        }
    </style>
    <h2 style="color:#fff;">Lịch Sử Đơn Hàng</h2>
    <div class="btn-view-history">
        <asp:GridView ID="gvOrderHistory" runat="server" AutoGenerateColumns="False"
            CellPadding="4" ForeColor="#333333" GridLines="None"
            OnRowCommand="gvOrderHistory_RowCommand">
            <Columns>
                <asp:BoundField DataField="ID_Order" HeaderText="Mã Đơn Hàng" SortExpression="ID_Order" />
                <asp:BoundField DataField="NgayTao" HeaderText="Ngày Tạo" SortExpression="NgayTao" />
                <asp:BoundField DataField="TongTien" HeaderText="Tổng Tiền" SortExpression="TongTien" />
                <asp:BoundField DataField="TrangThai" HeaderText="Trạng Thái" SortExpression="TrangThai" />
                <asp:TemplateField>
                    <ItemTemplate>
                        <asp:Button ID="btnViewOrder" runat="server" Text="Xem Chi Tiết" CommandName="ViewOrder"
                            CommandArgument='<%# Eval("ID_Order") %>' />
                    </ItemTemplate>
                </asp:TemplateField>
            </Columns>
        </asp:GridView>
    </div>

</asp:Content>
