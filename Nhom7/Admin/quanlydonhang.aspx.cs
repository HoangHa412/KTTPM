using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7.Admin
{
    public partial class quanlydonhang : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                LoadOrderList();
            }
        }
        private void LoadOrderList()
        {
            string connectionString = @"Data Source=HOANGHA\MSSQLSERVER01;Initial Catalog=demosach3;Integrated Security=True;";
            string query = "SELECT ID_Order, NgayTao, TongTien, TrangThai FROM DonHang";

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                SqlCommand cmd = new SqlCommand(query, conn);
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                gvOrders.DataSource = reader;
                gvOrders.DataBind();
            }
        }

        protected void gvOrders_RowCommand(object sender, GridViewCommandEventArgs e)
        {
            if (e.CommandName == "UpdateStatus")
            {
                int rowIndex = Convert.ToInt32(e.CommandArgument);
                if (rowIndex >= 0 && rowIndex < gvOrders.Rows.Count)
                {
                    GridViewRow row = gvOrders.Rows[rowIndex];
                    string orderId = gvOrders.DataKeys[rowIndex].Value.ToString();
                    DropDownList ddlStatus = (DropDownList)row.FindControl("ddlStatus");
                    string newStatus = ddlStatus.SelectedValue;
                    UpdateOrderStatus(orderId, newStatus);
                }
                else
                {
                    string script = "alert('Dòng dữ liệu không hợp lệ.');";
                    ClientScript.RegisterStartupScript(this.GetType(), "UpdateSuccess", script, true);
                }
            }
        }
        protected void gvOrders_RowEditing(object sender, GridViewEditEventArgs e)
        {
            gvOrders.EditIndex = e.NewEditIndex;
            LoadOrderList();
        }
        protected void gvOrders_RowUpdating(object sender, GridViewUpdateEventArgs e)
        {
            string orderId = gvOrders.DataKeys[e.RowIndex].Value.ToString();
            GridViewRow row = gvOrders.Rows[e.RowIndex];

            DropDownList ddlTrangThai = (DropDownList)row.FindControl("ddlTrangThai");
            string newStatus = ddlTrangThai.SelectedValue;

            UpdateOrderStatus(orderId, newStatus);

            gvOrders.EditIndex = -1;
            LoadOrderList();
        }

        private void UpdateOrderStatus(string orderId, string newStatus)
        {
            string connectionString = @"Data Source=HOANGHA\MSSQLSERVER01;Initial Catalog=demosach3;Integrated Security=True;";
            string query = "UPDATE DonHang SET TrangThai = @TrangThai WHERE ID_Order = @ID_Order";

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                SqlCommand cmd = new SqlCommand(query, conn);
                cmd.Parameters.AddWithValue("@TrangThai", newStatus);
                cmd.Parameters.AddWithValue("@ID_Order", orderId);

                try
                {
                    conn.Open();
                    cmd.ExecuteNonQuery();
                    string script = "alert('oke.');";
                    ClientScript.RegisterStartupScript(this.GetType(), "UpdateSuccess", script, true);
                    LoadOrderList();
                }
                catch (Exception ex)
                {
                    lblMessage.Text = "Lỗi: " + ex.Message;
                    lblMessage.Visible = true;
                }
            }
        }
        protected void gvOrders_RowCancelingEdit(object sender, GridViewCancelEditEventArgs e)
        {
            gvOrders.EditIndex = -1;

            LoadOrderList();

            lblMessage.Text = "Chỉnh sửa đã bị hủy.";
            lblMessage.Visible = true;
        }
    }
}