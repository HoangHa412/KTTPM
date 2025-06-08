using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using Nhom7;

namespace Nhom7
{
    public class Sach
    {
        public int ID_Sach { get; set; }
        public string TenSach { get; set; }
        public string MoTa { get; set; }
        public decimal Gia { get; set; }
        public int SoLuongTon { get; set; }
        public int ID_DanhMuc { get; set; }
        public string TenDanhMuc { get; set; }
        public DateTime NgayXuatBan { get; set; }
        public string Anh { get; set; }
        public int ID_TacGia { get; set; }
        public string TenTacGia { get; set; }
        public int TongSoLuongBan { get; set; }
    }
}