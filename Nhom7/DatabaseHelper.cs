using Nhom7;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;

public class DatabaseHelper
{
    public SqlConnection con;

    public DatabaseHelper()
    {
        String sqlCon = DATABASECONNECT.getConnectionString();
        //Thay bằng sql của mng
        //using (SqlConnection con = new SqlConnection(sqlCon));
        con = new SqlConnection(sqlCon);
    }

    
    // Lấy danh sách sách từ cơ sở dữ liệu
    public List<Sach> GetBooks()
    {
        List<Sach> books = new List<Sach>();
        string query = "SELECT ID_Sach, TenSach, MoTa, Gia, SoLuongTon, ID_DanhMuc, NgayXuatBan, Anh FROM Sach";
        con.Open();
        SqlCommand cmd = new SqlCommand(query, con);
        SqlDataReader rd = cmd.ExecuteReader();
        while (rd.Read())
        {
            Sach s = new Sach
            {
                ID_Sach = rd["ID_Sach"] != DBNull.Value ? (int)rd["ID_Sach"] : 0,
                TenSach = rd["TenSach"] != DBNull.Value ? (string)rd["TenSach"] : string.Empty,
                MoTa = rd["MoTa"] != DBNull.Value ? (string)rd["MoTa"] : string.Empty,
                Gia = rd["Gia"] != DBNull.Value ? (decimal)rd["Gia"] : 0,
                SoLuongTon = rd["SoLuongTon"] != DBNull.Value ? (int)rd["SoLuongTon"] : 0,
                ID_DanhMuc = rd["ID_DanhMuc"] != DBNull.Value ? (int)rd["ID_DanhMuc"] : 0,
                NgayXuatBan = rd["NgayXuatBan"] != DBNull.Value ? (DateTime)rd["NgayXuatBan"] : DateTime.MinValue,
                Anh = rd["Anh"] != DBNull.Value ? (string)rd["Anh"] : string.Empty
            };
            books.Add(s);
        }
        con.Close();
        return books;
    }
    public Sach GetBookById(int idSach)
    {
        Sach book = null;
        string query = @"
        SELECT 
            Sach.ID_Sach, 
            Sach.TenSach, 
            Sach.MoTa, 
            Sach.Gia, 
            Sach.SoLuongTon, 
            Sach.NgayXuatBan, 
            Sach.Anh, 
            TacGia.TenTacGia, 
            DanhMuc.TenDanhMuc
        FROM Sach
        INNER JOIN TacGia ON Sach.ID_TacGia = TacGia.ID_TacGia
        INNER JOIN DanhMuc ON Sach.ID_DanhMuc = DanhMuc.ID_DanhMuc
        WHERE Sach.ID_Sach = @ID_Sach";

        con.Open();
        SqlCommand cmd = new SqlCommand(query, con);
        cmd.Parameters.AddWithValue("@ID_Sach", idSach);

        SqlDataReader reader = cmd.ExecuteReader();
        if (reader.Read())
        {
            book = new Sach()
            {
                ID_Sach = (int)reader["ID_Sach"],
                TenSach = (string)reader["TenSach"],
                MoTa = (string)reader["MoTa"],
                Gia = (decimal)reader["Gia"],
                SoLuongTon = (int)reader["SoLuongTon"],
                TenDanhMuc = (string)reader["TenDanhMuc"],
                NgayXuatBan = (DateTime)reader["NgayXuatBan"],
                Anh = (string)reader["Anh"],
                TenTacGia = (string)reader["TenTacGia"]
            };
        }
        con.Close();
        return book;
    }
    // Tạo giỏ hàng mới
    public int CreateCart(int userId)
    {
        string query = "INSERT INTO GioHang (ID_User, NgayTao) OUTPUT INSERTED.ID_GioHang VALUES (@ID_User, GETDATE())";
        con.Open();
        SqlCommand cmd = new SqlCommand(query, con);
        cmd.Parameters.AddWithValue("@ID_User", userId);
        int cartId = (int)cmd.ExecuteScalar();
        con.Close();
        return cartId;
    }

