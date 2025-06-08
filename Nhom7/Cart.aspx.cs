using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7
{
    public partial class Cart : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                LoadCart();
            }
        }

        private void LoadCart()
        {
            // Kiểm tra người dùng đã đăng nhập hay chưa
            if (Session["UserID"] == null)
            {
                lblTotal.Text = "Bạn cần đăng nhập để xem giỏ hàng.";
                lblTotal.CssClass = "error-message success show";
                return;
            }

            int userId = Convert.ToInt32(Session["UserID"]);  // Lấy ID_User từ session (giả sử đã lưu sau khi đăng nhập)

            // Tạo kết nối tới cơ sở dữ liệu và lấy thông tin giỏ hàng
            DatabaseHelper db = new DatabaseHelper();

            // Lấy CartId của người dùng từ cơ sở dữ liệu
            int cartId = db.GetCartIdByUserId(userId);

            // Nếu không có giỏ hàng, thông báo giỏ hàng trống
            if (cartId == 0)
            {
                lblTotal.Text = "Giỏ hàng trống.";
                return;
            }

            // Lấy danh sách các sản phẩm trong giỏ hàng
            List<CartItem> cartItems = db.GetCartItems(cartId);

            // Liên kết dữ liệu với Repeater (rptCart) để hiển thị giỏ hàng
            rptCart.DataSource = cartItems;
            rptCart.DataBind();

            // Tính tổng giá trị giỏ hàng
            decimal total = 0;
            foreach (var item in cartItems)
            {
                total += (decimal)item.Gia * item.SoLuong;
            }

            // Hiển thị tổng giá trị
            lblTotal.Text = total.ToString() + "VND";  
        }

        protected void btnUpdate_Click(object sender, EventArgs e)
        {
            Button btn = (Button)sender;
            int bookId = Convert.ToInt32(btn.CommandArgument);
            int userId = Convert.ToInt32(Session["UserID"]);  // Lấy ID_User từ session (giả sử đã lưu sau khi đăng nhập)

            // Tạo kết nối tới cơ sở dữ liệu và lấy thông tin giỏ hàng
            DatabaseHelper db = new DatabaseHelper();

            // Lấy CartId của người dùng từ cơ sở dữ liệu
            int cartId = db.GetCartIdByUserId(userId);
            TextBox txt = (TextBox)btn.NamingContainer.FindControl("txtQuantity");
            int quantity;
            quantity = Convert.ToInt32(((TextBox)btn.NamingContainer.FindControl("txtQuantity")).Text);


            db.UpdateCartItemQuantity(cartId, bookId, quantity);
            // Load lại giỏ hàng
            LoadCart();
        }
        protected void btnDelete_Click(object sender, EventArgs e)
        {
            Button btn = (Button)sender;
            int bookId = Convert.ToInt32(btn.CommandArgument);
            int userId = Convert.ToInt32(Session["UserID"]);  // Lấy ID_User từ session (giả sử đã lưu sau khi đăng nhập)

            // Tạo kết nối tới cơ sở dữ liệu và lấy thông tin giỏ hàng
            DatabaseHelper db = new DatabaseHelper();

            // Lấy CartId của người dùng từ cơ sở dữ liệu
            int cartId = db.GetCartIdByUserId(userId);

            db.DeleteCartItem(cartId, bookId);

            // Load lại giỏ hàng
            LoadCart();
        }

        protected void btnCheckout_Click(object sender, EventArgs e)
        {
            // Xử lý logic thanh toán ở đây
            Response.Redirect("Checkout.aspx");
        }
    }
}