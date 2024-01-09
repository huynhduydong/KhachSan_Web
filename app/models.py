import enum
import hashlib
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean, BOOLEAN, DATETIME
from sqlalchemy.orm import relationship

from app import db, app


class UserRole(enum.Enum):
    NHAN_VIEN = 1
    QUAN_LY = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(45), unique=True, nullable=True)
    password = Column(String(45), nullable=True)
    ten = Column(String(45), nullable=False)
    ho = Column(String(22), nullable=False)
    gioi_tinh = Column(BOOLEAN, nullable=False, default=False)
    ngay_sinh = Column(DATETIME, nullable=True)
    cccd = Column(String(15), nullable=False, unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.QUAN_LY)


class LoaiPhongEnum(enum.Enum):
    VIP = 1
    THUONG = 2
    SIEUVIP = 3


class TinhTrangPhongEnum(enum.Enum):
    TRONG = 1
    DA_DAT = 2
    DANG_O = 3


class KhachHangEnum(enum.Enum):
    NOI_DIA = 1
    NUOC_NGOAI = 2


class KhachHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenKhachHang = Column(String(30), nullable=False)
    loaiKhachHang = Column(Enum(KhachHangEnum), nullable=False)
    CMND = Column(Integer, nullable=False)
    diaChia = Column(String(50), nullable=False)
    maDatPhong = Column(Integer, ForeignKey('phieu_dat_phong.id'), nullable=False)


class ChiTietDatPhong(db.Model):
    idPhong = Column(Integer, ForeignKey('phong.id'), primary_key=True)
    idPhieuDatPhong = Column(Integer, ForeignKey('phieu_dat_phong.id'), primary_key=True)
    donGia = Column(Integer, nullable=False)


class Phong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    maPhong = Column(String(10), nullable=False)
    loaiPhong = Column(Enum(LoaiPhongEnum), nullable=False)
    donGia = Column(Integer, nullable=False)
    tinhTrang = Column(Enum(TinhTrangPhongEnum), nullable=False)
    cacPhieuDatPhong = relationship('PhieuDatPhong', secondary='chi_tiet_dat_phong', back_populates='cacPhong')


class PhieuDatPhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenNguoiDat = Column(String(30), nullable=False)
    ngayDatPhong = Column(DateTime, nullable=False)
    ngayTraPhong = Column(DateTime, nullable=False)
    cacPhong = relationship('Phong', secondary='chi_tiet_dat_phong', back_populates='cacPhieuDatPhong')


class PhieuThuePhong(db.Model):
    idPhieu = Column(Integer, primary_key=True, autoincrement=True)
    idDatPhong = Column(Integer, ForeignKey('phieu_dat_phong.id'), unique=True)
    phieuThuePhong = relationship('PhieuDatPhong')


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Thêm 5 bản ghi mẫu cho model Phong
        for _ in range(5):
            phong = Phong(
                maPhong=f"Phong{_}",
                loaiPhong=LoaiPhongEnum.VIP,
                donGia=1000000 + _ * 100000,
                tinhTrang=TinhTrangPhongEnum.TRONG
            )
            db.session.add(phong)
        db.session.commit()

        # Thêm 5 bản ghi mẫu cho model PhieuDatPhong
        for _ in range(5):
            phieu_dat_phong = PhieuDatPhong(
                tenNguoiDat=f"NguoiDat{_}",
                ngayDatPhong=datetime.now(),
                ngayTraPhong=datetime.now()
            )
            db.session.add(phieu_dat_phong)
        db.session.commit()

        # Thêm 5 bản ghi mẫu cho model ChiTietDatPhong
        for _ in range(5):
            chi_tiet_dat_phong = ChiTietDatPhong(
                idPhong=_ + 1,  # Giả sử idPhong tăng dần từ 1
                idPhieuDatPhong=_ + 1,  # Giả sử idPhieuDatPhong tăng dần từ 1
                donGia=1000000 + _ * 100000
            )
            db.session.add(chi_tiet_dat_phong)
        db.session.commit()

        for _ in range(5):
            khach_hang = KhachHang(
                tenKhachHang=f"KhachHang{_}",
                loaiKhachHang=KhachHangEnum.NOI_DIA,
                CMND=1000000000 + _,
                diaChia=f"DiaChi{_}",
                maDatPhong=_ + 1  # Giả sử mã đặt phòng tăng dần từ 1
            )
            db.session.add(khach_hang)
        db.session.commit()

        # Thêm 5 bản ghi mẫu cho model PhieuThuePhong
        for _ in range(5):
            phieu_thue_phong = PhieuThuePhong(
                idDatPhong=_ + 1  # Giả sử idDatPhong tăng dần từ 1
            )
            db.session.add(phieu_thue_phong)

        # Lưu các thay đổi vào cơ sở dữ liệu
        db.session.commit()

        admin = User(username='admin', password=hashlib.md5('123'.encode('utf-8')).hexdigest(), ten='admin', ho='admin',
                     gioi_tinh=True, cccd="123", user_role=UserRole.QUAN_LY)
        nv = User(username='nv', password=hashlib.md5('123'.encode('utf-8')).hexdigest(), ten='admin', ho='admin',
                  gioi_tinh=True, cccd="12333", user_role=UserRole.NHAN_VIEN)

        db.session.add(nv)
        db.session.add(admin)
        db.session.commit()
