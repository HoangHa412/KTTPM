using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7
{
    public partial class STN : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                LoadBooksByDanhMuc(4);
            }
        }

        private void LoadBooksByDanhMuc(int idDanhMuc)
        {
            DatabaseHelper dbHelper = new DatabaseHelper();
            List<Sach> books = dbHelper.GetBooksByDanhMuc(idDanhMuc);
            RepeaterBooks1.DataSource = books;
            RepeaterBooks1.DataBind();
        }
    }
}