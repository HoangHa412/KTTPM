using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Nhom7
{
    public class User
    {
        public int ID_User { get; set; }              // Mã người dùng
        public string TenNguoiDung { get; set; }       // Tên người dùng
        public string Email { get; set; }              // Email người dùng
        public string MatKhau { get; set; }            // Mật khẩu người dùng
        public string SoDienThoai { get; set; }        // Số điện thoại người dùng
        public string DiaChi { get; set; }             // Địa chỉ người dùng
        public int ID_VaiTro { get; set; }             // Mã vai trò người dùng
    }
}