    // Thêm sản phẩm vào giỏ hàng
    public void AddToCart(int cartId, int bookId, int quantity, decimal price)
    {
        string checkQuery = "SELECT COUNT(*) FROM ChiTietGioHang WHERE ID_GioHang = @CartID AND ID_Sach = @BookID";

        con.Open();
        {
            SqlCommand checkCmd = new SqlCommand(checkQuery, con);
            checkCmd.Parameters.AddWithValue("@CartID", cartId);
            checkCmd.Parameters.AddWithValue("@BookID", bookId);

            int count = (int)checkCmd.ExecuteScalar();

            if (count > 0)  // Sản phẩm đã có trong giỏ hàng, cập nhật số lượng
            {
                string updateQuery = "UPDATE ChiTietGioHang SET SoLuong = SoLuong + @Quantity WHERE ID_GioHang = @CartID AND ID_Sach = @BookID";
                SqlCommand updateCmd = new SqlCommand(updateQuery, con);
                updateCmd.Parameters.AddWithValue("@Quantity", quantity);
                updateCmd.Parameters.AddWithValue("@CartID", cartId);
                updateCmd.Parameters.AddWithValue("@BookID", bookId);
                updateCmd.ExecuteNonQuery();
            }
            else  // Sản phẩm chưa có trong giỏ hàng, thêm mới
            {
                string insertQuery = "INSERT INTO ChiTietGioHang (ID_GioHang, ID_Sach, SoLuong, Gia) VALUES (@CartID, @BookID, @Quantity, @Price)";
                SqlCommand insertCmd = new SqlCommand(insertQuery, con);
                insertCmd.Parameters.AddWithValue("@CartID", cartId);
                insertCmd.Parameters.AddWithValue("@BookID", bookId);
                insertCmd.Parameters.AddWithValue("@Quantity", quantity);
                insertCmd.Parameters.AddWithValue("@Price", price);
                insertCmd.ExecuteNonQuery();
            }
        }
        con.Close();

    }


    // Lấy danh sách sản phẩm trong giỏ hàng
    public List<CartItem> GetCartItems(int cartId)
    {
        List<CartItem> cartItems = new List<CartItem>();
        string query = @"
                        SELECT 
                            Sach.ID_Sach, 
                            Sach.TenSach, 
                            Sach.Gia, 
                            ChiTietGioHang.SoLuong, 
                            Sach.Anh,
                            (ChiTietGioHang.SoLuong * Sach.Gia) AS Tong
                        FROM ChiTietGioHang
                        INNER JOIN Sach ON ChiTietGioHang.ID_Sach = Sach.ID_Sach
                        WHERE ChiTietGioHang.ID_GioHang = @ID_GioHang";

        {
            con.Open();

            SqlCommand cmd = new SqlCommand(query, con);
            cmd.Parameters.Add(new SqlParameter("@ID_GioHang", SqlDbType.Int) { Value = cartId });

            try
            {
                using (SqlDataReader reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        CartItem item = new CartItem
                        {
                            ID_Sach = reader.GetInt32(reader.GetOrdinal("ID_Sach")),
                            TenSach = reader.GetString(reader.GetOrdinal("TenSach")),
                            Gia = reader.GetDecimal(reader.GetOrdinal("Gia")),
                            SoLuong = reader.GetInt32(reader.GetOrdinal("SoLuong")),
                            Anh = reader.GetString(reader.GetOrdinal("Anh")),
                            Tong = reader.GetDecimal(reader.GetOrdinal("Tong"))
                        };
                        cartItems.Add(item);
                    }
                }
            }
            catch (SqlException ex)
            {
                // Log exception if necessary
                throw new Exception("Database error occurred while fetching cart items.", ex);
            }
            catch (Exception ex)
            {
                // Log exception if necessary
                throw new Exception("An error occurred while fetching cart items.", ex);
            }
        }
        con.Close();

