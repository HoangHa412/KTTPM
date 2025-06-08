using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7
{
    public partial class Login : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {

        }

        protected void btnLogin_Click(object sender, EventArgs e)
        {
            string username = txtUsername.Text;
            string password = txtPassword.Text;

            // Kiểm tra điều kiện nếu không đúng
            if (string.IsNullOrWhiteSpace(username) || string.IsNullOrWhiteSpace(password))
            {
                lblMessage.Text = "Vui lòng điền đầy đủ thông tin!";
                lblMessage.CssClass = "error-message error show"; // Hiển thị thông báo lỗi
                return;
            }

            // Kiểm tra thông tin đăng nhập (Ví dụ)
            if (username != "admin" || password != "1234")
            {
                lblMessage.Text = "Sai tên đăng nhập hoặc mật khẩu!";
                lblMessage.CssClass = "error-message error show"; // Hiển thị thông báo lỗi
            }
            else
            {
                lblMessage.Text = "Đăng nhập thành công!";
                lblMessage.CssClass = "error-message success show"; // Hiển thị thông báo thành công
            }

            if (string.IsNullOrWhiteSpace(txtUsername.Text) || string.IsNullOrWhiteSpace(txtPassword.Text) || ddlRole.SelectedValue == "0")
            {
                lblMessage.Text = "Vui lòng điền vào tất cả thông tin.";
                return; // Dừng xử lý nếu chưa đủ dữ liệu
            }

            string connectionString = "Data Source=HOANGHA\\MSSQLSERVER01;Initial Catalog=demosach3;Integrated Security=True;";
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                // Truy vấn để lấy vai trò của người dùng (Admin hoặc Khách hàng)
                string query = "SELECT U.ID_User, U.TenNguoiDung, R.TenVaiTro FROM tbluser U INNER JOIN VaiTro R ON U.ID_VaiTro = R.ID_VaiTro WHERE U.TenNguoiDung=@Username AND U.MatKhau=@Password AND U.ID_VaiTro=@RoleID";
                SqlCommand cmd = new SqlCommand(query, conn);
                cmd.Parameters.AddWithValue("@Username", txtUsername.Text);
                cmd.Parameters.AddWithValue("@Password", txtPassword.Text);
                cmd.Parameters.AddWithValue("@RoleID", ddlRole.SelectedValue);

                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();
                if (reader.Read())
                {
                    Session["UserID"] = reader["ID_User"].ToString();
                    Session["Username"] = reader["TenNguoiDung"].ToString();
                    Session["Role"] = reader["TenVaiTro"].ToString();

                    if (reader["TenVaiTro"].ToString() == "admin")
                    {
                        Response.Redirect("~/Admin/Admin.aspx");
                    }
                    else
                    {
                        Response.Redirect("~/HomePage.aspx"); // Đổi thành trang chính của Customer
                    }
                }
                else
                {
                    lblMessage.Text = "Sai tài khoản hoặc mật khẩu hoặc quyền truy cập";
                }
            }
        }
    }
}