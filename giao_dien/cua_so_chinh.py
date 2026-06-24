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
        self.state('zoomed')
        
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

        self.tree.heading("ma", text="Mã Thuốc")
        self.tree.heading("ten", text="Tên Thuốc")
        self.tree.heading("thanh_phan", text="Thành Phần")
        self.tree.heading("dvt", text="ĐVT")
        self.tree.heading("gia_nhap", text="Giá Nhập")
        self.tree.heading("gia_ban", text="Giá Bán (Đa Hình)")
        self.tree.heading("hsd", text="Hạn Sử Dụng")
        self.tree.heading("ton", text="Tồn Kho")
        self.tree.heading("loai", text="Phân Loại")
        
        for col in columns:
            self.tree.column(col, width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.tag_configure("HET_HAN", background="#ff7675", foreground="white")     # Màu đỏ nếu hết hạn sử dụng
        self.tree.tag_configure("SAP_HET_HANG", background="#ffeaa7", foreground="#2d3436")# Màu cam/vàng nếu tồn kho thấp (<10 vỉ/hộp)
        
        self.lam_moi_bang_du_lieu()

    def lam_moi_bang_du_lieu(self, danh_sach_thuoc=None):
        """Xóa bảng cũ và nạp lại toàn bộ dữ liệu kèm kiểm tra highlight cảnh báo."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if danh_sach_thuoc is None:
            danh_sach_thuoc = self.kho_thuoc.lay_tat_ca_thuoc()
            
        for t in danh_sach_thuoc:
            tag = "NORMAL"
            if not t.kiem_tra_han_dung():
                tag = "HET_HAN"
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
            
        thuoc_tim_thay = self.kho_thuoc[tu_khoa]
        if thuoc_tim_thay:
            self.lam_moi_bang_du_lieu([thuoc_tim_thay])
            return
            
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
        """Xóa thuốc đồng thời trên giao diện hiển thị và tìm gốc file JSON để xóa vĩnh viễn."""
        import json
        import os
        
        if not hasattr(self, 'tree'):
            return
            
        item_duoc_chon = self.tree.selection()
        if not item_duoc_chon:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn một loại thuốc trong bảng để xóa!")
            return
            
        ma_thuoc = self.tree.item(item_duoc_chon)['values'][0]
        
        xac_nhan = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa thuốc {ma_thuoc} vĩnh viễn khỏi hệ thống?")
        if xac_nhan:
            # 1. XÓA NGAY TRÊN GIAO DIỆN TREEVIEW ĐỂ HIỂN THỊ TRỰC QUAN
            try:
                self.tree.delete(item_duoc_chon)
            except Exception as e:
                print(f"Lỗi giao diện Treeview: {e}")

            # 2. QUÉT TOÀN BỘ THƯ MỤC DỰ ÁN ĐỂ TÌM FILE JSON CHỨA MÃ THUỐC ĐÓ
            da_xoa_json = False
            
            # Liệt kê tất cả các file .json khả nghi trong thư mục dự án của bạn
            file_json_list = []
            for root_dir, dirs, files in os.walk("."):
                # Bỏ qua thư mục ẩn venv hoặc .git để tìm cho nhanh
                if "venv" in root_dir or ".git" in root_dir or "__pycache__" in root_dir:
                    continue
                for file in files:
                    if file.endswith(".json") and file != "lich_su_don_hang.json":
                        file_json_list.append(os.path.join(root_dir, file))

            # Tiến hành đục bỏ mã thuốc ở TẤT CẢ các file JSON tìm thấy
            for path in file_json_list:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    local_deleted = False
                    # Trường hợp dữ liệu là Dictionary
                    if isinstance(data, dict):
                        if ma_thuoc in data:
                            del data[ma_thuoc]
                            local_deleted = True
                        else:
                            for k, v in data.items():
                                if isinstance(v, dict) and ma_thuoc in v:
                                    del v[ma_thuoc]
                                    local_deleted = True
                                    break
                                    
                    # Trường hợp dữ liệu là List (Danh sách đối tượng)
                    elif isinstance(data, list):
                        old_len = len(data)
                        data = [item for item in data if item.get('ma_thuoc') != ma_thuoc and item.get('Mã Thuốc') != ma_thuoc and item.get('ma') != ma_thuoc]
                        if len(data) < old_len:
                            local_deleted = True
                    
                    # Nếu file này chứa mã thuốc vừa xóa, tiến hành ghi đè sập nội dung mới vào
                    if local_deleted:
                        with open(path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        print(f"[XÁC NHẬN] Đã xóa triệt để thuốc {ma_thuoc} trong file: {path}")
                        da_xoa_json = True
                except Exception as e:
                    print(f"Không thể can thiệp file {path}: {e}")

            # 3. ĐỒNG BỘ LẠI BẢNG BĂM TRÊN RAM ĐỂ TRÁNH XUNG ĐỘT KHI CHẠY TIẾP
            try:
                if hasattr(self, 'kho_thuoc'):
                    for ten_ham in ['xoa', 'xoa_thuoc', 'delete', 'remove']:
                        if hasattr(self.kho_thuoc, ten_ham):
                            getattr(self.kho_thuoc, ten_ham)(ma_thuoc)
                            break
            except:
                pass

            if da_xoa_json:
                messagebox.showinfo("Thành công", f"Đã xóa vĩnh viễn thuốc {ma_thuoc} khỏi giao diện!")
            else:
                messagebox.showwarning("Cảnh báo", f"Đã xóa trên giao diện nhưng không tìm thấy mã {ma_thuoc} trong các file JSON nền!")
    def xu_ly_sua_thuoc(self):
        """Mở form sửa thuốc và nạp dữ liệu cũ vào các ô nhập."""
        if not hasattr(self, 'tree'):
            return
            
        item_duoc_chon = self.tree.selection()
        if not item_duoc_chon:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn một loại thuốc trong bảng để sửa!")
            return
            
        # 1. Lấy mã thuốc từ dòng được chọn
        ma_thuoc = self.tree.item(item_duoc_chon)['values'][0]
        thuoc_hien_tai = self.kho_thuoc[ma_thuoc]
        
        # 2. Mở FormThuoc (truyền thêm hàm callback để làm mới bảng sau khi lưu)
        from giao_dien.form_thuoc import FormThuoc
        cua_so_sua = FormThuoc(self, self.kho_thuoc, self.lam_moi_bang_du_lieu)
        
        # 3. Gọi hàm nạp dữ liệu (chúng ta sẽ viết hàm này ở Bước 2)
        cua_so_sua.nap_du_lieu_sua(thuoc_hien_tai)
        