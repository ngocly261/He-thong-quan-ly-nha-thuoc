class LoiHetHang(Exception):
    """Ngoại lệ ném ra khi số lượng thuốc trong kho không đủ cho đơn hàng."""
    def __init__(self, ten_thuoc, ton_kho, so_luong_yeu_cau):
        self.ten_thuoc = ten_thuoc
        self.ton_kho = ton_kho
        self.so_luong_yeu_cau = so_luong_yeu_cau
        self.msg = f"Lỗi hết hàng: Thuốc '{ten_thuoc}' chỉ còn {ton_kho} sản phẩm trong kho, không đủ đáp ứng yêu cầu ({so_luong_yeu_cau})."
        super().__init__(self.msg)