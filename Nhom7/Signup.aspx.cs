using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7
{
    public partial class Signup : System.Web.UI.Page
    {
        protected void btnRegister_Click(object sender, EventArgs e)
        {
            // Kiểm tra nếu tất cả các trường đều có giá trị
            if (string.IsNullOrWhiteSpace(txtUsername.Text) || string.IsNullOrWhiteSpace(txtPassword.Text) || string.IsNullOrWhiteSpace(txtEmail.Text) || ddlRole.SelectedValue == "0")
            {
                lblMessage.Text = "Điền đủ thông tin.";
                lblMessage.CssClass = "error-message error show";
                return; // Dừng xử lý nếu chưa đủ dữ liệu
            }

            string connectionString = "Data Source=HOANGHA\\MSSQLSERVER01;Initial Catalog=demosach3;Integrated Security=True;";
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                string query = "INSERT INTO tbluser (TenNguoiDung, MatKhau, Email, SoDienThoai, DiaChi, ID_VaiTro) " +
                               "VALUES (@Username, @Password, @Email, @Phone, @Address, @Role)";

                SqlCommand cmd = new SqlCommand(query, conn);
                cmd.Parameters.AddWithValue("@Username", txtUsername.Text);
                cmd.Parameters.AddWithValue("@Password", txtPassword.Text); // Lưu mật khẩu theo cách đơn giản, có thể mã hóa mật khẩu
                cmd.Parameters.AddWithValue("@Email", txtEmail.Text);
                cmd.Parameters.AddWithValue("@Phone", txtPhone.Text);
                cmd.Parameters.AddWithValue("@Address", txtAddress.Text);
                cmd.Parameters.AddWithValue("@Role", ddlRole.SelectedValue);

                try
                {
                    conn.Open();
                    cmd.ExecuteNonQuery();
                    lblMessage.Text = "Đăng ký thành công";
                    lblMessage.CssClass = "error-message error show";
                    // Chuyển hướng về trang đăng nhập sau khi đăng ký thành công
                    //Response.Redirect("Login.aspx");
                }
                catch (Exception ex)
                {
                    lblMessage.Text = "Lỗi: " + ex.Message;
                }
            }
        }
    }
}