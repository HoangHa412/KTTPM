using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7.Admin
{
    public partial class Admin : System.Web.UI.MasterPage
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (Session["UserID"] == null || Session["Role"] == null)
            {
                // Nếu chưa đăng nhập, chuyển hướng đến trang đăng nhập
                Response.Redirect("~/Login.aspx");
            }
            else
            {
                // Người dùng đã đăng nhập, hiển thị thông tin hoặc tiếp tục xử lý
                lblMessage.Text = "Chào mừng";
            }
        }
        protected void btnLogout_Click(object sender, EventArgs e)
        {
            // Xóa các session
            Session["UserID"] = null;
            Session["Role"] = null;

            // Chuyển hướng  đến trang đăng nhập
            Response.Redirect("~/Login.aspx");
        }
    }
}