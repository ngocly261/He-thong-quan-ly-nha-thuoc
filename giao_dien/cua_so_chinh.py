import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from luu_tru.xu_ly_json import doc_kho_thuoc_tu_json, ghi_kho_thuoc_vao_json
import tkinter as tk
from tkinter import ttk, messagebox
from luu_tru.xu_ly_json import doc_kho_thuoc_tu_json, ghi_kho_thuoc_vao_json, luu_don_hang_vao_lich_su
from giao_dien.form_thuoc import FormThuoc
from giao_dien.form_hoa_don import FormHoaDon
from giao_dien.bieu_do_doanh_thu import BieuDoDoanhThu

class CuaSoChinh(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HỆ THỐNG QUẢN LÝ NHÀ THUỐC ĐỒ ÁN")
        self.geometry("1000x600")
        
        # Nạp kho thuốc từ cơ sở dữ liệu JSON lên Bảng băm bộ nhớ khi khởi động app
        self.kho_thuoc = doc_kho_thuoc_tu_json()
        
        # --- THANH MENU ĐIỀU HƯỚNG PHÍA TRÊN ---
        top_bar = tk.Frame(self, bg="#2c3e50", height=50)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        
        lbl_brand = tk.Label(top_bar, text="MedManager v1.0", font=("Arial", 12, "bold"), fg="white", bg="#2c3e50")
        lbl_brand.pack(side=tk.LEFT, padx=15, pady=10)
        
        btn_add = tk.Button(top_bar, text="+ Nhập Thuốc Mới", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), command=self.mo_form_them_thuoc)
        btn_add.pack(side=tk.LEFT, padx=10, pady=10)

        btn_sua = tk.Button(top_bar, text="✏️ Sửa Thuốc", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), command=self.xu_ly_sua_thuoc)
        btn_sua.pack(side=tk.LEFT, padx=5)

        btn_xoa = tk.Button(top_bar, text="🗑️ Xóa Thuốc", bg="#c0392b", fg="white", font=("Arial", 10, "bold"), command=self.xu_ly_xoa_thuoc)
        btn_xoa.pack(side=tk.LEFT, padx=5)
        
        btn_invoice = tk.Button(top_bar, text="🛒 Lập Đơn Bán Hàng", bg="#3498db", fg="white", font=("Arial", 10, "bold"), command=self.mo_form_hoa_don)
        btn_invoice.pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_chart = tk.Button(top_bar, text="📊 Xem Biểu Đồ Doanh Thu", bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), command=self.mo_tab_bieu_do)
        btn_chart.pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_heap = tk.Button(top_bar, text="⏳ Sắp Xếp Hạn Sử Dụng (Heap Sort)", bg="#f1c40f", fg="#2c3e50", font=("Arial", 10, "bold"), command=self.hien_thi_thuoc_sap_xep_heap)
        btn_heap.pack(side=tk.LEFT, padx=10, pady=10)

        # --- KHU VỰC TÌM KIẾM THÔNG MINH (SMART SEARCH) ---
        search_frame = tk.Frame(self, padx=15, pady=10)
        search_frame.pack(fill=tk.X)
        
        tk.Label(search_frame, text="Tìm kiếm thông minh (Mã/Hoạt chất):", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.ent_search = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.ent_search.pack(side=tk.LEFT, padx=5)
        self.ent_search.bind("<KeyRelease>", self.xu_ly_tim_kiem_thong_minh) # Bắt sự kiện gõ phím trực tiếp
        
        btn_clear = tk.Button(search_frame, text="Đặt lại danh sách", command=self.lam_moi_bang_du_lieu)
        btn_clear.pack(side=tk.LEFT, padx=10)

        # --- BẢNG HIỂN THỊ DANH MỤC THUỐC TRỰC QUAN ---
        table_frame = tk.Frame(self, padx=15, pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ma", "ten", "thanh_phan", "dvt", "gia_nhap", "gia_ban", "hsd", "ton", "loai")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Cấu hình tiêu đề cột
        self.tree.heading("ma", text="Mã Thuốc")
        self.tree.heading("ten", text="Tên Thuốc")
        self.tree.heading("thanh_phan", text="Thành Phần")
        self.tree.heading("dvt", text="ĐVT")
        self.tree.heading("gia_nhap", text="Giá Nhập")
        self.tree.heading("gia_ban", text="Giá Bán (Đa Hình)")
        self.tree.heading("hsd", text="Hạn Sử Dụng")
        self.tree.heading("ton", text="Tồn Kho")
        self.tree.heading("loai", text="Phân Loại")
        
        # Cấu hình độ rộng cột gọn gàng
        for col in columns:
            self.tree.column(col, width=100, anchor="center")
        
        # Tạo thanh cuộn (Scrollbar) cho bảng
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Thiết lập màu nền highlight cho cảnh báo nguy cơ nghiệp vụ
        self.tree.tag_configure("HET_HAN", background="#ff7675", foreground="white")     # Màu đỏ nếu hết hạn sử dụng
        self.tree.tag_configure("SAP_HET_HANG", background="#ffeaa7", foreground="#2d3436")# Màu cam/vàng nếu tồn kho thấp (<10 vỉ/hộp)
        
        # Nạp dữ liệu lên bảng lần đầu
        self.lam_moi_bang_du_lieu()

    def lam_moi_bang_du_lieu(self, danh_sach_thuoc=None):
        """Xóa bảng cũ và nạp lại toàn bộ dữ liệu kèm kiểm tra highlight cảnh báo."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if danh_sach_thuoc is None:
            danh_sach_thuoc = self.kho_thuoc.lay_tat_ca_thuoc()
            
        for t in danh_sach_thuoc:
            tag = "NORMAL"
            # 1. Kiểm tra an toàn hạn sử dụng trước
            if not t.kiem_tra_han_dung():
                tag = "HET_HAN"
            # 2. Kiểm tra tồn kho dưới ngưỡng tối thiểu an toàn (Dưới 10 đơn vị)
            elif t.so_luong_ton < 10:
                tag = "SAP_HET_HANG"
                
            self.tree.insert("", tk.END, values=(
                t.ma_thuoc, t.ten_thuoc, t.thanh_phan, t.don_vi_tinh,
                f"{t.gia_nhap:,.0f}", f"{t.tinh_gia_ban():,.0f}",
                t.han_su_dung, t.so_luong_ton, t.__class__.__name__
            ), tags=(tag,))

    def xu_ly_tim_kiem_thong_minh(self, event):
        """Ô tìm kiếm thông minh: Gõ đến đâu kết quả từ Bảng băm/Đệ quy lọc đến đấy."""
        tu_khoa = self.ent_search.get().strip().upper()
        if not tu_khoa:
            self.lam_moi_bang_du_lieu()
            return
            
        # 1. Ưu tiên 1: Tra cứu nhanh O(1) từ bảng băm theo mã thuốc qua nạp chồng toán tử
        thuoc_tim_thay = self.kho_thuoc[tu_khoa]
        if thuoc_tim_thay:
            self.lam_moi_bang_du_lieu([thuoc_tim_thay])
            return
            
        # 2. Ưu tiên 2: Nếu không thấy mã, gọi Lọc đệ quy tìm kiếm theo chuỗi hoạt chất thành phần
        ket_qua_loc = self.kho_thuoc.loc_thuoc_theo_hoat_chat(tu_khoa)
        self.lam_moi_bang_du_lieu(ket_qua_loc)

    def hien_thi_thuoc_sap_xep_heap(self):
        """Gọi thuật toán Heap Sort để đẩy toàn bộ thuốc sắp hết hạn lên đầu danh sách."""
        danh_sach_sap_xep = self.kho_thuoc.lay_thuoc_sap_het_han()
        self.lam_moi_bang_du_lieu(danh_sach_sap_xep)
        messagebox.showinfo("Heap Sort", "Đã sắp xếp! Các thuốc có hạn sử dụng cận ngày nhất hoặc đã quá hạn đã được đẩy lên hàng đầu.")

    def mo_form_them_thuoc(self):
        """Mở cửa sổ thêm sản phẩm và lưu bền vững khi đóng."""
        FormThuoc(self, self.kho_thuoc, self.luu_va_lam_moi_kho)

    def mo_form_hoa_don(self):
        """Mở cửa sổ lập đơn bán hàng nhanh."""
        FormHoaDon(self, self.kho_thuoc, self.xu_ly_thanh_toan_don_hang)

    def mo_tab_bieu_do(self):
        """Mở một cửa sổ mới độc lập hiển thị đồ thị đường doanh thu."""
        top_chart = tk.Toplevel(self)
        top_chart.title("Báo Cáo Thống Kê Doanh Thu")
        top_chart.geometry("700x450")
        BieuDoDoanhThu(top_chart)

    def luu_va_lam_moi_kho(self):
        """Ghi dữ liệu đồng bộ xuống file JSON danh mục."""
        ghi_kho_thuoc_vao_json(self.kho_thuoc)
        self.lam_moi_bang_du_lieu()

    def xu_ly_thanh_toan_don_hang(self, don_thuoc_da_ban):
        """Ghi nhận đơn hàng mới thành công, cập nhật kho vật lý và ghi file JSON."""
        luu_don_hang_vao_lich_su(don_thuoc_da_ban)
        self.luu_va_lam_moi_kho()
    
    def xu_ly_xoa_thuoc(self):
        """Xóa thuốc khỏi bảng băm, cập nhật JSON và xóa trực tiếp dòng hiển thị trên giao diện."""
        if not hasattr(self, 'tree'):
            return
            
        item_duoc_chon = self.tree.selection()
        if not item_duoc_chon:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn một loại thuốc trong bảng để xóa!")
            return
            
        ma_thuoc = self.tree.item(item_duoc_chon)['values'][0]
        
        xac_nhan = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa thuốc {ma_thuoc} khỏi hệ thống không?")
        if xac_nhan:
            # 1. Gọi lệnh xóa trực tiếp từ bảng băm nội bộ của đối tượng kho_thuoc
            if hasattr(self.kho_thuoc, 'kho_thuoc'):
                self.kho_thuoc.kho_thuoc.xoa(ma_thuoc)
            elif hasattr(self.kho_thuoc, 'bang_bam'):
                self.kho_thuoc.bang_bam.xoa(ma_thuoc)
            
            # 2. Ghi đè file JSON để cập nhật dữ liệu bền vững xuống ổ đĩa
            try:
                import luu_tru.xu_ly_json as xl_json
                xl_json.ghi_kho_thuoc_vao_json(self.kho_thuoc)
            except Exception:
                import sys, os
                sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                import luu_tru.xu_ly_json as xl_json
                xl_json.ghi_kho_thuoc_vao_json(self.kho_thuoc)
            
            # 3. Xóa dòng trực tiếp trên giao diện Treeview ngay lập tức
            self.tree.delete(item_duoc_chon)
            messagebox.showinfo("Thành công", f"Đã xóa hoàn toàn thuốc {ma_thuoc}!")

    def xu_ly_sua_thuoc(self):
        """Mở form sửa thuốc tương thích 100% với form_thuoc.py hiện tại mà không lỗi tham số."""
        if not hasattr(self, 'tree'):
            return
            
        item_duoc_chon = self.tree.selection()
        if not item_duoc_chon:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn một loại thuốc trong bảng để sửa!")
            return
            
        ma_thuoc = self.tree.item(item_duoc_chon)['values'][0]
        thuoc_hien_tai = self.kho_thuoc[ma_thuoc]
        
        from giao_dien.form_thuoc import FormThuoc
        # Chỉ truyền đúng 2 tham số gốc mà hàm __init__ của FormThuoc đang nhận để tránh lỗi 'callback_luu'
        cua_so_sua = FormThuoc(self, self.kho_thuoc)
        
        # Gán đè đối tượng thuốc cần sửa vào thuộc tính của form
        cua_so_sua.thuoc_can_sua = thuoc_hien_tai
        
        # Lắng nghe sự kiện khi đóng cửa sổ FormThuoc để tự động nạp lại bảng ở cửa sổ chính
        cua_so_sua.bind("<Destroy>", lambda e: self.lam_moi_bang_du_lieu())