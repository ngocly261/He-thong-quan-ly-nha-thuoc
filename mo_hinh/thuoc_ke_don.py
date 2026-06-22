from mo_hinh.duoc_pham import DuocPham

class ThuocKeDon(DuocPham):
    """Lớp quản lý thuốc cần có đơn của bác sĩ mới được bán."""
    def __init__(self, ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung, ma_bac_si, canh_bao_lieu_dung, so_luong_ton=0):
        super().__init__(ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung, so_luong_ton)
        self.ma_bac_si = ma_bac_si
        self.canh_bao_lieu_dung = canh_bao_lieu_dung

    def tinh_gia_ban(self):
        """Thuốc kê đơn: Lợi nhuận định mức 10% + Thuế VAT 5%."""
        return self.gia_nhap * 1.10 * 1.05