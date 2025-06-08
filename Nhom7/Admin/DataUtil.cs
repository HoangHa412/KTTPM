using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Web;

namespace Nhom7.Admin
{
    public class DataUtil
    {
        SqlConnection con;

        public DataUtil()
        {
            // Chuỗi kết nối đã được kiểm tra và chỉnh sửa
            String sqlCon = DATABASECONNECT.getConnectionString();
            con = new SqlConnection(sqlCon);
        }

        public List<ThongKe> ThongKeDoanhThuTheoNgay()
        {
            List<ThongKe> dsThongKe = new List<ThongKe>();
            String sql = "SELECT CONVERT(DATE, NgayTao) AS Ngay, SUM(TongTien) AS TongTienBanDuoc FROM DonHang GROUP BY CONVERT(DATE, NgayTao) ORDER BY Ngay";

            try
            {
                con.Open();
                SqlCommand cmd = new SqlCommand(sql, con);
                SqlDataReader rd = cmd.ExecuteReader();

                while (rd.Read())
                {
                    ThongKe tk = new ThongKe();
                    tk.Ngay = (DateTime)rd["Ngay"];
                    tk.TongTienBanDuoc = (double)rd["TongTienBanDuoc"];
                    dsThongKe.Add(tk);
                }
            }
            catch (Exception ex)
            {
                // Log lỗi hoặc hiển thị thông báo lỗi
                throw new Exception("Lỗi khi kết nối đến SQL Server: " + ex.Message);
            }
            finally
            {
                con.Close();
            }

            return dsThongKe;
        }
    }

    public class ThongKe
    {
        public DateTime Ngay { get; set; }
        public double TongTienBanDuoc { get; set; }

        public ThongKe()
        {
            // TODO: Add constructor logic here
        }
    }
}
