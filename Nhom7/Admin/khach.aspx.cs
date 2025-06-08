using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7.Admin
{
    public partial class khach : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                BindData();
            }
        }

        private void BindData()
        {
            QLKH qlkh = new QLKH();
            List<User> dsKhachHang = qlkh.GetDSKH();
            RepeaterCustomer.DataSource = dsKhachHang;
            RepeaterCustomer.DataBind();
        }
    }

    public class QLKH
    {

        private string connectionString = DATABASECONNECT.getConnectionString();
        // Phương thức lấy danh sách khách hàng
        public List<User> GetDSKH()
        {
            List<User> ds = new List<User>();
            string query = @"
                SELECT 
                    u.ID_User,
                    u.TenNguoiDung,
                    u.Email,
                    u.MatKhau,
                    u.SoDienThoai,
                    u.DiaChi,
                    COUNT(dh.ID_Order) AS SoDonMua
                FROM 
                    tbluser u
                LEFT JOIN 
                    DonHang dh ON u.ID_User = dh.ID_User
                WHERE 
                    u.ID_Vaitro = 2
                GROUP BY 
                    u.ID_User, 
                    u.TenNguoiDung, 
                    u.Email, 
                    u.MatKhau,
                    u.SoDienThoai, 
                    u.DiaChi;";

            SqlConnection con = new SqlConnection(connectionString);

            try
            {
                con.Open();
                SqlCommand cmd = new SqlCommand(query, con);
                SqlDataReader rd = cmd.ExecuteReader();
                while (rd.Read())
                {
                    User u = new User();
                    u.ID_User = (int)rd["ID_User"];
                    u.TenNguoiDung = (string)rd["TenNguoiDung"];
                    u.Email = (string)rd["Email"];
                    u.MatKhau = (string)rd["MatKhau"];
                    u.SoDienThoai = (string)rd["SoDienThoai"];
                    u.DiaChi = (string)rd["DiaChi"];
                    u.SoDonMua = (int)rd["SoDonMua"];
                    ds.Add(u);  // Thêm vào danh sách khách hàng
                }
            }
            catch (Exception ex)
            {
                // Log lỗi hoặc xử lý lỗi ở đây
                throw new ApplicationException("Lỗi khi kết nối cơ sở dữ liệu: " + ex.Message);
            }
            finally
            {
                if (con.State == System.Data.ConnectionState.Open)
                {
                    con.Close();
                }
            }

            return ds;
        }
    }

    public class User
    {
        public int ID_User { get; set; }
        public string TenNguoiDung { get; set; }
        public string Email { get; set; }
        public string MatKhau { get; set; }
        public string SoDienThoai { get; set; }
        public string DiaChi { get; set; }
        public int SoDonMua { get; set; }
    }
}
