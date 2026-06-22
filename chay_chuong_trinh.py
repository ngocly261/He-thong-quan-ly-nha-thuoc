import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from giao_dien.cua_so_chinh import CuaSoChinh

def main():
    print("--- ĐANG KHỞI ĐỘNG HỆ THỐNG QUẢN LÝ NHÀ THUỐC ---")
    app = CuaSoChinh()
    app.mainloop()
    print("--- HỆ THỐNG ĐÃ ĐÓNG AN TOÀN ---")

if __name__ == "__main__":
    main()