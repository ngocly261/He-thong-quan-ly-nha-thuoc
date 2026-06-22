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
        self.grab_set() # Khóa tiêu điểm vào cửa sổ này
        
        # Thành phần giao diện chính
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
        
        # Lựa chọn phân loại thuốc để hiển thị trường đặc thù (Tính Đa Hình OOP)
        tk.Label(form_frame, text="Phân loại thuốc:", font=("Arial", 10)).grid(row=7, column=0, sticky="w", pady=5)
        self.cbo_loai = ttk.Combobox(form_frame, values=["Thuốc kê đơn", "Thuốc không kê đơn", "Thực phẩm chức năng"], state="readonly", font=("Arial", 10))
        self.cbo_loai.grid(row=7, column=1, sticky="ew", pady=5)
        self.cbo_loai.current(1)
        self.cbo_loai.bind("<<ComboboxSelected>>", lambda e: self.thay_doi_loai_thuoc())
        
        # Khung chứa các trường động đặc thù
        self.dynamic_frame = tk.Frame(form_frame)
        self.dynamic_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=5)
        self.dynamic_entry_1 = None
        self.dynamic_entry_2 = None
        
        # Nút bấm lưu trữ
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
        """Bắt lỗi nhập liệu chặt chẽ và khởi tạo đúng đối tượng lớp con đưa vào hệ thống."""
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
            
            # Đa hình khởi tạo lớp con phù hợp
            if loai == "Thuốc kê đơn":
                ma_bs = self.dynamic_entry_1.get().strip() if self.dynamic_entry_1 else ""
                lieu = self.dynamic_entry_2.get().strip() if self.dynamic_entry_2 else ""
                thuoc_moi = ThuocKeDon(ma, ten, thanh_phan, dvt, gia, hsd, ma_bs, lieu, ton)
            elif loai == "Thực phẩm chức năng":
                nsx = self.dynamic_entry_1.get().strip() if self.dynamic_entry_1 else ""
                thuoc_moi = ThucPhamChucNang(ma, ten, thanh_phan, dvt, gia, hsd, nsx, ton)
            else:
                thuoc_moi = ThuocKhongKeDon(ma, ten, thanh_phan, dvt, gia, hsd, ton)
                
            # Đưa vào kho lưu trữ (Bảng băm)
            self.kho.them_thuoc(thuoc_moi)
            self.callback_cap_nhat() # Làm mới bảng hiển thị chính
            messagebox.showinfo("Thành công", f"Đã thêm/cập nhật thuốc '{ten}' vào kho thuốc!")
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Lỗi dữ liệu", f"Vui lòng kiểm tra lại định dạng nhập liệu!\nChi tiết: {e}")