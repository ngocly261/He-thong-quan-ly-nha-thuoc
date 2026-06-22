from mo_hinh.duoc_pham import DuocPham

class ThucPhamChucNang(DuocPham):
    """Lớp quản lý thực phẩm chức năng, vitamin bổ sung."""
    def __init__(self, ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung, nha_san_xuat, so_luong_ton=0):
        super().__init__(ma_thuoc, ten_thuoc, thanh_phan, don_vi_tinh, gia_nhap, han_su_dung, so_luong_ton)
        self.nha_san_xuat = nha_san_xuat

    def tinh_gia_ban(self):
        """Thực phẩm chức năng: Lợi nhuận định mức 20% + Thuế VAT 10%."""
        return self.gia_nhap * 1.20 * 1.10