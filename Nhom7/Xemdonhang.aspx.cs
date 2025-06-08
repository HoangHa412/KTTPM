using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7
{
    public partial class Xemdonhang : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                string orderId = Request.QueryString["ID_Order"];
                if (!string.IsNullOrEmpty(orderId))
                {
                    LoadOrderSummary(orderId);
                }
                else
                {
                    Response.Redirect("DSdonhang.aspx");
                }
            }
        }
        private void LoadOrderSummary(string orderId)
        {
            string connectionString = @"Data Source=HOANGHA\MSSQLSERVER01;Initial Catalog=demosach3;Integrated Security=True;";
            string queryOrder = @"
    SELECT ID_Order, NgayTao, TongTien, TrangThai
    FROM DonHang
    WHERE ID_Order = @ID_Order";

            string queryOrderDetails = @"
    SELECT ct.ID_Sach, s.TenSach, ct.SoLuong, ct.GiaBan, (ct.SoLuong * ct.GiaBan) AS ThanhTien
    FROM ChiTietDonHang ct
    JOIN Sach s ON ct.ID_Sach = s.ID_Sach
    WHERE ct.ID_Order = @ID_Order";

            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                try
                {
                    connection.Open();

                    // Lấy thông tin đơn hàng
                    using (SqlCommand command = new SqlCommand(queryOrder, connection))
                    {
                        command.Parameters.AddWithValue("@ID_Order", orderId);
                        SqlDataReader reader = command.ExecuteReader();

                        if (reader.Read())
                        {
                            lblOrderID.Text = reader["ID_Order"].ToString();
                            lblNgayTao.Text = Convert.ToDateTime(reader["NgayTao"]).ToString("dd/MM/yyyy HH:mm");
                            lblTongTien.Text = string.Format("{0} VND", reader["TongTien"]);
                            lblTrangThai.Text = reader["TrangThai"].ToString();
                        }
                        else
                        {
                            lblMessage.Text = "Không tìm thấy đơn hàng!";
                            lblMessage.Visible = true;
                            return;
                        }
                        reader.Close();
                    }

                    // Lấy chi tiết đơn hàng
                    using (SqlCommand command = new SqlCommand(queryOrderDetails, connection))
                    {
                        command.Parameters.AddWithValue("@ID_Order", orderId);
                        SqlDataAdapter adapter = new SqlDataAdapter(command);
                        DataTable dataTable = new DataTable();
                        adapter.Fill(dataTable);

                        if (dataTable.Rows.Count > 0)
                        {
                            gvOrderDetails.DataSource = dataTable;
                            gvOrderDetails.DataBind();
                        }
                        else
                        {
                            lblMessage.Text = "Không có chi tiết đơn hàng!";
                            lblMessage.Visible = true;
                        }
                    }
                }
                catch (Exception ex)
                {
                    lblMessage.Text = "Lỗi: " + ex.Message;
                    lblMessage.Visible = true;
                }
            }
        }

    }
}