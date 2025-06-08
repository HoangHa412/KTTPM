<%@ Page Title="" Language="C#" MasterPageFile="~/SitePage.Master" AutoEventWireup="true" CodeBehind="DSdonhang.aspx.cs" Inherits="Nhom7.DSdonhang" %>

<asp:Content ID="Content1" ContentPlaceHolderID="TitleContent" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            box-sizing: border-box;
        }

        form {
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            border-radius: 8px;
            width: 100%;
            /*         width: 900px; */
            margin-top: 30px;
        }

        h2 {
            text-align: center;
            font-size: 24px;
            color: #333;
            margin-bottom: 30px;
        }

        table {
            width: 900px;
            border-collapse: collapse;
            /*        margin-top: 20px;
         margin-bottom: 20px;*/
            margin-left: auto;
            margin-right: auto;
        }

        table, th, td {
            border: 1px solid #ddd;
        }

        th, td {
            padding: 12px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
            color: #333;
            font-weight: bold;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            margin-top: 10px;
            display: block;
            width: 100%;
            box-sizing: border-box;
        }

            button:hover {
                background-color: #45a049;
            }

        .message {
            color: red;
            text-align: center;
            font-weight: bold;
        }
    </style>
    <div>
        <h2>Danh sách Đơn Hàng</h2>
        <asp:GridView ID="gvOrders" runat="server" AutoGenerateColumns="False"
            CellPadding="4" ForeColor="#333333" GridLines="None"
            OnRowCommand="gvOrders_RowCommand" Height="400px">
            <Columns>
                <asp:BoundField DataField="ID_Order" HeaderText="Mã đơn hàng" SortExpression="ID_Order" />
                <asp:BoundField DataField="NgayTao" HeaderText="Ngày tạo" SortExpression="NgayTao" />
                <asp:BoundField DataField="TongTien" HeaderText="Tổng tiền" SortExpression="TongTien" />
                <asp:BoundField DataField="TrangThai" HeaderText="Trạng thái" SortExpression="TrangThai" />
                <asp:TemplateField>
                    <ItemTemplate>
                        <asp:Button ID="btnViewOrder" runat="server" CommandName="ViewOrder" CommandArgument='<%# Eval("ID_Order") %>' Text="Xem" />
                    </ItemTemplate>
                </asp:TemplateField>
            </Columns>
        </asp:GridView>
        <asp:Label ID="lblMessage" runat="server" ForeColor="Red" Visible="false" />
    </div>
</asp:Content>
