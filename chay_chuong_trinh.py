import sys
import os

# Bổ sung đường dẫn thư mục gốc vào hệ thống để tránh lỗi ModuleNotFoundError khi chạy chéo thư mục
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from giao_dien.cua_so_chinh import CuaSoChinh

def main():
    print("--- ĐANG KHỞI ĐỘNG HỆ THỐNG QUẢN LÝ NHÀ THUỐC ---")
    # Khởi tạo đối tượng cửa sổ đồ họa giao diện
    app = CuaSoChinh()
    # Kích hoạt vòng lặp chạy vô tận giữ giao diện đứng vững hiển thị
    app.mainloop()
    print("--- HỆ THỐNG ĐÃ ĐÓNG AN TOÀN ---")

if __name__ == "__main__":
    main()