using System;
using System.Collections.Generic;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Nhom7.Admin
{
    public partial class thongke : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                DataUtil dataUtil = new DataUtil();
                List<ThongKe> dsThongKe = dataUtil.ThongKeDoanhThuTheoNgay();

                gvThongKe.DataSource = dsThongKe;
                gvThongKe.DataBind();
            }
        }
    }
}
