using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7.Admin
{
    public partial class Sach : System.Web.UI.Page
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
                LoadBooks();
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


        private void LoadBooks(string searchQuery = "")
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                string query = @"SELECT S.*, D.TenDanhMuc 
                         FROM Sach S 
                         JOIN DanhMuc D ON S.ID_DanhMuc = D.ID_DanhMuc";
                if (!string.IsNullOrEmpty(searchQuery))
                {
                    query += " WHERE S.TenSach LIKE @SearchQuery";
                }

                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    if (!string.IsNullOrEmpty(searchQuery))
                    {
                        cmd.Parameters.AddWithValue("@SearchQuery", "%" + searchQuery + "%");
                    }

                    SqlDataAdapter da = new SqlDataAdapter(cmd);
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    // Bind the data to the Repeater
                    RepeaterBooks.DataSource = dt;
                    RepeaterBooks.DataBind();
                }
            }
        }

        protected void btnSearch_Click(object sender, EventArgs e)
        {
            LoadBooks(txtSearch.Text.Trim());
        }

        protected void btnAddNew_Click(object sender, EventArgs e)
        {
            //pnlEdit.Visible = true;
            //ClearForm();
            Response.Redirect("themvasua.aspx");
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


            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                string query;



                if (string.IsNullOrEmpty(txtID.Text))
                {
                    query = "INSERT INTO Sach (TenSach, MoTa, Gia, SoLuongTon, NgayXuatBan, ID_DanhMuc) VALUES (@TenSach, @MoTa, @Gia, @SoLuongTon, @NgayXuatBan, @ID_DanhMuc)";
                }
                else
                {
                    query = "UPDATE Sach SET TenSach=@TenSach, MoTa=@MoTa, Gia=@Gia, SoLuongTon=@SoLuongTon, NgayXuatBan=@NgayXuatBan, ID_DanhMuc=@ID_DanhMuc WHERE ID_Sach=@ID_Sach";
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


                    cmd.ExecuteNonQuery();

                }
            }
            lblMessage.Text = "Lưu thông tin sách thành công.";
            pnlEdit.Visible = false;

            LoadBooks();
        }

        protected void btnCancel_Click(object sender, EventArgs e)
        {
            pnlEdit.Visible = false;
            ClearForm();
        }

        protected void btnEdit_Click(object sender, EventArgs e)
        {
            string idSach = (sender as Button).CommandArgument;
            Response.Redirect("SuaSach.aspx?ID_Sach=" + idSach);

        }

        protected void btnDelete_Click(object sender, EventArgs e)
        {
            Button btnDelete = (Button)sender;
            int id = Convert.ToInt32(btnDelete.CommandArgument);

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                string query = "DELETE FROM Sach WHERE ID_Sach=@ID_Sach";

                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@ID_Sach", id);
                    cmd.ExecuteNonQuery();
                }
            }

            LoadBooks();
        }

        private void ClearForm()
        {
            txtID.Text = "";
            txtTenSach.Text = "";
            txtMoTa.Text = "";
            txtGia.Text = "";
            txtSoLuongTon.Text = "";
            txtNgayXuatBan.Text = "";
            ddlDanhMuc.SelectedIndex = 0;
        }
    }
}