        return cartItems;
    }



    public int GetCartIdByUserId(int userId)
    {
        string query = "SELECT ID_GioHang FROM GioHang WHERE ID_User = @UserID";

        con.Open();
        {
            SqlCommand cmd = new SqlCommand(query, con);
            cmd.Parameters.AddWithValue("@UserID", userId);

            var result = cmd.ExecuteScalar();
            con.Close();

            return result != null ? Convert.ToInt32(result) : 0;  // Trả về CartID nếu tìm thấy, nếu không trả về 0
        }
    }

    public void UpdateCartItemQuantity(int cartId, int bookId, int quantity)
    {
        string query = "UPDATE ChiTietGioHang SET SoLuong = @Quantity WHERE ID_GioHang = @CartId AND ID_Sach = @BookId";
        con.Open();

        {
            SqlCommand cmd = new SqlCommand(query, con);
            cmd.Parameters.AddWithValue("@CartId", cartId);
            cmd.Parameters.AddWithValue("@BookId", bookId);
            cmd.Parameters.AddWithValue("@Quantity", quantity);

            cmd.ExecuteNonQuery();
            con.Close();
        }
    }
    public void DeleteCartItem(int cartId, int bookId)
    {
        string query = "DELETE FROM ChiTietGioHang WHERE ID_GioHang = @CartId AND ID_Sach = @BookId";
        con.Open();

        {
            SqlCommand cmd = new SqlCommand(query, con);
            cmd.Parameters.AddWithValue("@CartId", cartId);
            cmd.Parameters.AddWithValue("@BookId", bookId);

            cmd.ExecuteNonQuery();
            con.Close();
        }
    }

    public List<Sach> GetBooksByDanhMuc(int idDanhMuc)
    {
        List<Sach> books = new List<Sach>();
        string query = "SELECT ID_Sach, TenSach, MoTa, Gia, SoLuongTon, ID_DanhMuc, NgayXuatBan, Anh " +
                       "FROM Sach " +
                       "WHERE ID_DanhMuc = @ID_DanhMuc";
        try
        {
            con.Open();
            SqlCommand cmd = new SqlCommand(query, con);
            cmd.Parameters.AddWithValue("@ID_DanhMuc", idDanhMuc);
            SqlDataReader rd = cmd.ExecuteReader();
            while (rd.Read())
            {
                Sach s = new Sach
                {
                    ID_Sach = (int)rd["ID_Sach"],
                    TenSach = (string)rd["TenSach"],
                    MoTa = (string)rd["MoTa"],
                    Gia = (decimal)rd["Gia"],
                    SoLuongTon = (int)rd["SoLuongTon"],
                    ID_DanhMuc = (int)rd["ID_DanhMuc"],
                    NgayXuatBan = (DateTime)rd["NgayXuatBan"],
                    Anh = (string)rd["Anh"]
                };
                books.Add(s);
            }
        }
        catch (Exception ex)
        {
            throw new Exception("Error fetching books by danh muc", ex);
        }
        finally
        {
            con.Close();
        }
        return books;
    }
    public List<Sach> GetBestSellingBooks()
    {
        List<Sach> books = new List<Sach>();
        string query = @"
            SELECT TOP 5
                s.ID_Sach,
                s.TenSach,
                s.MoTa,
                s.Gia,
                s.SoLuongTon,
                s.ID_DanhMuc,
                s.NgayXuatBan,
                s.Anh,
                SUM(ct.SoLuong) AS TongSoLuongBan
            FROM Sach s
            INNER JOIN ChiTietGioHang ct ON s.ID_Sach = ct.ID_Sach
            GROUP BY s.ID_Sach, s.TenSach, s.MoTa, s.Gia, s.SoLuongTon, s.ID_DanhMuc, s.NgayXuatBan, s.Anh
            ORDER BY TongSoLuongBan DESC";
        con.Open();
        SqlCommand cmd = new SqlCommand(query, con);
        SqlDataReader rd = cmd.ExecuteReader();
        while (rd.Read())
        {
            Sach s = new Sach
            {
                ID_Sach = rd["ID_Sach"] != DBNull.Value ? (int)rd["ID_Sach"] : 0,
                TenSach = rd["TenSach"] != DBNull.Value ? (string)rd["TenSach"] : string.Empty,
                MoTa = rd["MoTa"] != DBNull.Value ? (string)rd["MoTa"] : string.Empty,
                Gia = rd["Gia"] != DBNull.Value ? (decimal)rd["Gia"] : 0,
                SoLuongTon = rd["SoLuongTon"] != DBNull.Value ? (int)rd["SoLuongTon"] : 0,
                ID_DanhMuc = rd["ID_DanhMuc"] != DBNull.Value ? (int)rd["ID_DanhMuc"] : 0,
                NgayXuatBan = rd["NgayXuatBan"] != DBNull.Value ? (DateTime)rd["NgayXuatBan"] : DateTime.MinValue,
                Anh = rd["Anh"] != DBNull.Value ? (string)rd["Anh"] : string.Empty,
                TongSoLuongBan = (int)rd["TongSoLuongBan"]
            };
            books.Add(s);
        }
        con.Close();
        return books;
    }

    public List<Sach> GetSachMoi()
    {
        List<Sach> news = new List<Sach>();
        string query = @"
        SELECT
            Sach.ID_Sach, 
            Sach.TenSach, 
            Sach.Gia,
            Sach.Anh,
            Sach.NgayXuatBan
        FROM Sach
        WHERE Sach.NgayXuatBan >= '2024-12-01'
        ORDER BY Sach.NgayXuatBan DESC;";

        con.Open();
        SqlCommand cmd = new SqlCommand(query, con);
        SqlDataReader rd = cmd.ExecuteReader();

        while (rd.Read())
        {
            Sach s = new Sach();
            s.ID_Sach = (int)rd["ID_Sach"];
            s.TenSach = (string)rd["TenSach"];
            s.Gia = (decimal)rd["Gia"];
            s.Anh = (string)rd["Anh"];
            news.Add(s);
        }
        con.Close();
        return news;
    }




    public int CreateOrder(int userId, float totalPrice)
    {
        //string query = "INSERT INTO DonHang (ID_User, NgayTao, TongTien, TrangThai) OUTPUT INSERTED.ID_Order VALUES (@ID_User, GETDATE(), @TongTien, 'Đang xử lý')";
        string query = "INSERT INTO DonHang (NgayTao, TongTien, TrangThai, ID_User) OUTPUT INSERTED.ID_Order VALUES (GETDATE(), @TongTien, N'Đang xử lý', @ID_User)";

        con.Open();
        SqlCommand cmd = new SqlCommand(query, con);
        cmd.Parameters.Add("@ID_User", SqlDbType.Int).Value = userId;
        //cmd.Parameters.Add("@TongTien", SqlDbType.Decimal).Value = totalPrice;
        cmd.Parameters.AddWithValue("@TongTien", totalPrice);

        int orderId = (int)cmd.ExecuteScalar();
        con.Close();
        return orderId;
    }

    public void AddOrderDetail(int orderId, int sachId, int soLuong, float gia)
    {


        // Câu truy vấn SQL để thêm chi tiết đơn hàng
        //string query = @"INSERT INTO ChiTietDonHang (ID_DonHang, ID_Sach, SoLuong, GiaBan) 
        //                VALUES (@ID_DonHang, @ID_Sach, @SoLuong, @Gia)";

        //string query = "INSERT INTO DonHang (ID_User, NgayTao, TongTien, TrangThai) OUTPUT INSERTED.ID_Order VALUES (@ID_User, GETDATE(), @TongTien, 'Đang xử lý')";
        string query = @"INSERT INTO ChiTietDonHang (ID_Order, ID_Sach, SoLuong, GiaBan) 
                         VALUES (@ID_DonHang, @ID_Sach, @SoLuong, @Gia)";

        SqlCommand cmd = new SqlCommand(query, con);
        cmd.Parameters.Add("@ID_DonHang", SqlDbType.Int).Value = orderId;
        cmd.Parameters.Add("@ID_Sach", SqlDbType.Int).Value = sachId;
        cmd.Parameters.Add("@SoLuong", SqlDbType.Int).Value = soLuong;
        cmd.Parameters.Add("@Gia", SqlDbType.Float).Value = gia;
        con.Open();

        cmd.ExecuteNonQuery();
        con.Close();

    }

    // Các phương thức khác như CreateOrder, GetCartItems, CreatePayment, UpdateOrderStatus, ClearCart, ...

    public void CreatePayment(int orderId, string paymentMethod, float totalPrice)
    {
        string query = "INSERT INTO ThanhToan (ID_Order, PhuongThuc, TrangThai, NgayThanhToan) VALUES (@ID_Order, @PhuongThuc, 'Đã thanh toán', GETDATE())";

            con.Open();
            SqlCommand cmd = new SqlCommand(query, con);
            cmd.Parameters.Add("@ID_Order", SqlDbType.Int).Value = orderId;
            cmd.Parameters.Add("@PhuongThuc", SqlDbType.NVarChar).Value = paymentMethod;
            cmd.Parameters.Add("@SoTien", SqlDbType.Decimal).Value = totalPrice;
            cmd.ExecuteNonQuery();
            con.Close();
    }

    public void UpdateOrderStatus(int orderId, string status)
    {
        string query = "UPDATE DonHang SET TrangThai = @TrangThai WHERE ID_Order = @ID_Order";

        con.Open();

 
            SqlCommand cmd = new SqlCommand(query, con);
            cmd.Parameters.Add("@TrangThai", SqlDbType.NVarChar).Value = status;
            cmd.Parameters.Add("@ID_Order", SqlDbType.Int).Value = orderId;

            cmd.ExecuteNonQuery();
            con.Close();
 
    }

    public void ClearCart(int userId)
    {
        string query = "DELETE FROM ChiTietGioHang WHERE ID_GioHang = (SELECT ID_GioHang FROM GioHang WHERE ID_User = @ID_User)";

        con.Open();

    
            SqlCommand cmd = new SqlCommand(query, con);
            cmd.Parameters.Add("@ID_User", SqlDbType.Int).Value = userId;

            cmd.ExecuteNonQuery();
            con.Close();
 
    }



}