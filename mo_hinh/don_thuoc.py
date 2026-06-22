from datetime import datetime
from ngoai_le.loi_het_hang import LoiHetHang
from ngoai_le.loi_het_han_sudung import LoiHetHanSuDung

class DonThuoc:
    """Quản lý các sản phẩm khách chọn mua và xuất hóa đơn tính tiền."""
    def __init__(self, ma_don):
        self.ma_don = ma_don
        self.ngay_ke = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.danh_sach_mua = {}

    def them_san_pham(self, duoc_pham, so_luong_mua):
        """Thêm thuốc vào đơn hàng, thực hiện các kiểm tra an toàn nghiêm ngặt."""
        # 1. Kiểm tra hạn sử dụng trước khi bán
        if not duoc_pham.kiem_tra_han_dung():
            raise LoiHetHanSuDung(duoc_pham.ten_thuoc, duoc_pham.han_su_dung)
        
        # 2. Kiểm tra số lượng tồn kho
        if duoc_pham.so_luong_ton < so_luong_mua:
            raise LoiHetHang(duoc_pham.ten_thuoc, duoc_pham.so_luong_ton, so_luong_mua)
            
        # Nếu đã có trong đơn thì cộng dồn, chưa có thì tạo mới
        if duoc_pham in self.danh_sach_mua:
            self.danh_sach_mua[duoc_pham] += so_luong_mua
        else:
            self.danh_sach_mua[duoc_pham] = so_luong_mua

    def tinh_tong_tien(self):
        """Tính tổng số tiền của đơn hàng dựa trên giá bán đa hình của từng loại."""
        tong = 0.0
        for duoc_pham, so_luong in self.danh_sach_mua.items():
            tong += duoc_pham.tinh_gia_ban() * so_luong
        return round(tong, 2)

    def thuc_hiện_tru_kho(self):
        """Khi bấm thanh toán, chính thức trừ số lượng tồn kho của thuốc."""
        for duoc_pham, so_luong in self.danh_sach_mua.items():
            duoc_pham.so_luong_ton -= so_luong

    def xuat_hoa_don_text(self):
        """Sinh chuỗi văn bản hóa đơn trực quan để hiển thị ra màn hình GUI."""
        hd = f"--- HÓA ĐƠN BÁN HÀNG ({self.ma_don}) ---\n"
        hd += f"Ngày lập: {self.ngay_ke}\n"
        hd += f"{'-'*45}\n"
        hd += f"{'Tên thuốc':<20} | {'SL':<4} | {'Thành tiền':<15}\n"
        hd += f"{'-'*45}\n"
        
        for duoc_pham, so_luong in self.danh_sach_mua.items():
            thanh_tien = duoc_pham.tinh_gia_ban() * so_luong
            hd += f"{duoc_pham.ten_thuoc:<20} | {so_luong:<4} | {thanh_tien:,.0f} VNĐ\n"
            
        hd += f"{'-'*45}\n"
        hd += f"TỔNG THANH TOÁN: {self.tinh_tong_tien():,.0f} VNĐ\n"
        return hd