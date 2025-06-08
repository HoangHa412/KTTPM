
--ALTER DATABASE sach SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
--drop database demosach3;
--ALTER DATABASE demosach3 SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
--drop database demosach3

create database demosach3;

use demosach3;

-- Bảng Vai Trò
CREATE TABLE VaiTro (
    ID_VaiTro INT PRIMARY KEY IDENTITY,
    TenVaiTro NVARCHAR(50) -- Ví dụ: 'Admin', 'Khách hàng'
);

-- Bảng Người Dùng
CREATE TABLE tbluser (
    ID_User INT PRIMARY KEY IDENTITY,
    TenNguoiDung NVARCHAR(255),
    Email NVARCHAR(255) UNIQUE,
    MatKhau NVARCHAR(255),
    SoDienThoai NVARCHAR(20),
    DiaChi NVARCHAR(MAX),
    ID_VaiTro INT,
    FOREIGN KEY (ID_VaiTro) REFERENCES VaiTro(ID_VaiTro)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- Bảng Danh Mục
CREATE TABLE DanhMuc (
    ID_DanhMuc INT PRIMARY KEY IDENTITY,
    TenDanhMuc NVARCHAR(255)
);

-- Bảng Tác Giả
CREATE TABLE TacGia (
    ID_TacGia INT PRIMARY KEY IDENTITY,
    TenTacGia NVARCHAR(255)
);

-- Bảng Sách
CREATE TABLE Sach (
    ID_Sach INT PRIMARY KEY IDENTITY,
    TenSach NVARCHAR(255),
    MoTa NVARCHAR(MAX),
    Gia decimal,
    SoLuongTon INT,
    ID_DanhMuc INT,
    ID_TacGia INT,
    NgayXuatBan DATETIME,
    Anh NVARCHAR(MAX),
    FOREIGN KEY (ID_DanhMuc) REFERENCES DanhMuc(ID_DanhMuc)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    FOREIGN KEY (ID_TacGia) REFERENCES TacGia(ID_TacGia)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- Bảng Đơn Hàng
CREATE TABLE DonHang (
    ID_Order INT PRIMARY KEY IDENTITY,
    NgayTao DATETIME,
    ID_User INT,
    TongTien FLOAT,
    TrangThai NVARCHAR(50), -- Ví dụ: 'Đang xử lý', 'Đã giao', 'Đã hủy'
    FOREIGN KEY (ID_User) REFERENCES tbluser(ID_User)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);
ALTER TABLE DonHang
ALTER COLUMN TongTien DECIMAL(18, 2);

-- Bảng Thanh Toán
CREATE TABLE ThanhToan (
    ID_ThanhToan INT PRIMARY KEY IDENTITY,
    ID_Order INT,
    PhuongThuc NVARCHAR(50), -- Ví dụ: 'Tiền mặt', 'Thẻ tín dụng', 'Ví điện tử'
    TrangThai NVARCHAR(50), -- Ví dụ: 'Đã thanh toán', 'Chưa thanh toán'
    NgayThanhToan DATETIME,
    FOREIGN KEY (ID_Order) REFERENCES DonHang(ID_Order)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);
--DROP TABLE DonHang;

-- Bảng Chi Tiết Đơn Hàng
CREATE TABLE ChiTietDonHang (
    ID_ChiTiet INT PRIMARY KEY IDENTITY,
    ID_Order INT,
    ID_Sach INT,
    SoLuong INT,
    GiaBan FLOAT,
    FOREIGN KEY (ID_Order) REFERENCES DonHang(ID_Order)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    FOREIGN KEY (ID_Sach) REFERENCES Sach(ID_Sach)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

-- Bảng Giỏ Hàng
CREATE TABLE GioHang (
    ID_GioHang INT PRIMARY KEY IDENTITY,
    ID_User INT,
    NgayTao DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ID_User) REFERENCES tbluser(ID_User)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);
ALTER TABLE ThanhToan DROP CONSTRAINT FK__ThanhToan__ID_Or__47DBAE45;

-- Bảng Chi Tiết Giỏ Hàng
CREATE TABLE ChiTietGioHang (
    ID_ChiTietGioHang INT PRIMARY KEY IDENTITY,
    ID_GioHang INT,
    ID_Sach INT,
    SoLuong INT,
    Gia FLOAT,
    FOREIGN KEY (ID_GioHang) REFERENCES GioHang(ID_GioHang)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    FOREIGN KEY (ID_Sach) REFERENCES Sach(ID_Sach)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


--them
-- Bật IDENTITY_INSERT cho bảng VaiTro
SET IDENTITY_INSERT VaiTro ON;

-- Chèn dữ liệu vào bảng VaiTro
INSERT INTO VaiTro (ID_VaiTro, TenVaiTro)
VALUES 
(1, N'admin'),
(2, N'customer');

-- Tắt IDENTITY_INSERT sau khi chèn xong
SET IDENTITY_INSERT VaiTro OFF;

-- Chèn dữ liệu vào bảng User với vai trò phù hợp
INSERT INTO tbluser (TenNguoiDung, MatKhau, Email, SoDienThoai, DiaChi, ID_VaiTro)
VALUES 
('admin', '123', 'admin@example.com', '0123456789', 'Hà Nội', 1),  -- Quản trị viên
('khachhang01', 'password123', 'khachhang01@example.com', '0987654321', 'TP. Hồ Chí Minh', 2);  -- Khách hàng

SELECT * FROM VaiTro;  -- Xem các vai trò
SELECT * FROM tbluser;   -- Xem các người dùng

INSERT INTO TacGia ( TenTacGia)
VALUES 
(N'Nguyễn Nhật Ánh'),
(N'J.K. Rowling'),
(N'George Orwell');

INSERT INTO DanhMuc ( TenDanhMuc)
VALUES 
(N'Văn học Việt Nam'),
(N'Văn học nước ngoài'),
(N'Khoa học viễn tưởng'),
(N'Sách thiếu nhi');


INSERT INTO Sach ( TenSach, MoTa, Gia, SoLuongTon, ID_DanhMuc, NgayXuatBan, Anh, ID_TacGia)
VALUES 
(N'Cho Tôi Xin Một Vé Đi Tuổi Thơ', N'Cuốn sách gợi nhớ về tuổi thơ của mỗi người', 80000, 50, 1, '2023-12-17', 'https://upload.wikimedia.org/wikipedia/vi/c/c9/Cho_t%C3%B4i_xin_m%E1%BB%99t_v%C3%A9_%C4%91i_tu%E1%BB%95i_th%C6%A1.jpg',1),
(N'Harry Potter và Hòn Đá Phù Thủy', N'Phần đầu tiên của series Harry Potter', 120000, 30, 2, '2023-12-17', 'https://www.nxbtre.com.vn/Images/Book/nxbtre_full_21542017_035423.jpg',2),
(N'Kẻ cắp tia chớp', N'Khoa học viễn tưởng', 90000, 20, 3, '2024-12-17', 'https://gcs.tripi.vn/public-tripi/tripi-feed/img/475218DNt/anh-mo-ta.png',1),
(N'Những Người Bạn', N'Cuốn sách về tình bạn và sự sẻ chia.', 95000, 40, 1, '2022-12-17', 'https://product.hstatic.net/200000343865/product/nhung-nguoi-ban_bia-cung_0_91eafad19cb54708968eb37a707296ce_grande.jpg',1),
(N'Chuyện Cổ Tích', N'Sách kể về những câu chuyện cổ tích nổi tiếng thế giới.', 80000, 60, 1, '2019-12-17', 'https://product.hstatic.net/1000237375/product/bia_1_409d2c70893a478cac94c2a96f49c057_master.jpg',2),
(N'Những Cuộc Phiêu Lưu Của Tom SawYer', N'Một cuốn sách đầy những câu chuyện phiêu lưu kỳ thú.', 110000, 25, 2, '2019-12-17', 'https://bizweb.dktcdn.net/100/468/166/products/cuoc-phieu-luu-cua-tom-sawyer-bia-5e3827f6813a4327ac142e04dbd51873-master.jpg?v=1671722301300',2),
(N'Sống Cùng Nước', N'Khám phá những sự kiện lịch sử đã hình thành thế giới ngày nay.', 130000, 20, 1, '2019-12-17', 'https://thuvien.tayninh.gov.vn/News/DisplayImage/?itemID=8575',2),
(N'Phòng Trọ Ba Người', N'Một câu chuyện về tình bạn, kỷ niệm và những điều giản dị trong cuộc sống.', 110000, 50, 1, '2004-12-17', 'https://tuyenchonsachhay.com/wp-content/uploads/2019/02/phong-tro-ba-nguoi.jpg',2),
(N'Gửi Ngày Mai Một Lời Chào', N'Một câu chuyện về tình yêu và hy vọng.', 110000, 35, 1, '2004-12-17', 'https://cdn0.fahasa.com/media/catalog/product/b/_/b_a-1-1_2.jpg',3),
(N'Triết Học Cổ Đại', N'Cuốn sách giới thiệu về các triết lý và tư tưởng của các nhà triết học nổi tiếng.', 130000, 60, 2, '2020-12-17', 'https://www.nxbctqg.org.vn/img_data/images/images/triet%20hoc%20co%20dai.JPG',3),
(N'Mỹ Thuật Đông Dương', N'Tìm hiểu về các tác phẩm nghệ thuật nổi tiếng.', 120000, 10, 2, '2002-12-17', 'https://pos.nvncdn.com/d8267c-94460/ps/20220526_Cim5JRccXQfCbi6jpLBpdiNF.png',3),
(N'Cái Chết Huy Hoàng', N'Khám phá thế giới tuyệt vời qua lăng kính văn học.', 98000, 55, 2, '2002-12-17', 'https://thesaigontimes.vn/Uploads/Articles/59363/614e3_cai-ch-t-huy-hoang.jpg',3),
(N'Khi Nào Tôi Lớn', N'Sách về những trăn trở và khó khăn trong tuổi trưởng thành.', 95000, 45, 1, '2000-12-17', 'https://cdn0.fahasa.com/media/catalog/product/8/9/8936203361957.jpg',1),
(N'Muôn Màu Cuộc Sống', N'Sách về những cung bậc cảm xúc trong cuộc sống hàng ngày.', 100000, 40, 1, '2024-12-17', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCtp2rUsattySDFjmWpvt3PIPCDuTCgnhSlw&s',1),
(N'Cây Cam Ngọt Của Tôi', N'Sách về những người bạn không ngờ lại là một phần quan trọng trong cuộc sống.', 100000, 30, 2, '2024-12-21', 'https://img.tripi.vn/cdn-cgi/image/width=700,height=700/https://gcs.tripi.vn/public-tripi/tripi-feed/img/473860xJr/cay-cam-ngot-cua-toi-1284347.jpg',2),
(N'Trăm năm cô đơn', N'Tiểu thuyết nước ngoài hay nhất mọi thời đại', 100000, 30, 2, '2024-12-17', 'https://book365.vn/upload/iblock/a0f/a0fd2b7a21520b8fa01acc633f3546cf.jpeg',2),
(N'Hai vạn dặm dưới biển', N'Sách về những người bạn không ngờ lại là một phần quan trọng trong cuộc sống.', 850000, 30, 2, '2024-12-25', 'https://product.hstatic.net/1000237375/product/bia_truoc_hvd_6176fe6221aa47a4a757825fc2da1e13_large.jpg',2),
(N'Chuyện Kỳ Dị Về Benjamin', N'Cuộc hành trình xuyên qua thời gian, lịch sử và các nền văn minh.', 125000, 45, 2, '2024-12-17', 'https://bizweb.dktcdn.net/100/180/408/products/chuyen-ky-di-ve-benjamin-jpeg.jpg?v=1657207308340',2),
(N'Tôi thấy hoa vàng trên cỏ xanh', N'Tôi thấy hoa vàng trên cỏ xanh một cuốn sách được chuyển thể thành bộ phim cùng tên của tác giả Nguyễn Nhật Ánh đã cho ta sống lại trong những cảm xúc, suy nghĩ vô ưu vô tư qua các câu chuyện xoay quanh nhân vật Thiều, Tường, Mận,... Giúp ta như được trở về những ngày vô lo, vô nghĩ, sống thật với cảm xúc của mình mà không ngần ngại kia đáng quý biết bao. Nhưng cớ sao quãng thời gian đó ta chỉ ước mình mau chóng lớn thật nhanh để làm “người lớn” với vô vàn những khó khăn mà cuộc sống đặt lên vai.i', 90000, 40, 1, '2024-12-17', 'https://www.nxbtre.com.vn/Images/Book/NXBTreStoryFull_02482010_104821.jpg',1),
(N'Quái Vật Hồ Loch Ness', N'Khám phá những sinh vật huyền bí trong văn hóa dân gian và thần thoại.', 95000, 30, 3, '2001-12-17', 'https://cdnvg.scandict.com/pictures/fullsize/2013/05/30/ejq1369931861.jpg',1),
(N'Âm Mưu Cấu Kết', N'Một câu chuyện về sự lừa dối và âm mưu trong một gia đình.', 85000, 20, 3, '2020-12-17', 'https://cdn0.fahasa.com/media/catalog/product/8/9/8935235233362.jpg',1),
(N'Thế Giới Là Một Giấc Mơ', N'Sách về sự tưởng tượng và những điều kỳ diệu trong cuộc sống.', 105000, 40, 3, '2024-12-19', 'https://down-vn.img.susercontent.com/file/vn-11134207-7r98o-lthj12qgnrbh42',1),
(N'Đấu Trường Sinh Tử', N'Câu chuyện về cuộc chiến sinh tồn trong tương lai đầy khắc nghiệt.', 150000, 50, 3, '2024-12-18', 'https://cdn0.fahasa.com/media/catalog/product/i/m/image_172953.jpg',2),
(N'Dune: Hành Tinh Cát', N'Một trong những tiểu thuyết khoa học viễn tưởng kinh điển nhất mọi thời đại.', 180000, 35, 3, '2024-12-19', 'https://cdn0.fahasa.com/media/catalog/product/x/u/xu-cat---600.jpg',2),
(N'Trạm Không Gian', N'Một câu chuyện khoa học viễn tưởng về cuộc sống ngoài không gian.', 110000, 25, 3, '2024-12-18', 'https://bizweb.dktcdn.net/thumb/1024x1024/100/362/945/products/f6eba92871fc18485632afa6ce46a6.jpg?v=1617001338450',2),
(N'Kỷ Nguyên Máy Móc', N'Cuốn sách về sự nổi dậy của AI và những hệ quả đối với nhân loại.', 170000, 30, 3, '2024-12-25', 'https://cdn0.fahasa.com/media/catalog/product/8/9/8935251419528.jpg',3),
(N'Vùng Đất Câm Lặng', N'Cuộc chiến sinh tồn trong một thế giới nơi âm thanh có thể giết chết.', 120000, 27, 3, '2005-12-18', 'https://upload.wikimedia.org/wikipedia/vi/e/e0/A_Quiet_Place_poster.jpg',3),
(N'Hoàng Tử Bé', N'Câu chuyện cảm động về cậu bé từ một hành tinh xa xôi và bài học cuộc sống.', 90000, 50, 4, '2006-12-18', 'https://product.hstatic.net/200000343865/product/hoang-tu-be---tb-2022_f0f2f9b813c246c4878e7e685f683d50_5b46a794d64c4996a6695f6e9e8d3213.jpg',2),
(N'Cây Táo Yêu Thương', N'Câu chuyện xúc động về tình yêu thương vô điều kiện của cây táo.', 75000, 45, 4, '2007-12-18', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR20psn07DGsFk0d0HiUrxINWNUsfPKyMpkYg&s',1),
(N'Dế Mèn Phiêu Lưu Ký', N'Cuốn sách gắn liền với tuổi thơ, kể về cuộc phiêu lưu của chú dế mèn.', 85000, 60, 4, '2024-12-18', 'https://bavi.edu.vn/upload/21768/fck/files/150800018_3868030666550251_8375198552020103317_n.jpg',2),
(N'Chú Bé Rắc Rối', N'Câu chuyện hài hước về cậu bé với những trò nghịch ngợm đáng yêu.', 70000, 40, 4, '2024-11-18', 'https://www.nxbtre.com.vn/Images/Book/copy_21_NXBTreStoryFull_08072014_110754.jpg',3),
(N'Mèo Đi Hia', N'Câu chuyện cổ tích nổi tiếng về chú mèo thông minh và dũng cảm.', 80000, 30, 4, '2024-11-30', 'https://product.hstatic.net/200000017360/product/chumeodihia_c3687eee6b5d46a1bcb62608dca48024.jpg',3),
(N'Cậu Bé Người Gỗ Pinocchio', N'Hành trình trở thành một cậu bé thật thà và dũng cảm của Pinocchio.', 88000, 50, 4, '2020-12-18', 'https://dinhtibooks.com.vn/images/products/2023/05/23/large/piocchino_1684826484.webp',2),
(N'Nghìn Lẻ Một Đêm', N'Tuyển tập truyện cổ tích huyền thoại đầy kỳ ảo và hấp dẫn.', 95000, 35, 4, '2022-12-18', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSa9Fl6QZ2fbNIZPjsntxAZcL-ALPAcmhXnbQ&s',1),
(N'Bạch Tuyết Và Bảy Chú Lùn', N'Câu chuyện cổ tích kinh điển về công chúa Bạch Tuyết và cuộc phiêu lưu của cô.', 72000, 25, 4, '2024-12-18', 'https://bizweb.dktcdn.net/100/370/339/products/nang-bach-tuyet.jpg?v=1582693289777',1),
(N'Alice Ở Xứ Sở Thần Tiên', N'Hành trình kỳ lạ của Alice trong một thế giới thần tiên đầy màu sắc.', 93000, 38, 4, '2024-12-25', 'https://www.nxbtre.com.vn/Images/Book/nxbtre_full_28402016_104013.jpg',2);


INSERT INTO DonHang (NgayTao, TongTien, TrangThai, ID_User)
VALUES 
('2024-12-20', 1200000, N'Đang xử lý', 2),
('2024-12-20', 2500000, N'Đang xử lý', 2),
('2024-12-21', 1050000, N'Đang xử lý', 2),
('2024-12-21', 900000, N'Đã giao', 2),
('2024-12-22', 300000, N'Đã giao', 2),
('2024-12-22', 1800000, N'Đang xử lý', 2),
('2024-12-23', 500000, N'Đang xử lý', 2),
('2024-12-23', 1400000, N'Đã giao', 2),
('2024-12-24', 2200000, N'Đã giao', 2),
('2024-12-24', 1300000, N'Đang xử lý', 2),
('2024-12-25', 1700000, N'Đang xử lý', 2),
('2024-12-25', 750000, N'Đã hủy', 2),
('2024-12-26', 800000, N'Đang xử lý', 2),
('2024-12-26', 1900000, N'Đã giao', 2),
('2024-12-27', 1350000, N'Đang xử lý', 2),
('2024-12-27', 2000000, N'Đã giao', 2),
('2024-12-28', 1500000, N'Đang xử lý', 2),
('2024-12-28', 1100000, N'Đang xử lý', 2),
('2024-12-29', 2100000, N'Đã giao', 2),
('2024-12-29', 2200000, N'Đang xử lý', 2);
INSERT INTO ChiTietDonHang (ID_Order, ID_Sach, SoLuong, GiaBan)
VALUES 
(1, 3, 2, 80000), -- Cho Tôi Xin Một Vé Đi Tuổi Thơ
(1, 2, 3, 120000),  -- Harry Potter và Hòn Đá Phù Thủy
(1, 3, 1, 90000),  -- Kẻ cắp tia chớp
(2, 4, 4, 95000),  -- Những Người Bạn
(2, 5, 2, 80000),  -- Chuyện Cổ Tích
(2, 6, 2, 110000), -- Những Cuộc Phiêu Lưu Của Tom Sawyer
(3, 1, 2, 80000),
(3, 2, 1, 120000),
(3, 3, 3, 90000),
(4, 4, 2, 95000),
(4, 5, 3, 80000),
(4, 6, 2, 110000),
(5, 7, 3, 130000),  -- Sống Cùng Nước
(5, 8, 2, 110000),  -- Phòng Trọ Ba Người
(5, 9, 1, 130000),  -- Triết Học Cổ Đại
(6, 10, 4, 95000),  -- Quái Vật Hồ Loch Ness
(6, 11, 3, 85000),  -- Âm Mưu Cấu Kết
(7, 12, 2, 95000),  -- Thế Giới Là Một Giấc Mơ
(7, 13, 2, 105000),  -- Đấu Trường Sinh Tử
(8, 14, 3, 120000),  -- Dune: Hành Tinh Cát
(8, 15, 1, 170000),  -- Trạm Không Gian
(9, 16, 2, 130000),  -- Kỷ Nguyên Máy Móc
(9, 17, 2, 120000),  -- Vùng Đất Câm Lặng
(10, 18, 1, 90000),  -- Hoàng Tử Bé
(10, 19, 3, 75000),  -- Cây Táo Yêu Thương
(10, 20, 4, 85000);  -- Dế Mèn Phiêu Lưu Ký

SELECT * FROM tbluser;
select * from Sach;
SELECT * FROM DonHang;
SELECT * FROM ChiTietDonHang;
SELECT SUM(Gia * SoLuong) AS TotalPrice FROM ChiTietGioHang WHERE ID_GioHang = 1;
ALTER TABLE DonHang
ALTER COLUMN TongTien FLOAT;

SELECT TOP 5
                s.ID_Sach,
                s.TenSach,
                s.MoTa,
                s.Gia,
                s.SoLuongTon,
                s.ID_DanhMuc,
                s.NgayXuatBan,
                s.Anh,
                SUM(ct.SoLuong) AS TongSoLuongBan
            FROM Sach s
            INNER JOIN ChiTietGioHang ct ON s.ID_Sach = ct.ID_Sach
            GROUP BY s.ID_Sach, s.TenSach, s.MoTa, s.Gia, s.SoLuongTon, s.ID_DanhMuc, s.NgayXuatBan, s.Anh
            ORDER BY TongSoLuongBan DESC
        SELECT 
            Sach.ID_Sach, 
            Sach.TenSach, 
            Sach.MoTa, 
            Sach.Gia, 
            Sach.SoLuongTon, 
            Sach.NgayXuatBan, 
            Sach.Anh, 
            TacGia.TenTacGia, 
            DanhMuc.TenDanhMuc
        FROM Sach
        INNER JOIN TacGia ON Sach.ID_TacGia = TacGia.ID_TacGia
        INNER JOIN DanhMuc ON Sach.ID_DanhMuc = DanhMuc.ID_DanhMuc
        WHERE Sach.ID_Sach = ID_Sach

SELECT TOP 9
    Sach.ID_Sach, 
    Sach.TenSach, 
    SUM(ChiTietDonHang.SoLuong) AS TongSoLuongBan
FROM ChiTietDonHang
INNER JOIN Sach ON ChiTietDonHang.ID_Sach = Sach.ID_Sach
GROUP BY Sach.ID_Sach, Sach.TenSach
ORDER BY TongSoLuongBan DESC;

SELECT
    Sach.ID_Sach, 
    Sach.TenSach, 
    Sach.Gia,
    Sach.Anh,
    Sach.NgayXuatBan
FROM Sach
WHERE Sach.NgayXuatBan >= '2024-12-01'
ORDER BY Sach.NgayXuatBan DESC;

SELECT 
    u.ID_User,
    u.TenNguoiDung,
    u.Email,
    u.SoDienThoai,
    u.DiaChi,
    COUNT(dh.ID_Order) AS SoLuongDonHang
FROM 
    tbluser u
LEFT JOIN 
    DonHang dh ON u.ID_User = dh.ID_User
WHERE 
    u.ID_Vaitro = 2
GROUP BY 
    u.ID_User, u.TenNguoiDung, u.Email, u.SoDienThoai, u.DiaChi;

ALTER TABLE ChiTietGioHang
ADD TrangThai NVARCHAR(50) DEFAULT 'Active';

SELECT NgayTao, TongTien, TrangThai 
FROM DonHang 
WHERE ID_User = ID_User 
AND (TrangThai = 'Đã giao' OR TrangThai = 'Đã hủy')

SELECT 
                    u.ID_User,
                    u.TenNguoiDung,
                    u.Email,
                    u.MatKhau,
                    u.SoDienThoai,
                    u.DiaChi,
                    COUNT(dh.ID_Order) AS SoDonMua
                FROM 
                    tbluser u
                LEFT JOIN 
                    DonHang dh ON u.ID_User = dh.ID_User
                WHERE 
                    u.ID_Vaitro = 2
                GROUP BY 
                    u.ID_User, 
                    u.TenNguoiDung, 
                    u.Email, 
                    u.MatKhau,
                    u.SoDienThoai, 
                    u.DiaChi;

SELECT TOP 9
    Sach.ID_Sach, 
    Sach.TenSach, 
    MAX(Sach.Gia) AS Gia,
    MAX(Sach.Anh) AS Anh,
    SUM(ChiTietDonHang.SoLuong) AS TongSoLuongBan
FROM ChiTietDonHang
INNER JOIN Sach ON ChiTietDonHang.ID_Sach = Sach.ID_Sach
GROUP BY Sach.ID_Sach, Sach.TenSach
ORDER BY TongSoLuongBan DESC