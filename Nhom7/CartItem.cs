using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Nhom7
{
    public class CartItem
    {
        public int ID_Sach { get; set; }
        public string TenSach { get; set; }
        public decimal Gia { get; set; }
        public int SoLuong { get; set; }
        public string Anh { get; set; }
        public decimal Tong { get; set; }
    }

}
