using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7
{
    public partial class VHVN : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                LoadBooksByDanhMuc(1);
            }
        }

        private void LoadBooksByDanhMuc(int idDanhMuc)
        {
            DatabaseHelper dbHelper = new DatabaseHelper();
            List<Sach> books = dbHelper.GetBooksByDanhMuc(idDanhMuc); // Truyền ID_DanhMuc vào
            RepeaterBooks1.DataSource = books;
            RepeaterBooks1.DataBind();
        }
    }
}