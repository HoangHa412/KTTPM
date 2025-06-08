using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7
{
    public partial class Checkout : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                if (Session["UserID"] != null)
                {
                    int userId = Convert.ToInt32(Session["UserID"]);
                    LoadUserData(userId);
                    LoadCart(userId);
                    float totalPrice = LoadCartItems();
                    lblTotalPrice.Text = $"Tổng tiền: {totalPrice} VND"; // Hiển thị tổng tiền lên giao diện
                }
                else
                {
                    Response.Redirect("Login.aspx");
                }
            }
        }

        private void LoadUserData(int userId)
        {
            string query = "SELECT TenNguoiDung, Email, SoDienThoai, DiaChi FROM tbluser WHERE ID_User = @ID_User";
            string connectionString = DATABASECONNECT.getConnectionString();

            using (SqlConnection con = new SqlConnection(connectionString))
            {
                SqlCommand cmd = new SqlCommand(query, con);
                cmd.Parameters.AddWithValue("@ID_User", userId);
                con.Open();
                SqlDataReader reader = cmd.ExecuteReader();
                if (reader.Read())
                {
                    txtTenNguoiDung.Text = reader["TenNguoiDung"].ToString();
                    txtEmail.Text = reader["Email"].ToString();
                    txtSoDienThoai.Text = reader["SoDienThoai"].ToString();
                    txtDiaChi.Text = reader["DiaChi"].ToString();
                }
                con.Close();
            }
        }
        private float LoadCartItems()
        {


            int userId = Convert.ToInt32(Session["UserID"]);  // Lấy ID_User từ session (giả sử đã lưu sau khi đăng nhập)

            // Tạo kết nối tới cơ sở dữ liệu và lấy thông tin giỏ hàng
            DatabaseHelper db = new DatabaseHelper();

            // Lấy CartId của người dùng từ cơ sở dữ liệu
            int cartId = db.GetCartIdByUserId(userId);



            // Lấy danh sách các sản phẩm trong giỏ hàng
            List<CartItem> cartItems = db.GetCartItems(cartId);



            // Tính tổng giá trị giỏ hàng
            float total = 0;
            foreach (var item in cartItems)
            {
                total += (float)item.Gia * item.SoLuong;
            }
            return total; // Trả về tổng tiền kiểu float

        }


        private void LoadCart(int userId)
        {
            string query = @"SELECT s.TenSach, ct.SoLuong, ct.Gia, (ct.SoLuong * ct.Gia) as Tong
                     FROM ChiTietGioHang ct
                     INNER JOIN Sach s ON ct.ID_Sach = s.ID_Sach
                     INNER JOIN GioHang gh ON ct.ID_GioHang = gh.ID_GioHang
                     WHERE gh.ID_User = @ID_User";
            string connectionString = DATABASECONNECT.getConnectionString();

            using (SqlConnection con = new SqlConnection(connectionString))
            {
                SqlCommand cmd = new SqlCommand(query, con);
                cmd.Parameters.Add("@ID_User", SqlDbType.Int).Value = userId;
                con.Open();
                SqlDataReader reader = cmd.ExecuteReader();
                List<CartItem> cartItems = new List<CartItem>();
                while (reader.Read())
                {
                    cartItems.Add(new CartItem
                    {
                        TenSach = reader["TenSach"].ToString(),
                        Gia = Convert.ToDecimal(reader["Gia"]),
                        SoLuong = Convert.ToInt32(reader["SoLuong"]),
                        Tong = Convert.ToDecimal(reader["Tong"])
                    });
                }
                RepeaterCartItems.DataSource = cartItems;
                RepeaterCartItems.DataBind();
                con.Close();
            }
        }

        private List<CartItem> LoadCart2(int userId)
        {
            string query = @"SELECT s.TenSach, s.ID_Sach, ct.SoLuong, ct.Gia, (ct.SoLuong * ct.Gia) as Tong
                     FROM ChiTietGioHang ct
                     INNER JOIN Sach s ON ct.ID_Sach = s.ID_Sach
                     INNER JOIN GioHang gh ON ct.ID_GioHang = gh.ID_GioHang
                     WHERE gh.ID_User = @ID_User";

            string connectionString = DATABASECONNECT.getConnectionString();

            List<CartItem> cartItems = new List<CartItem>();

            using (SqlConnection con = new SqlConnection(connectionString))
            {
                SqlCommand cmd = new SqlCommand(query, con);
                cmd.Parameters.Add("@ID_User", SqlDbType.Int).Value = userId;
                con.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    cartItems.Add(new CartItem
                    {
                        ID_Sach = Convert.ToInt32(reader["ID_Sach"]), // Added this field
                        TenSach = reader["TenSach"].ToString(),
                        Gia = Convert.ToDecimal(reader["Gia"]),
                        SoLuong = Convert.ToInt32(reader["SoLuong"]),
                        Tong = Convert.ToDecimal(reader["Tong"])
                    });
                }

                con.Close();
            }

            return cartItems; // Return the list of cart items
        }


        protected void btnUpdate_Click(object sender, EventArgs e)
        {
            if (Session["UserID"] != null)
            {
                int userId = Convert.ToInt32(Session["UserID"]);
                string tenNguoiDung = txtTenNguoiDung.Text;
                string email = txtEmail.Text;
                string soDienThoai = txtSoDienThoai.Text;
                string diaChi = txtDiaChi.Text;

                string query = @"UPDATE tbluser 
                                 SET TenNguoiDung = @TenNguoiDung, Email = @Email, 
                                     SoDienThoai = @SoDienThoai, DiaChi = @DiaChi 
                                 WHERE ID_User = @ID_User";
                string connectionString = DATABASECONNECT.getConnectionString();

                using (SqlConnection con = new SqlConnection(connectionString))
                {
                    SqlCommand cmd = new SqlCommand(query, con);
                    cmd.Parameters.AddWithValue("@ID_User", userId);
                    cmd.Parameters.AddWithValue("@TenNguoiDung", tenNguoiDung);
                    cmd.Parameters.AddWithValue("@Email", email);
                    cmd.Parameters.AddWithValue("@SoDienThoai", soDienThoai);
                    cmd.Parameters.AddWithValue("@DiaChi", diaChi);

                    con.Open();
                    int rowsAffected = cmd.ExecuteNonQuery();
                    con.Close();

                    if (rowsAffected > 0)
                    {
                        lblMessage.Text = "Cập nhật thông tin thành công!";
                        lblMessage.ForeColor = System.Drawing.Color.Green;
                    }
                    else
                    {
                        lblMessage.Text = "Cập nhật thông tin thất bại!";
                        lblMessage.ForeColor = System.Drawing.Color.Red;
                    }
                }
            }
            else
            {
                Response.Redirect("Login.aspx");
            }
        }

        protected void btnThanhToan_Click(object sender, EventArgs e)
        {
            if (Session["UserID"] != null)
            {
                int userId = Convert.ToInt32(Session["UserID"]);

                // Gọi phương thức LoadCartItems để lấy giỏ hàng và tổng tiền
                float totalPrice = LoadCartItems();

                // Kiểm tra xem tổng tiền có đúng không
                Console.WriteLine($"Tổng tiền: {totalPrice}");

                // Khởi tạo đối tượng DatabaseHelper để thao tác với cơ sở dữ liệu
                DatabaseHelper dbHelper = new DatabaseHelper();

                // Thêm đơn hàng vào cơ sở dữ liệu
                int orderId = dbHelper.CreateOrder(userId, totalPrice);



                string query = @"SELECT s.TenSach, s.ID_Sach, ct.SoLuong, ct.Gia, (ct.SoLuong * ct.Gia) as Tong
                 FROM ChiTietGioHang ct
                 INNER JOIN Sach s ON ct.ID_Sach = s.ID_Sach
                 INNER JOIN GioHang gh ON ct.ID_GioHang = gh.ID_GioHang
                 WHERE gh.ID_User = @ID_User";

                string connectionString = DATABASECONNECT.getConnectionString();

                List<CartItem> cartItems = new List<CartItem>();

                using (SqlConnection con = new SqlConnection(connectionString))
                {
                    SqlCommand cmd = new SqlCommand(query, con);
                    cmd.Parameters.Add("@ID_User", SqlDbType.Int).Value = userId;
                    con.Open();
                    SqlDataReader reader = cmd.ExecuteReader();

                    while (reader.Read())
                    {
                        int ID_Sach = Convert.ToInt32(reader["ID_Sach"]);
                        string TenSach = reader["TenSach"].ToString();
                        decimal Gia = Convert.ToDecimal(reader["Gia"]);
                        int SoLuong = Convert.ToInt32(reader["SoLuong"]);
                        decimal Tong = Convert.ToDecimal(reader["Tong"]);

                        cartItems.Add(new CartItem
                        {
                            ID_Sach = ID_Sach,
                            TenSach = TenSach,
                            Gia = Gia,
                            SoLuong = SoLuong,
                            Tong = Tong
                        });

                        // Add order detail for each item
                        dbHelper.AddOrderDetail(orderId, ID_Sach, SoLuong, (float)Gia);
                    }

                    //con.Close();
                }


                    // Lấy phương thức thanh toán từ DropDownList
                    string paymentMethod = ddlPaymentMethod.SelectedValue;

                // Thêm thông tin thanh toán
                dbHelper.CreatePayment(orderId, paymentMethod, totalPrice);

                // Cập nhật trạng thái đơn hàng
                dbHelper.UpdateOrderStatus(orderId, "Đang xử lý");

                // Xóa giỏ hàng
                dbHelper.ClearCart(userId);

                // Hiển thị tổng tiền lên giao diện
                lblTotalPrice.Text = $"Tổng tiền: {totalPrice:C}";

                // Chuyển đến trang thông báo thanh toán thành công
                Response.Redirect("ThanhToanThanhCong.aspx");
            }
            else
            {
                // Nếu người dùng chưa đăng nhập, chuyển đến trang đăng nhập
                Response.Redirect("Login.aspx");
            }
        }
    }
}
