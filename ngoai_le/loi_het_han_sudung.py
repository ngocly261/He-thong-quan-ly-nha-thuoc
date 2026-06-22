class LoiHetHanSuDung(Exception):
    """Ngoại lệ ngăn chặn việc bán thuốc đã hết hạn sử dụng[cite: 35]."""
    def __init__(self, ten_thuoc, han_su_dung):
        self.ten_thuoc = ten_thuoc
        self.han_su_dung = han_su_dung
        self.msg = f"Lỗi hạn sử dụng: Thuốc '{ten_thuoc}' đã hết hạn vào ngày {han_su_dung}, nghiêm cấm bán ra!"
        super().__init__(self.msg)