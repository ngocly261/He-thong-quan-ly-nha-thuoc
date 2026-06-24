import tkinter as tk
from tkinter import ttk, messagebox
from mo_hinh.thuoc_ke_don import ThuocKeDon
from mo_hinh.thuoc_khong_ke_don import ThuocKhongKeDon
from mo_hinh.thuc_pham_chuc_nang import ThucPhamChucNang

class FormThuoc(tk.Toplevel):
    """Cửa sổ Pop-up để thêm mới thuốc hoặc cập nhật số lượng thuốc vào kho."""
    def __init__(self, parent, kho_thuoc, callback_cap_nhat):
        super().__init__(parent)
        self.kho = kho_thuoc
        self.callback_cap_nhat = callback_cap_nhat # Hàm gọi lại để làm mới bảng hiển thị bên ngoài
        
        self.title("Thêm Dược Phẩm Mới")
        self.geometry("450x550")
        self.grab_set() 
        
        tk.Label(self, text="THÔNG TIN DƯỢC PHẨM", font=("Arial", 14, "bold"), fg="#2c3e50").pack(pady=15)
        
        form_frame = tk.Frame(self, padx=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ô nhập chung
        labels = ["Mã thuốc:", "Tên thuốc:", "Thành phần:", "Đơn vị tính:", "Giá nhập:", "Hạn sử dụng (DD/MM/YYYY):", "Số lượng tồn:"]
        self.entries = {}
        
        for idx, text in enumerate(labels):
            lbl = tk.Label(form_frame, text=text, font=("Arial", 10), anchor="w")
            lbl.grid(row=idx, column=0, sticky="ew", pady=5)
            
            entry = tk.Entry(form_frame, font=("Arial", 10))
            entry.grid(row=idx, column=1, sticky="ew", pady=5)
            
            # Đặt tên khóa tiện lưu trữ
            key = text.replace(":", "").split(" ")[0].lower()
            self.entries[key] = entry
            
        form_frame.columnconfigure(1, weight=1)
        
        tk.Label(form_frame, text="Phân loại thuốc:", font=("Arial", 10)).grid(row=7, column=0, sticky="w", pady=5)
        self.cbo_loai = ttk.Combobox(form_frame, values=["Thuốc kê đơn", "Thuốc không kê đơn", "Thực phẩm chức năng"], state="readonly", font=("Arial", 10))
        self.cbo_loai.grid(row=7, column=1, sticky="ew", pady=5)
        self.cbo_loai.current(1)
        self.cbo_loai.bind("<<ComboboxSelected>>", lambda e: self.thay_doi_loai_thuoc())
        
        self.dynamic_frame = tk.Frame(form_frame)
        self.dynamic_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=5)
        self.dynamic_entry_1 = None
        self.dynamic_entry_2 = None
        
        btn_save = tk.Button(self, text="LƯU VÀO KHO", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", command=self.luu_du_lieu)
        btn_save.pack(fill=tk.X, padx=20, pady=20)

    def thay_doi_loai_thuoc(self):
        """Xóa trường cũ, sinh ra trường mới phù hợp với thuộc tính riêng của từng lớp con."""
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
            
        loai = self.cbo_loai.get()
        self.dynamic_frame.columnconfigure(1, weight=1)
        
        if loai == "Thuốc kê đơn":
            tk.Label(self.dynamic_frame, text="Mã bác sĩ:", font=("Arial", 10), width=12, anchor="w").grid(row=0, column=0, pady=5)
            self.dynamic_entry_1 = tk.Entry(self.dynamic_frame, font=("Arial", 10))
            self.dynamic_entry_1.grid(row=0, column=1, sticky="ew", pady=5)
            
            tk.Label(self.dynamic_frame, text="Cảnh báo liều:", font=("Arial", 10), width=12, anchor="w").grid(row=1, column=0, pady=5)
            self.dynamic_entry_2 = tk.Entry(self.dynamic_frame, font=("Arial", 10))
            self.dynamic_entry_2.grid(row=1, column=1, sticky="ew", pady=5)
            
        elif loai == "Thực phẩm chức năng":
            tk.Label(self.dynamic_frame, text="Nhà sản xuất:", font=("Arial", 10), width=12, anchor="w").grid(row=0, column=0, pady=5)
            self.dynamic_entry_1 = tk.Entry(self.dynamic_frame, font=("Arial", 10))
            self.dynamic_entry_1.grid(row=0, column=1, sticky="ew", pady=5)
            self.dynamic_entry_2 = None

    def luu_du_lieu(self):
        """Bắt lỗi nhập liệu chặt chẽ, hỗ trợ cả Thêm mới và Sửa thuốc, đồng bộ dữ liệu vào file JSON."""
        try:
            ma = self.entries["mã"].get().strip().upper()
            ten = self.entries["tên"].get().strip()
            thanh_phan = self.entries["thành"].get().strip()
            dvt = self.entries["đơn"].get().strip()
            gia = float(self.entries["giá"].get().strip())
            hsd = self.entries["hạn"].get().strip()
            ton = int(self.entries["số"].get().strip())
            
            if not ma or not ten:
                raise ValueError("Mã thuốc và tên thuốc không được để trống!")
                
            loai = self.cbo_loai.get()
            
            # Khởi tạo đúng đối tượng lớp con dựa trên phân loại thuốc
            if loai == "Thuốc kê đơn":
                ma_bs = self.dynamic_entry_1.get().strip() if self.dynamic_entry_1 else ""
                lieu = self.dynamic_entry_2.get().strip() if self.dynamic_entry_2 else ""
                thuoc_moi = ThuocKeDon(ma, ten, thanh_phan, dvt, gia, hsd, ma_bs, lieu, ton)
            elif loai == "Thực phẩm chức năng":
                nsx = self.dynamic_entry_1.get().strip() if self.dynamic_entry_1 else ""
                thuoc_moi = ThucPhamChucNang(ma, ten, thanh_phan, dvt, gia, hsd, nsx, ton)
            else:
                thuoc_moi = ThuocKhongKeDon(ma, ten, thanh_phan, dvt, gia, hsd, ton)
                
            # --- XỬ LÝ PHÂN NHÁNH: SỬA THUỐC VS THÊM MỚI ---
            is_edit_mode = getattr(self, 'mode', 'add') == 'edit'
            
            if is_edit_mode:
                # Chế độ SỬA: Ghi đè trực tiếp đối tượng thuốc mới vào Mã thuốc cũ trong bảng băm (RAM)
                # Nếu lớp KhoThuoc của bạn có hàm cap_nhat, bạn có thể đổi thành: self.kho.cap_nhat(ma, thuoc_moi)
                if hasattr(self.kho, 'kho_thuoc') and isinstance(self.kho.kho_thuoc, dict):
                    self.kho.kho_thuoc[ma] = thuoc_moi
                else:
                    # Dự phòng nếu self.kho kế thừa hoặc chính là dictionary chứa dữ liệu
                    try:
                        self.kho[ma] = thuoc_moi
                    except:
                        # Nếu self.kho có hàm thêm/cập nhật tùy biến thì dùng trực tiếp
                        self.kho.them_thuoc(thuoc_moi)
            else:
                # Chế độ THÊM MỚI: Báo lỗi nếu trùng mã thuốc
                # Kiểm tra trùng mã dựa trên cấu trúc lưu trữ của self.kho
                da_ton_tai = False
                if hasattr(self.kho, 'kho_thuoc') and ma in self.kho.kho_thuoc:
                    da_ton_tai = True
                elif hasattr(self.kho, '__contains__') and ma in self.kho:
                    da_ton_tai = True
                    
                if da_ton_tai:
                    messagebox.showerror("Lỗi dữ liệu", f"Mã thuốc '{ma}' đã tồn tại trong kho! Không thể thêm mới.")
                    return
                    
                self.kho.them_thuoc(thuoc_moi)
            
            # --- ĐỒNG BỘ GHI FILE JSON VĨNH VIỄN XUỐNG Ổ CỨNG ---
            try:
                from luu_tru.xu_ly_json import ghi_kho_thuoc_vao_json
                ghi_kho_thuoc_vao_json(self.kho)
                print(f"[ĐỒNG BỘ JSON] Đã lưu thông tin cập nhật của thuốc {ma} vào file JSON thành công.")
            except Exception as json_err:
                print(f"[CẢNH BÁO] Không thể ghi file JSON tự động: {json_err}")
            
            # Làm mới bảng hiển thị chính (Treeview) ở cửa sổ chính
            if hasattr(self, 'callback_cap_nhat') and self.callback_cap_nhat:
                self.callback_cap_nhat()
                
            messagebox.showinfo("Thành công", f"Đã lưu/cập nhật thông tin thuốc '{ten}' vào hệ thống vĩnh viễn!")
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Lỗi dữ liệu", f"Vui lòng kiểm tra lại định dạng nhập liệu!\nChi tiết: {e}")
    def nap_du_lieu_sua(self, thuoc):
        """Tự động điền dữ liệu cũ của thuốc được chọn vào các ô nhập."""
        self.title(f"Sửa Thông Tin Thuốc: {thuoc.ma_thuoc}")
        self.mode = "edit"  # Đánh dấu đang ở chế độ SỬA
        
        # Điền dữ liệu vào các ô Entry (Xóa chữ cũ trước khi chèn)
        self.entries['mã'].insert(0, thuoc.ma_thuoc)
        self.entries['mã'].config(state='disabled') # Khóa ô nhập mã, không cho sửa mã thuốc
        
        self.entries['tên'].insert(0, thuoc.ten_thuoc)
        self.entries['thành'].insert(0, thuoc.thanh_phan)
        self.entries['đơn'].insert(0, thuoc.don_vi_tinh)
        self.entries['giá'].insert(0, str(thuoc.gia_nhap))
        self.entries['hạn'].insert(0, thuoc.han_su_dung)
        
        # Riêng số lượng tồn kho (chỉ thuốc không kê đơn hoặc chung tùy logic của bạn)
        if 'số' in self.entries:
            self.entries['số'].insert(0, str(thuoc.so_luong_ton))
        
        # Tự động chọn đúng Phân loại thuốc trên Combobox
        if hasattr(self, 'cbo_loai'):
            ten_lop = thuoc.__class__.__name__
            if ten_lop == "ThuocKeDon":
                self.cbo_loai.set("Thuốc kê đơn")
                self.thay_doi_loai_thuoc() # Gọi hàm hiển thị ô dynamic
                if hasattr(self, 'dynamic_entry_1') and self.dynamic_entry_1:
                    self.dynamic_entry_1.insert(0, getattr(thuoc, 'ma_bac_si', ''))
                if hasattr(self, 'dynamic_entry_2') and self.dynamic_entry_2:
                    self.dynamic_entry_2.insert(0, getattr(thuoc, 'cach_dung', ''))
            elif ten_lop == "ThucPhamChucNang":
                self.cbo_loai.set("Thực phẩm chức năng")
                self.thay_doi_loai_thuoc()
                if hasattr(self, 'dynamic_entry_1') and self.dynamic_entry_1:
                    self.dynamic_entry_1.insert(0, getattr(thuoc, 'nha_san_xuat', ''))
            else:
                self.cbo_loai.set("Thuốc không kê đơn")
                self.thay_doi_loai_thuoc()