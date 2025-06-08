using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7.Admin
{
    public partial class themvasua : System.Web.UI.Page
    {
        private string connectionString = "Data Source=HOANGHA\\MSSQLSERVER01;Initial Catalog=demosach3;Integrated Security=True;";

        protected void Page_Load(object sender, EventArgs e)
        {
            //if (Session["Role"] != null)
            //{
            //    lblMessage.Text = "Session Role: " + Session["Role"].ToString();
            //}
            //else
            //{
            //    lblMessage.Text = "Session Role is null";
            //}
            if (Session["UserID"] == null || Session["Role"].ToString() != "admin")
            {
                Response.Redirect("~/Login.aspx");
            }

            if (!IsPostBack)
            {
                LoadDanhMuc();
                if (!string.IsNullOrEmpty(Request.QueryString["ID_Sach"]))
                {
                    LoadSach(Request.QueryString["ID_Sach"]);
                }
            }
        }

        private void LoadDanhMuc()
        {

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                string sql = "SELECT ID_DanhMuc, TenDanhMuc FROM DanhMuc";

                using (SqlCommand cmd = new SqlCommand(sql, conn))
                {
                    SqlDataReader reader = cmd.ExecuteReader();
                    ddlDanhMuc.DataSource = reader;
                    ddlDanhMuc.DataTextField = "TenDanhMuc";
                    ddlDanhMuc.DataValueField = "ID_DanhMuc";
                    ddlDanhMuc.DataBind();
                }
            }

            ddlDanhMuc.Items.Insert(0, new ListItem("--Chọn danh mục--", "0"));
        }


        public void LoadSach(string idSach)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                SqlCommand cmd = new SqlCommand("SELECT * FROM Sach WHERE ID_Sach = @ID_Sach", conn);
                cmd.Parameters.AddWithValue("@ID_Sach", idSach);
                SqlDataReader reader = cmd.ExecuteReader();

                if (reader.Read())
                {
                    txtID.Text = reader["ID_Sach"].ToString();
                    txtTenSach.Text = reader["TenSach"].ToString();
                    txtMoTa.Text = reader["MoTa"].ToString();
                    txtGia.Text = reader["Gia"].ToString();
                    txtSoLuongTon.Text = reader["SoLuongTon"].ToString();
                    txtNgayXuatBan.Text = Convert.ToDateTime(reader["NgayXuatBan"]).ToString("yyyy-MM-dd");
                    ddlDanhMuc.SelectedValue = reader["ID_DanhMuc"].ToString();

                    // Load the image if it exists
                    if (!string.IsNullOrEmpty(reader["Anh"].ToString()))
                    {
                        imgPreview.ImageUrl = "~/image/" + reader["Anh"].ToString();
                    }
                }
            }
        }


        protected void btnSave_Click(object sender, EventArgs e)
        {

            if (string.IsNullOrEmpty(txtTenSach.Text) || string.IsNullOrEmpty(txtMoTa.Text) ||
            string.IsNullOrEmpty(txtGia.Text) || string.IsNullOrEmpty(txtSoLuongTon.Text) || ddlDanhMuc.SelectedIndex == 0)
            {

                lblMessage.Text = "Vui lòng nhập đủ thông tin.";
                lblMessage.ForeColor = System.Drawing.Color.Red;
                return;
            }

            string fileName = null;
            if (fileUpload.HasFile)
            {
                fileName = Path.GetFileName(fileUpload.PostedFile.FileName);
                fileUpload.SaveAs(Server.MapPath("~/image/") + fileName);
            }


            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                string query;



                if (string.IsNullOrEmpty(txtID.Text))
                {
                    query = "INSERT INTO Sach (TenSach, MoTa, Gia, SoLuongTon, NgayXuatBan, ID_DanhMuc, Anh) VALUES (@TenSach, @MoTa, @Gia, @SoLuongTon, @NgayXuatBan, @ID_DanhMuc, @Anh)";
                }
                else
                {
                    query = "UPDATE Sach SET TenSach=@TenSach, MoTa=@MoTa, Gia=@Gia, SoLuongTon=@SoLuongTon, NgayXuatBan=@NgayXuatBan, ID_DanhMuc=@ID_DanhMuc, Anh=@Anh WHERE ID_Sach=@ID_Sach";
                }

                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    if (!string.IsNullOrEmpty(txtID.Text))
                    {
                        cmd.Parameters.AddWithValue("@ID_Sach", txtID.Text);
                        lblMessage.Text = "Lưu thành công";
                    }
                    cmd.Parameters.AddWithValue("@TenSach", txtTenSach.Text);
                    cmd.Parameters.AddWithValue("@MoTa", txtMoTa.Text);
                    cmd.Parameters.AddWithValue("@Gia", txtGia.Text);
                    cmd.Parameters.AddWithValue("@SoLuongTon", txtSoLuongTon.Text);
                    cmd.Parameters.AddWithValue("@NgayXuatBan", txtNgayXuatBan.Text);
                    cmd.Parameters.AddWithValue("@ID_DanhMuc", ddlDanhMuc.SelectedValue);
                    cmd.Parameters.AddWithValue("@Anh", fileName);

                    cmd.ExecuteNonQuery();
                }
            }

            lblMessage.Text = "Lưu thông tin sách thành công.";
            pnlEdit.Visible = false;
            Response.Redirect("Sach.aspx");
        }

        protected void btnCancel_Click(object sender, EventArgs e)
        {
            //pnlEdit.Visible = false;
            //ClearForm();
            Response.Redirect("Sach.aspx");
        }



    }
}