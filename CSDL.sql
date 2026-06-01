CREATE DATABASE QuanLyNhanSu;
use QuanLyNhanSu;

CREATE TABLE CuaHang (
    MaCuaHang VARCHAR(10) PRIMARY KEY,
    TenCuaHang VARCHAR(100),
    DiaChi VARCHAR(255),
    SoDienThoai VARCHAR(10)
);

INSERT INTO CuaHang
VALUES ("CH01", "KTX DHQG", "Đông Hòa, Dĩ An, Bình Dương", "0123456789");

SELECT * FROM CuaHang;

CREATE TABLE ChucVu (
    MaChucVu VARCHAR(10) PRIMARY KEY,
    TenChucVu VARCHAR(50),
    HeSoLuong FLOAT
);

INSERT INTO ChucVu VALUES
('CV01', 'Pha chế', 1.2),
('CV02', 'Thu ngân', 1.0),
('CV03', 'Quản lý', 2.0);

SELECT * FROM ChucVu;

CREATE TABLE NhanVien (
    MaNhanVien VARCHAR(10) PRIMARY KEY,
    HoTen VARCHAR(100),
    GioiTinh ENUM('Nam', 'Nu', 'Khac'),
    NgaySinh DATE,
    SoDienThoai VARCHAR(15),
    Email VARCHAR(100),
    DiaChi VARCHAR(255),
    NgayVaoLam DATE,
    MaCuaHang VARCHAR(10),
    MaChucVu VARCHAR(10),
    FOREIGN KEY (MaCuaHang) REFERENCES CuaHang(MaCuaHang),
    FOREIGN KEY (MaChucVu) REFERENCES ChucVu(MaChucVu)
);

INSERT INTO NhanVien VALUES
('NV01', 'Nguyen Minh Tu', 'Nam', '1997-12-01', '0909123456', 'a@gmail.com', 'Q1, HCM', '2020-05-12', 'CH01', 'CV03'),
('NV02', 'Tran Thi Bich Ngoc', 'Nu', '2005-5-23', '0911123456', 'b@gmail.com', 'Q3, HCM', '2024-08-11', 'CH01', 'CV02'),
('NV03', 'Nguyen Tu Anh', 'Nam', '2006-02-18','095095441','c@gmail.com','Q12, HCM', '2024-05-01','CH01','CV01'),
('NV04', 'Pham Thi Ngoc Ha', 'Nu', '2004-07-10','0967492644','d@gmail.com','Q5, HCM', '2024-08-15','CH01','CV01'),
('NV05', 'Pham Minh Khoi ', 'Nam', '2004-03-17','0967768644','e@gmail.com','Q5, HCM', '2024-08-15','CH01','CV01'),
('NV06', 'Pham Thi Hai Thy ', 'Nu', '2002-04-12','0967434984','f@gmail.com','ThuDuc, HCM', '2023-03-16','CH01','CV02');

CREATE TABLE CaLam (
    MaCa VARCHAR(10) PRIMARY KEY,
    TenCa VARCHAR(50),
    GioBatDau TIME,
    GioKetThuc TIME
);

INSERT INTO CaLam VALUES
('CA01', 'Ca sáng', '06:00', '12:00'),
('CA02', 'Ca chiều', '12:00', '18:00'),
('CA03', 'Ca tối', '18:00', '22:00');

CREATE TABLE Luong (
    MaLuong INT AUTO_INCREMENT PRIMARY KEY,
    MaNhanVien VARCHAR(10),
    Thang INT CHECK (Thang >= 1 AND Thang <= 12),
    Nam INT,
    LuongCoBan DECIMAL(15,2),
    PhuCap DECIMAL(15,2),
    SoNgayCong INT,
    GhiChu TEXT,
    FOREIGN KEY (MaNhanVien) REFERENCES NhanVien(MaNhanVien)
);

INSERT INTO Luong (MaNhanVien, Thang, Nam, LuongCoBan, PhuCap, SoNgayCong, GhiChu) VALUES
('NV01', 4, 2025, 6000000.00, 600000.00, 22, 'Lương tháng 4/2025 cho Nguyen Minh Tu'),
('NV02', 4, 2025, 4500000.00, 450000.00, 20, 'Lương tháng 4/2025 cho Tran Thi Bich Ngoc'),
('NV03', 4, 2025, 5000000.00, 500000.00, 20, 'Lương tháng 4/2025 cho Nguyen Tu Anh'),
('NV04', 4, 2025, 5000000.00, 500000.00, 22, 'Lương tháng 4/2025 cho Pham Thi Ngoc Ha'),
('NV05', 4, 2025, 5000000.00, 500000.00, 21, 'Lương tháng 4/2025 cho Pham Minh Khoi'),
('NV06', 4, 2025, 4500000.00, 450000.00, 21, 'Lương tháng 4/2025 cho Pham Thi Hai Thy');

