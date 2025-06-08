using System;
using System.Collections.Generic;
using System.Web.UI;

namespace Nhom7
{
    public partial class TopBanChay : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                DatabaseHelper dbHelper = new DatabaseHelper();
                List<Sach> books = dbHelper.GetBestSellingBooks();
                RepeaterBooks.DataSource = books;
                RepeaterBooks.DataBind();
            }
        }
    }
}
