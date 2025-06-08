using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data.SqlClient;
using System.Diagnostics;
using System.Data;

namespace Nhom7
{
    public partial class HomePage : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            var master = (SitePage)this.Master;
            if (master != null)
            {
                master.SearchButtonClick += Master_SearchButtonClick;
            }

            if (!IsPostBack)
            {
                DatabaseHelper dbHelper = new DatabaseHelper();
                List<Sach> books = dbHelper.GetBooks();
                RepeaterBooks.DataSource = books;
                RepeaterBooks.DataBind();
                TimkiemSP(null);
            }

        }
        private void Master_SearchButtonClick(object sender, EventArgs e)
        {
            var master = (SitePage)this.Master;
            string searchTerm = master.GetSearchTerm();
            TimkiemSP(searchTerm);
        }
        private void TimkiemSP(string searchTerm)
        {
            //string connectionString = ConfigurationManager.ConnectionStrings["YourConnectionString"].ConnectionString;
            string connectionString = DATABASECONNECT.getConnectionString();
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                string query = "SELECT ID_Sach, TenSach, Gia, Anh FROM Sach";
                if (!string.IsNullOrEmpty(searchTerm))
                {
                    query += " WHERE TenSach LIKE @SearchTerm";
                }
                SqlCommand cmd = new SqlCommand(query, conn);
                if (!string.IsNullOrEmpty(searchTerm))
                {
                    cmd.Parameters.AddWithValue("@SearchTerm", "%" + searchTerm + "%");
                }
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                DataTable dt = new DataTable();
                da.Fill(dt);

                RepeaterBooks.DataSource = dt;
                RepeaterBooks.DataBind();

            }

        }
    }
}