CREATE TABLE ChamCong (
    MaChamCong INT AUTO_INCREMENT PRIMARY KEY,
    MaNhanVien VARCHAR(10),
    Ngay DATE,
    MaCa VARCHAR(10),
    TrangThai ENUM('Co mat', 'Vang', 'Nghi phep'),
    FOREIGN KEY (MaNhanVien) REFERENCES NhanVien(MaNhanVien),
    FOREIGN KEY (MaCa) REFERENCES CaLam(MaCa)
);

INSERT INTO ChamCong (MaNhanVien, Ngay, MaCa, TrangThai) VALUES
('NV01', '2025-04-01', 'CA01', 'Có mặt'), ('NV01', '2025-04-02', 'CA02', 'Có mặt'),
('NV01', '2025-04-03', 'CA03', 'Có mặt'), ('NV01', '2025-04-04', 'CA01', 'Có mặt'),
('NV01', '2025-04-05', 'CA02', 'Có mặt'), ('NV01', '2025-04-08', 'CA03', 'Có mặt'),
('NV01', '2025-04-09', 'CA01', 'Có mặt'), ('NV01', '2025-04-10', 'CA02', 'Có mặt'),
('NV01', '2025-04-11', 'CA03', 'Có mặt'), ('NV01', '2025-04-12', 'CA01', 'Có mặt'),
('NV01', '2025-04-15', 'CA02', 'Có mặt'), ('NV01', '2025-04-16', 'CA03', 'Có mặt'),
('NV01', '2025-04-17', 'CA01', 'Có mặt'), ('NV01', '2025-04-18', 'CA02', 'Có mặt'),
('NV01', '2025-04-19', 'CA03', 'Có mặt'), ('NV01', '2025-04-22', 'CA01', 'Có mặt'),
('NV01', '2025-04-23', 'CA02', 'Có mặt'), ('NV01', '2025-04-24', 'CA03', 'Có mặt'),
('NV01', '2025-04-25', 'CA01', 'Có mặt'), ('NV01', '2025-04-26', 'CA02', 'Có mặt'),
('NV01', '2025-04-29', 'CA01', 'Có mặt'), ('NV01', '2025-04-30', 'CA03', 'Có mặt'),

('NV02', '2025-04-01', 'CA02', 'Có mặt'), ('NV02', '2025-04-02', 'CA01', 'Có mặt'),
('NV02', '2025-04-03', 'CA03', 'Có mặt'), ('NV02', '2025-04-04', 'CA02', 'Có mặt'),
('NV02', '2025-04-05', 'CA01', 'Có mặt'), ('NV02', '2025-04-08', 'CA03', 'Có mặt'),
('NV02', '2025-04-09', 'CA02', 'Có mặt'), ('NV02', '2025-04-10', 'CA01', 'Có mặt'),
('NV02', '2025-04-11', 'CA03', 'Có mặt'), ('NV02', '2025-04-12', 'CA02', 'Có mặt'),
('NV02', '2025-04-15', 'CA01', 'Có mặt'), ('NV02', '2025-04-16', 'CA03', 'Có mặt'),
('NV02', '2025-04-17', 'CA02', 'Có mặt'), ('NV02', '2025-04-18', 'CA01', 'Có mặt'),
('NV02', '2025-04-19', 'CA03', 'Có mặt'), ('NV02', '2025-04-22', 'CA02', 'Có mặt'),
('NV02', '2025-04-23', 'CA01', 'Có mặt'), ('NV02', '2025-04-24', 'CA03', 'Có mặt'),
('NV02', '2025-04-25', 'CA02', 'Có mặt'), ('NV02', '2025-04-26', 'CA01', 'Có mặt'),

('NV03', '2025-04-01', 'CA01', 'Có mặt'), ('NV03', '2025-04-02', 'CA01', 'Có mặt'),
('NV03', '2025-04-03', 'CA02', 'Có mặt'), ('NV03', '2025-04-04', 'CA02', 'Có mặt'),
('NV03', '2025-04-05', 'CA03', 'Có mặt'), ('NV03', '2025-04-08', 'CA01', 'Có mặt'),
('NV03', '2025-04-09', 'CA01', 'Có mặt'), ('NV03', '2025-04-10', 'CA02', 'Có mặt'),
('NV03', '2025-04-11', 'CA02', 'Có mặt'), ('NV03', '2025-04-12', 'CA03', 'Có mặt'),
('NV03', '2025-04-15', 'CA01', 'Có mặt'), ('NV03', '2025-04-16', 'CA01', 'Có mặt'),
('NV03', '2025-04-17', 'CA02', 'Có mặt'), ('NV03', '2025-04-18', 'CA02', 'Có mặt'),
('NV03', '2025-04-19', 'CA03', 'Có mặt'), ('NV03', '2025-04-22', 'CA01', 'Có mặt'),
('NV03', '2025-04-23', 'CA02', 'Có mặt'), ('NV03', '2025-04-24', 'CA03', 'Có mặt'),
('NV03', '2025-04-25', 'CA01', 'Có mặt'), ('NV03', '2025-04-26', 'CA02', 'Có mặt'),

