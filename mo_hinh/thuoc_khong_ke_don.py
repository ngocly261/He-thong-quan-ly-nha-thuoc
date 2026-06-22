from mo_hinh.duoc_pham import DuocPham

class ThuocKhongKeDon(DuocPham):
    """Lớp quản lý thuốc thông thường, bán không cần đơn."""
    def __init__(self, ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung, so_luong_ton=0):
        super().__init__(ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung, so_luong_ton)

    def tinh_gia_ban(self):
        """Thuốc không kê đơn: Lợi nhuận định mức 15% + Thuế VAT 10%."""
        return self.gia_nhap * 1.15 * 1.10