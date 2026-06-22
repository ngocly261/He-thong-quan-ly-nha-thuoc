from abc import ABC, abstractmethod
from datetime import datetime

class DuocPham(ABC):
    """Lớp cha trừu tượng định nghĩa các thuộc tính và phương thức chung của dược phẩm."""
    def __init__(self, ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung, so_luong_ton=0):
        self.ma_thuoc = ma_thuoc            
        self.ten_thuoc = ten_thuoc          
        self.thanh_phan = thanh_phan        
        self.don_vi_tinh = don_vi_tinh      
        self.gia_nhap = float(gia_nhap)   
        self.han_su_dung = han_su_dung      
        self.so_luong_ton = int(so_luong_ton)
    @abstractmethod
    def tinh_gia_ban(self):
        """Phương thức trừu tượng tính giá bán, bắt buộc các lớp con phải cài đặt (Đa hình)."""
        pass

    def kiem_tra_han_dung(self):
        """Kiểm tra xem thuốc còn hạn sử dụng hay đã hết hạn."""
        try:
            ngay_het_han = datetime.strptime(self.han_su_dung, "%d/%m/%Y")
            return ngay_het_han >= datetime.now()
        except ValueError:
            return False 

    def __str__(self):
        return f"[{self.ma_thuoc}] {self.ten_thuoc} ({self.don_vi_tinh}) - Tồn: {self.so_luong_ton} - HSD: {self.han_su_dung}"