('NV04', '2025-04-01', 'CA02', 'Có mặt'), ('NV04', '2025-04-02', 'CA01', 'Có mặt'),
('NV04', '2025-04-03', 'CA03', 'Có mặt'), ('NV04', '2025-04-04', 'CA02', 'Có mặt'),
('NV04', '2025-04-05', 'CA01', 'Có mặt'), ('NV04', '2025-04-08', 'CA03', 'Có mặt'),
('NV04', '2025-04-09', 'CA02', 'Có mặt'), ('NV04', '2025-04-10', 'CA01', 'Có mặt'),
('NV04', '2025-04-11', 'CA03', 'Có mặt'), ('NV04', '2025-04-12', 'CA02', 'Có mặt'),
('NV04', '2025-04-15', 'CA01', 'Có mặt'), ('NV04', '2025-04-16', 'CA03', 'Có mặt'),
('NV04', '2025-04-17', 'CA02', 'Có mặt'), ('NV04', '2025-04-18', 'CA01', 'Có mặt'),
('NV04', '2025-04-19', 'CA03', 'Có mặt'), ('NV04', '2025-04-22', 'CA02', 'Có mặt'),
('NV04', '2025-04-23', 'CA01', 'Có mặt'), ('NV04', '2025-04-24', 'CA03', 'Có mặt'),
('NV04', '2025-04-25', 'CA02', 'Có mặt'), ('NV04', '2025-04-26', 'CA01', 'Có mặt'),
('NV04', '2025-04-29', 'CA03', 'Có mặt'), ('NV04', '2025-04-30', 'CA02', 'Có mặt'),

('NV05', '2025-04-01', 'CA01', 'Có mặt'), ('NV05', '2025-04-02', 'CA01', 'Có mặt'),
('NV05', '2025-04-03', 'CA02', 'Có mặt'), ('NV05', '2025-04-04', 'CA02', 'Có mặt'),
('NV05', '2025-04-05', 'CA03', 'Có mặt'), ('NV05', '2025-04-08', 'CA01', 'Có mặt'),
('NV05', '2025-04-09', 'CA01', 'Có mặt'), ('NV05', '2025-04-10', 'CA02', 'Có mặt'),
('NV05', '2025-04-11', 'CA02', 'Có mặt'), ('NV05', '2025-04-12', 'CA03', 'Có mặt'),
('NV05', '2025-04-15', 'CA01', 'Có mặt'), ('NV05', '2025-04-16', 'CA01', 'Có mặt'),
('NV05', '2025-04-17', 'CA02', 'Có mặt'), ('NV05', '2025-04-18', 'CA02', 'Có mặt'),
('NV05', '2025-04-19', 'CA03', 'Có mặt'), ('NV05', '2025-04-22', 'CA01', 'Có mặt'),
('NV05', '2025-04-23', 'CA02', 'Có mặt'), ('NV05', '2025-04-24', 'CA03', 'Có mặt'),
('NV05', '2025-04-25', 'CA01', 'Có mặt'), ('NV05', '2025-04-26', 'CA02', 'Có mặt'),
('NV05', '2025-04-29', 'CA03', 'Có mặt'),

('NV06', '2025-04-01', 'CA02', 'Có mặt'), ('NV06', '2025-04-02', 'CA02', 'Có mặt'),
('NV06', '2025-04-03', 'CA01', 'Có mặt'), ('NV06', '2025-04-04', 'CA01', 'Có mặt'),
('NV06', '2025-04-05', 'CA03', 'Có mặt'), ('NV06', '2025-04-08', 'CA02', 'Có mặt'),
('NV06', '2025-04-09', 'CA02', 'Có mặt'), ('NV06', '2025-04-10', 'CA01', 'Có mặt'),
('NV06', '2025-04-11', 'CA01', 'Có mặt'), ('NV06', '2025-04-12', 'CA03', 'Có mặt'),
('NV06', '2025-04-15', 'CA02', 'Có mặt'), ('NV06', '2025-04-16', 'CA02', 'Có mặt'),
('NV06', '2025-04-17', 'CA01', 'Có mặt'), ('NV06', '2025-04-18', 'CA01', 'Có mặt'),
('NV06', '2025-04-19', 'CA03', 'Có mặt'), ('NV06', '2025-04-22', 'CA02', 'Có mặt'),
('NV06', '2025-04-23', 'CA01', 'Có mặt'), ('NV06', '2025-04-24', 'CA03', 'Có mặt'),
('NV06', '2025-04-25', 'CA02', 'Có mặt'), ('NV06', '2025-04-26', 'CA01', 'Có mặt'),
('NV06', '2025-04-29', 'CA03', 'Có mặt');

INSERT INTO ChamCong (MaNhanVien, Ngay, MaCa, TrangThai) VALUES
('NV01', '2025-05-1', 'CA01', 'Có mặt'),
('NV02', '2025-05-1', 'CA02', 'Có mặt'),
('NV03', '2025-05-1', 'CA03', 'Có mặt'),
('NV04', '2025-05-2', 'CA01', 'Có mặt'),
('NV06', '2025-05-2', 'CA02', 'Có mặt'),
('NV05', '2025-05-2', 'CA03', 'Có mặt');

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL
);

INSERT INTO admin (username, password) VALUES 
('hr@gmail.com','123456');


