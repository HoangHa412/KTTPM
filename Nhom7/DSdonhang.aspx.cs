using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Data;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7
{
    public partial class DSdonhang : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                // Kiểm tra nếu người dùng đã đăng nhập
                if (Session["UserID"] != null)
                {
                    int userId = Convert.ToInt32(Session["UserID"]);
                    LoadOrders(userId); // Gọi phương thức LoadOrders với userId
                }
                else
                {
                    Response.Redirect("Login.aspx"); // Chuyển hướng tới trang đăng nhập nếu chưa đăng nhập
                }
            }
        }

        // Phương thức tải đơn hàng theo userId
        private void LoadOrders(int userId)
        {
            string connectionString = DATABASECONNECT.getConnectionString();

            // Câu lệnh truy vấn lấy đơn hàng của người dùng
            string query = "SELECT ID_Order, NgayTao, TongTien, TrangThai FROM DonHang WHERE ID_User = @ID_User ORDER BY NgayTao DESC";

            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                try
                {
                    connection.Open();
                    SqlDataAdapter adapter = new SqlDataAdapter(query, connection);
                    // Thêm tham số cho truy vấn SQL
                    adapter.SelectCommand.Parameters.AddWithValue("@ID_User", userId);

                    DataTable dataTable = new DataTable();
                    adapter.Fill(dataTable);

                    // Hiển thị đơn hàng vào GridView
                    gvOrders.DataSource = dataTable;
                    gvOrders.DataBind();
                }
                catch (Exception ex)
                {
                    lblMessage.Text = "Lỗi: " + ex.Message;
                    lblMessage.Visible = true;
                }
            }
        }

        // Xử lý khi người dùng nhấn vào lệnh "Xem đơn hàng"
        protected void gvOrders_RowCommand(object sender, GridViewCommandEventArgs e)
        {
            if (e.CommandName == "ViewOrder")
            {
                string orderId = e.CommandArgument.ToString();
                // Chuyển hướng đến trang xem chi tiết đơn hàng
                Response.Redirect("Xemdonhang.aspx?ID_Order=" + orderId);
            }
        }
    }
}
