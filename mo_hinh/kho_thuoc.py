from cau_truc_du_lieu.bang_bam import BangBam
from thuat_toan.sap_xep_heap import heap_sort
from thuat_toan.loc_de_quy import loc_theo_hoat_chat_de_quy

class KhoThuoc:
    """Quản lý toàn bộ thuốc trong kho bằng cấu trúc Bảng băm tự định nghĩa."""
    def __init__(self):
        
        self.danh_sach_bham = BangBam()

    def them_thuoc(self, thuoc_obj):
        """Thêm một đối tượng thuốc vào kho."""
        self.danh_sach_bham.them(thuoc_obj.ma_thuoc, thuoc_obj)

    def tim_kiem_theo_ma(self, ma_thuoc):
        """Tìm kiếm thuốc theo mã với độ phức tạp tối ưu xấp xỉ O(1)."""
        return self.danh_sach_bham.lay(ma_thuoc)

    def lay_tat_ca_thuoc(self):
        """Lấy danh sách thông thường từ bảng băm phục vụ giao diện hiển thị."""
        return self.danh_sach_bham.lay_tat_ca_gia_tri()

    def lay_thuoc_sap_het_han(self):
        """Sử dụng thuật toán Heap Sort để sắp xếp thuốc có hạn dùng cận ngày nhất lên đầu."""
        tat_ca = self.lay_tat_ca_thuoc()
        return heap_sort(tat_ca)

    def loc_thuoc_theo_hoat_chat(self, hoat_chat):
        """Gọi thuật toán lọc đệ quy để tìm các thuốc chung thành phần hoạt chất."""
        tat_ca = self.lay_tat_ca_thuoc()
        return loc_theo_hoat_chat_de_quy(tat_ca, hoat_chat)

   
    def __getitem__(self, ma_thuoc):
        """Hỗ trợ cú pháp lấy đối tượng thuốc: thuoc = KhoThuoc["THUOC01"]"""
        return self.tim_kiem_theo_ma(ma_thuoc)

    def __setitem__(self, ma_thuoc, thuoc_obj):
        """Hỗ trợ cú pháp gán trực tiếp: KhoThuoc["THUOC01"] = thuoc_obj"""
        self.danh_sach_bham.them(ma_thuoc, thuoc_obj)

    def __iadd__(self, tuple_nhap_kho):
        """
        Nạp chồng toán tử += để cập nhật số lượng tồn kho cực nhanh.
        Cú pháp yêu cầu: KhoThuoc += ("MẠ_THUỐC", SỐ_LƯỢNG_NHẬP)
        Hoặc nếu gán qua key-value: KhoThuoc["MẠ_THUỐC"].so_luong_ton += 100
        """
        if isinstance(tuple_nhap_kho, tuple) and len(tuple_nhap_kho) == 2:
            ma_thuoc, so_luong_them = tuple_nhap_kho
            thuoc = self.tim_kiem_theo_ma(ma_thuoc)
            if thuoc:
                thuoc.so_luong_ton += int(so_luong_them)
            else:
                raise KeyError(f"Không tìm thấy mã thuốc '{ma_thuoc}' trong kho để cập nhật số lượng.")
        return self