using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7
{
    public partial class SachMoi : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                DatabaseHelper dbHelper = new DatabaseHelper();
                List<Sach> newbooks = dbHelper.GetSachMoi();
                RepeaterBooks.DataSource = newbooks;
                RepeaterBooks.DataBind();
            }

        }
    }
}
