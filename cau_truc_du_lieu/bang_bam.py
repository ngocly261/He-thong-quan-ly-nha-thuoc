from cau_truc_du_lieu.nut_bam import NutBam

class BangBam:
    """Cài đặt Bảng băm (Hash Table) tự xây dựng giải quyết xung đột bằng phương pháp Chaining."""
    def __init__(self, kich_thuoc_ban_dau=1007):
        self.kich_thuoc = kich_thuoc_ban_dau
        self.slots = [None] * self.kich_thuoc
        self.tong_so_phan_tu = 0

    def _hash_function(self, key):
        """Hàm băm chuỗi ký tự (Polynomial Rolling Hash) để chuyển key thành chỉ mục mảng."""
        hash_val = 0
        p = 31  
        for char in str(key):
            hash_val = (hash_val * p + ord(char)) % self.kich_thuoc
        return hash_val

    def them(self, key, value):
        """Thêm hoặc cập nhật một cặp Key-Value trong bảng băm."""
        chi_muc = self._hash_function(key)
        
        if self.slots[chi_muc] is None:
            self.slots[chi_muc] = NutBam(key, value)
            self.tong_so_phan_tu += 1
        else:
            hien_tai = self.slots[chi_muc]
            while True:
                if hien_tai.key == key:
                    hien_tai.value = value 
                    return
                if hien_tai.next is None:
                    break
                hien_tai = hien_tai.next
            
            hien_tai.next = NutBam(key, value)
            self.tong_so_phan_tu += 1

    def lay(self, key):
        """Truy xuất giá trị (Value) theo khóa (Key). Trả về None nếu không tìm thấy."""
        chi_muc = self._hash_function(key)
        hien_tai = self.slots[chi_muc]
        
        while hien_tai is not None:
            if hien_tai.key == key:
                return hien_tai.value
            hien_tai = hien_tai.next
        return None

    def xoa(self, key):
        """Xóa nút chứa mã thuốc ra khỏi danh sách liên kết của ô băm O(1)."""
        chi_muc = self._hash_function(key)
        hien_tai = self.slots[chi_muc]
        truoc_do = None
        
        while hien_tai is not None:
            if hien_tai.key == key:
                if truoc_do is None:
                    # Nếu nút cần xóa nằm ngay đầu Slot
                    self.slots[chi_muc] = hien_tai.next
                else:
                    # Nếu nút cần xóa nằm ở giữa hoặc cuối chuỗi liên kết Chaining
                    truoc_do.next = hien_tai.next
                self.tong_so_phan_tu -= 1
                return True
            truoc_do = hien_tai
            hien_tai = hien_tai.next
        return False

    def lay_tat_ca_gia_tri(self):
        """Trả về một danh sách chứa toàn bộ các đối tượng đang lưu trong bảng băm."""
        danh_sach = []
        for slot in self.slots:
            hien_tai = slot
            while hien_tai is not None:
                danh_sach.append(hien_tai.value)
                hien_tai = hien_tai.next
        return danh_sach
    
    def cap_nhat(self, key, du_lieu_moi):
        """Tìm kiếm phần tử theo mã thuốc và cập nhật thông tin mới O(1)."""
        chi_muc = self._hash_function(key)
        hien_tai = self.slots[chi_muc]
        
        while hien_tai is not None:
            if hien_tai.key == key:
                hien_tai.value = du_lieu_moi
                return True
            hien_tai = hien_tai.next
        return False