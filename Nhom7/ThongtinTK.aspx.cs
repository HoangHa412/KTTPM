using System;
using System.Data.SqlClient;
using System.Web;
using System.Web.UI;

namespace Nhom7
{
    public partial class ThongtinTK : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                if (Session["UserID"] != null)
                {
                    LoadUserInfo();
                }
                else
                {
                     Response.Redirect("Login.aspx");
                }
            }
        }

        private void LoadUserInfo()
        {
            int userId = Convert.ToInt32(Session["UserID"]);
            if (userId == 0)
            {
                Response.Redirect("Login.aspx");
            }

            string connectionString = DATABASECONNECT.getConnectionString();
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                try
                {
                    conn.Open();
                    string query = "SELECT TenNguoiDung, MatKhau, Email, SoDienThoai, DiaChi FROM tbluser WHERE ID_User = @ID_User";
                    using (SqlCommand cmd = new SqlCommand(query, conn))
                    {
                        cmd.Parameters.AddWithValue("@ID_User", userId);
                        SqlDataReader reader = cmd.ExecuteReader();
                        if (reader.Read())
                        {
                            lblTenNguoiDung.Text = reader["TenNguoiDung"].ToString();
                            lblEmail.Text = reader["Email"].ToString();
                            lblSoDienThoai.Text = reader["SoDienThoai"].ToString();
                            lblDiaChi.Text = reader["DiaChi"].ToString();
                            lblMatKhau.Text = reader["MatKhau"].ToString();

                            txtTenNguoiDung.Text = reader["TenNguoiDung"].ToString();
                            txtEmail.Text = reader["Email"].ToString();
                            txtSoDienThoai.Text = reader["SoDienThoai"].ToString();
                            txtDiaChi.Text = reader["DiaChi"].ToString();
                            txtMatKhau.Text = reader["MatKhau"].ToString();
                        }
                    }
                }
                catch (Exception ex)
                {
                    lblMessage.Text = "Error occurred: " + ex.Message;
                }
            }
        }

        protected void btnEdit_Click(object sender, EventArgs e)
        {
            ToggleEditMode(true);
        }

        protected void btnSave_Click(object sender, EventArgs e)
        {
            // Display updated information in labels
            lblTenNguoiDung.Text = txtTenNguoiDung.Text;
            lblEmail.Text = txtEmail.Text;
            lblSoDienThoai.Text = txtSoDienThoai.Text;
            lblDiaChi.Text = txtDiaChi.Text;
            lblMatKhau.Text = txtMatKhau.Text;

            // Hide textboxes and show labels
            ToggleEditMode(false);

            int userId = Convert.ToInt32(Session["UserID"]);
            if (userId == 0)
            {
                lblMessage.Text = "You need to log in to perform this action.";
                lblMessage.Visible = true;
                return;
            }

            string connectionString = DATABASECONNECT.getConnectionString();
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                string query = "UPDATE tbluser SET TenNguoiDung = @TenNguoiDung, Email = @Email, SoDienThoai = @SoDienThoai, DiaChi = @DiaChi, MatKhau = @MatKhau WHERE ID_User = @ID_User";
                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@TenNguoiDung", txtTenNguoiDung.Text.Trim());
                    cmd.Parameters.AddWithValue("@Email", txtEmail.Text.Trim());
                    cmd.Parameters.AddWithValue("@SoDienThoai", txtSoDienThoai.Text.Trim());
                    cmd.Parameters.AddWithValue("@DiaChi", txtDiaChi.Text.Trim());
                    cmd.Parameters.AddWithValue("@MatKhau", txtMatKhau.Text.Trim());
                    cmd.Parameters.AddWithValue("@ID_User", userId);

                    conn.Open();
                    cmd.ExecuteNonQuery();
                }
            }

            string script = "alert('Your information has been updated.');";
            ClientScript.RegisterStartupScript(this.GetType(), "UpdateSuccess", script, true);

            LoadUserInfo();
        }

        protected void btnCancel_Click(object sender, EventArgs e)
        {
            ToggleEditMode(false);
        }

        private void ToggleEditMode(bool isEditMode)
        {
            lblTenNguoiDung.Visible = !isEditMode;
            lblEmail.Visible = !isEditMode;
            lblSoDienThoai.Visible = !isEditMode;
            lblDiaChi.Visible = !isEditMode;
            lblMatKhau.Visible = !isEditMode;

            txtTenNguoiDung.Visible = isEditMode;
            txtEmail.Visible = isEditMode;
            txtSoDienThoai.Visible = isEditMode;
            txtDiaChi.Visible = isEditMode;
            txtMatKhau.Visible = isEditMode;

            btnEdit.Visible = !isEditMode;
            btnSave.Visible = isEditMode;
            btnCancel.Visible = isEditMode;
        }

        protected void btnLogout_Click(object sender, EventArgs e)
        {
            Session.Clear();
            Response.Redirect("Login.aspx");
        }
    }
}
