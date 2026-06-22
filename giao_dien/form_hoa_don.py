import tkinter as tk
from tkinter import messagebox
from mo_hinh.don_thuoc import DonThuoc
from ngoai_le.loi_het_hang import LoiHetHang
from ngoai_le.loi_het_han_sudung import LoiHetHanSuDung
import random

class FormHoaDon(tk.Toplevel):
    """Cửa sổ lập hóa đơn bán thuốc cho khách hàng, tích hợp kiểm thử ngoại lệ."""
    def __init__(self, parent, kho_thuoc, callback_luu_xong):
        super().__init__(parent)
        self.kho = kho_thuoc
        self.callback_luu_xong = callback_luu_xong
        
        # Khởi tạo mã đơn hàng ngẫu nhiên độc nhất
        self.don_thuoc = DonThuoc(ma_don=f"HD{random.randint(1000, 9999)}")
        
        self.title(f"Lập Hóa Đơn - Mã: {self.don_thuoc.ma_don}")
        self.geometry("600x500")
        self.grab_set()
        
        # Chia bố cục giao diện làm 2 vùng trái (nhập liệu) và phải (xem trước hóa đơn)
        left_frame = tk.LabelFrame(self, text="Chọn thuốc bán", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = tk.LabelFrame(self, text="Chi tiết hóa đơn", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # --- BÊN TRÁI: LOGIC CHỌN THUỐC ---
        tk.Label(left_frame, text="Nhập Mã thuốc:").pack(anchor="w")
        self.ent_ma = tk.Entry(left_frame, font=("Arial", 11))
        self.ent_ma.pack(fill=tk.X, pady=5)
        
        tk.Label(left_frame, text="Số lượng mua:").pack(anchor="w")
        self.ent_sl = tk.Entry(left_frame, font=("Arial", 11))
        self.ent_sl.insert(0, "1")
        self.ent_sl.pack(fill=tk.X, pady=5)
        
        btn_add = tk.Button(left_frame, text="THÊM VÀO ĐƠN", bg="#3498db", fg="white", font=("Arial", 10, "bold"), command=self.them_thuoc_vao_don)
        btn_add.pack(fill=tk.X, pady=15)
        
        # --- BÊN PHẢI: HIỂN THỊ HÓA ĐƠN TEXT ---
        self.txt_hoadon = tk.Text(right_frame, font=("Courier New", 10), bg="#f8f9fa")
        self.txt_hoadon.pack(fill=tk.BOTH, expand=True)
        
        btn_pay = tk.Button(right_frame, text="XUẤT & THANH TOÁN", bg="#e67e22", fg="white", font=("Arial", 11, "bold"), command=self.hoan_tat_thanh_toan)
        btn_pay.pack(fill=tk.X, pady=5)
        
        self.cap_nhat_giao_dien_hoa_don()

    def them_thuoc_vao_don(self):
        """Xử lý tra cứu bảng băm và bắt các lỗi nghiêm cấm bán hàng nâng cao."""
        ma = self.ent_ma.get().strip().upper()
        try:
            sl = int(self.ent_sl.get().strip())
            if sl <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi số lượng", "Số lượng mua phải là một số nguyên dương!")
            return
            
        # Tra cứu tối ưu O(1) từ Kho bằng bảng băm qua nạp chồng toán tử __getitem__
        thuoc = self.kho[ma]
        
        if not thuoc:
            messagebox.showerror("Thất bại", f"Không tìm thấy mã thuốc '{ma}' trong kho!")
            return
            
        try:
            # Hàm này sẽ tự kiểm tra hạn dùng & tồn kho để ném ngoại lệ nếu có lỗi
            self.don_thuoc.them_san_pham(thuoc, sl)
            self.cap_nhat_giao_dien_hoa_don()
            self.ent_ma.delete(0, tk.END)
            
        except LoiHetHanSuDung as ex:
            messagebox.showerror("Cấm Bán Thuốc", str(ex)) 
        except LoiHetHang as ex:
            messagebox.showwarning("Kho Không Đủ", str(ex)) 

    def cap_nhat_giao_dien_hoa_don(self):
        """Làm mới lại khung chữ hiển thị hóa đơn xem trước bên phải."""
        self.txt_hoadon.delete("1.0", tk.END)
        self.txt_hoadon.insert(tk.END, self.don_thuoc.xuat_hoa_don_text())

    def hoan_tat_thanh_toan(self):
        """Thực hiện trừ số lượng tồn kho vật lý và ghi file JSON lịch sử đơn hàng."""
        if not self.don_thuoc.danh_sach_mua:
            messagebox.showwarning("Đơn rỗng", "Vui lòng thêm ít nhất một sản phẩm để thanh toán!")
            return
            
        # Thực hiện trừ kho vật lý
        self.don_thuoc.thuc_hiện_tru_kho()
        # Gọi callback để lưu file JSON lưu trữ và cập nhật lại cửa sổ chính
        self.callback_luu_xong(self.don_thuoc)
        
        messagebox.showinfo("Thành công", f"Hóa đơn {self.don_thuoc.ma_don} đã được thanh toán và lưu lịch sử!")
        self.destroy()