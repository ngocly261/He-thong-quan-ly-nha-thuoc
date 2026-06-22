import tkinter as tk
from luu_tru.xu_ly_json import doc_lich_su_don_hang

class BieuDoDoanhThu(tk.Frame):
    """Lớp tự vẽ biểu đồ đường hiển thị doanh thu theo ngày bằng Tkinter Canvas."""
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        
        lbl_title = tk.Label(self, text="BIỂU ĐỒ DOANH THU THEO NGÀY", font=("Arial", 14, "bold"), fg="#2c3e50")
        lbl_title.pack(pady=10)
        
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1, highlightbackground="#bdc3c7")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.canvas.bind("<Configure>", lambda event: self.ve_bieu_do())

    def lay_du_lieu_doanh_thu(self):
        """Đọc lịch sử đơn hàng và thống kê tổng doanh thu gom theo ngày."""
        lich_su = doc_lich_su_don_hang()
        thong_ke = {}
        
        for don in lich_su:
            ngay = don["ngay_ke"].split(" ")[0]
            tong_tien = don["tong_tien"]
            thong_ke[ngay] = thong_ke.get(ngay, 0) + tong_tien
            
        cac_ngay_sap_xep = sorted(thong_ke.keys())
        cac_gia_tri = [thong_ke[ngay] for ngay in cac_ngay_sap_xep]
        
        return cac_ngay_sap_xep, cac_gia_tri

    def ve_bieu_do(self):
        """Hàm xử lý vẽ đồ thị đường kết hợp điểm mốc tọa độ trên Canvas."""
        self.canvas.delete("all") 
        
        cac_ngay, cac_doanh_thu = self.lay_du_lieu_doanh_thu()
        
        if not cac_doanh_thu:
            self.canvas.create_text(
                self.canvas.winfo_width() / 2, 
                self.canvas.winfo_height() / 2, 
                text="Chưa có dữ liệu hóa đơn để hiển thị báo cáo.", 
                font=("Arial", 12, "italic"), fill="#7f8c8d"
            )
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        margin_x = 60
        margin_y = 40
        
        plot_w = w - 2 * margin_x
        plot_h = h - 2 * margin_y
        
        max_val = max(cac_doanh_thu) if max(cac_doanh_thu) > 0 else 100000
        min_val = 0
        val_range = max_val - min_val
        
        self.canvas.create_line(margin_x, h - margin_y, w - margin_x, h - margin_y, width=2, fill="#34495e") # Trục X
        self.canvas.create_line(margin_x, margin_y, margin_x, h - margin_y, width=2, fill="#34495e") # Trục Y

        points = []
        num_points = len(cac_doanh_thu)
        
        for i in range(num_points):
            cx = margin_x + (plot_w / (num_points - 1) * i) if num_points > 1 else margin_x + plot_w / 2
            cy = h - margin_y - ((cac_doanh_thu[i] - min_val) / val_range * plot_h)
            points.append((cx, cy))
            
            self.canvas.create_text(cx, h - margin_y + 15, text=cac_ngay[i], font=("Arial", 8), fill="#2c3e50")
            self.canvas.create_text(cx, cy - 12, text=f"{cac_doanh_thu[i]:,.0f}", font=("Arial", 8, "bold"), fill="#27ae60")

        for i in range(num_points):
            if i < num_points - 1:
                self.canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], width=3, fill="#2980b9")
            
            cx, cy = points[i]
            r = 4
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#e74c3c", outline="white", width=1)