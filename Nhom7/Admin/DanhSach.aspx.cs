using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using Nhom7;

namespace Nhom7.Admin
{
    public partial class DanhSach : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                if (Session["userID"] != null)
                {
                    string userId = Session["userID"].ToString();
                    LoadOrders();
                }
                else
                {
                    Response.Redirect("Dangnhap.aspx");
                }
            }
        }
        private void LoadOrders()
        {
            string connectionString = DATABASECONNECT.getConnectionString();

            // Câu lệnh truy vấn lấy tất cả đơn hàng
            string query = "SELECT ID_Order, ID_User, NgayTao, TongTien, TrangThai FROM DonHang ORDER BY NgayTao DESC";

            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                try
                {
                    connection.Open();
                    SqlDataAdapter adapter = new SqlDataAdapter(query, connection);

                    DataTable dataTable = new DataTable();
                    adapter.Fill(dataTable);

                    // Hiển thị tất cả đơn hàng vào GridView
                    gvOrderHistory.DataSource = dataTable;
                    gvOrderHistory.DataBind();
                }
                catch (Exception ex)
                {
                    lblMessage.Text = "Lỗi: " + ex.Message;
                    lblMessage.Visible = true;
                }
            }
        }


        protected void gvOrderHistory_RowCommand(object sender, System.Web.UI.WebControls.GridViewCommandEventArgs e)
        {
            if (e.CommandName == "ViewOrder")
            {
                string orderId = e.CommandArgument.ToString();
                Response.Redirect("Xemdonhang.aspx?ID_Order=" + orderId);
            }
        }
    }

}