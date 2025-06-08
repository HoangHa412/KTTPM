using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Web.UI;
using System.Web.UI.WebControls;
using Nhom7;

namespace Nhom7
{
    public partial class ProductDetail : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                int idSach = 0;
                if (int.TryParse(Request.QueryString["ID_Sach"], out idSach))
                {
                    // Tạo đối tượng DatabaseHelper để lấy thông tin sản phẩm theo ID_Sach
                    DatabaseHelper dbHelper1 = new DatabaseHelper();
                    Sach book = dbHelper1.GetBookById(idSach);
                    List<Sach> bookList = new List<Sach> { book };
                    RepeaterBook.DataSource = bookList; // Liên kết dữ liệu với Repeater
                    RepeaterBook.DataBind();
                }
            }
        }
        protected void btnAddToCart_Click(object sender, EventArgs e)
        {
            Button button = (Button)sender;
            string commandArgument = button.CommandArgument;

            int idSach;
            if (int.TryParse(commandArgument, out idSach))
            {
                DatabaseHelper db = new DatabaseHelper();
                Sach book = db.GetBookById(idSach);

                if (book != null)
                {
                    // Lấy ID_User từ session của người dùng đã đăng nhập
                    int userId = Convert.ToInt32(Session["UserID"]);

                    if (userId > 0)
                    {
                        int cartId;

                        // Kiểm tra xem giỏ hàng đã tồn tại trong cơ sở dữ liệu hay không
                        string checkCartQuery = "SELECT ID_GioHang FROM GioHang WHERE ID_User = @ID_User";
                        SqlCommand checkCartCmd = new SqlCommand(checkCartQuery, db.con);
                        checkCartCmd.Parameters.AddWithValue("@ID_User", userId);

                        db.con.Open();
                        var cartIdResult = checkCartCmd.ExecuteScalar();
                        db.con.Close();

                        // Nếu không tìm thấy giỏ hàng, tạo mới giỏ hàng
                        if (cartIdResult == null)
                        {
                            cartId = db.CreateCart(userId);  // Tạo giỏ hàng mới
                        }
                        else
                        {
                            cartId = Convert.ToInt32(cartIdResult);
                        }

                        // Lưu ID_GioHang vào Session để sử dụng trong các lần thêm sản phẩm sau
                        Session["CartId"] = cartId;

                        db.AddToCart(cartId, book.ID_Sach, 1, (decimal)book.Gia);
                        string script = "alert('Thêm thành công');";
                        ClientScript.RegisterStartupScript(this.GetType(), "UpdateSuccess", script, true);
                    }
                    else
                    {
                        Response.Write("Bạn phải đăng nhập để thêm sản phẩm vào giỏ hàng.");
                    }
                }
            }
            else
            {
                // Xử lý trường hợp CommandArgument không hợp lệ
                Response.Write("ID sách không hợp lệ.");
            }
        }

    }
}
