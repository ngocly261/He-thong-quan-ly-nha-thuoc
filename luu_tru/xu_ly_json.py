import json
import os
from mo_hinh.thuoc_ke_don import ThuocKeDon
from mo_hinh.thuoc_khong_ke_don import ThuocKhongKeDon
from mo_hinh.thuc_pham_chuc_nang import ThucPhamChucNang
from mo_hinh.kho_thuoc import KhoThuoc

FILE_THUOC = "du_lieu/danh_muc_thuoc.json"
FILE_DON_HANG = "du_lieu/lich_su_don_hang.json"

def doc_kho_thuoc_tu_json():
    """Đọc dữ liệu từ file danh_muc_thuoc.json và nạp vào đối tượng KhoThuoc (Bảng băm)."""
    kho = KhoThuoc()
    if not os.path.exists(FILE_THUOC):
        return kho

    try:
        with open(FILE_THUOC, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            for ma_thuoc, info in data.items():
                loai = info.get("loai")
                if loai == "ThuocKeDon":
                    thuoc = ThuocKeDon(
                        ma_thuoc=ma_thuoc,
                        ten_thuoc=info["ten_thuoc"],
                        thanh_phan=info["thanh_phan"],
                        don_vi_tinh=info["don_vi_tinh"],
                        gia_nhap=info["gia_nhap"],
                        han_su_dung=info["han_su_dung"],
                        ma_bac_si=info.get("ma_bac_si", ""),
                        canh_bao_lieu_dung=info.get("canh_bao_lieu_dung", ""),
                        so_luong_ton=info.get("so_luong_ton", 0)
                    )
                elif loai == "ThuocKhongKeDon":
                    thuoc = ThuocKhongKeDon(
                        ma_thuoc=ma_thuoc,
                        ten_thuoc=info["ten_thuoc"],
                        thanh_phan=info["thanh_phan"],
                        don_vi_tinh=info["don_vi_tinh"],
                        gia_nhap=info["gia_nhap"],
                        han_su_dung=info["han_su_dung"],
                        so_luong_ton=info.get("so_luong_ton", 0)
                    )
                elif loai == "ThucPhamChucNang":
                    thuoc = ThucPhamChucNang(
                        ma_thuoc=ma_thuoc,
                        ten_thuoc=info["ten_thuoc"],
                        thanh_phan=info["thanh_phan"],
                        don_vi_tinh=info["don_vi_tinh"],
                        gia_nhap=info["gia_nhap"],
                        han_su_dung=info["han_su_dung"],
                        nha_san_xuat=info.get("nha_san_xuat", ""),
                        so_luong_ton=info.get("so_luong_ton", 0)
                    )
                else:
                    continue
                
                kho.them_thuoc(thuoc)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Cảnh báo: Lỗi cấu trúc file dữ liệu thuốc ({e}). Khởi tạo kho trống.")
    return kho

def ghi_kho_thuoc_vao_json(kho_thuoc):
    """Ghi toàn bộ thông tin thuốc hiện tại từ cấu trúc Bảng băm vào file JSON."""
    data = {}
    tat_ca_thuoc = kho_thuoc.lay_tat_ca_thuoc()
    
    for thuoc in tat_ca_thuoc:
        info = {
            "ten_thuoc": thuoc.ten_thuoc,
            "thanh_phan": thuoc.thanh_phan,
            "don_vi_tinh": thuoc.don_vi_tinh,
            "gia_nhap": thuoc.gia_nhap,
            "han_su_dung": thuoc.han_su_dung,
            "so_luong_ton": thuoc.so_luong_ton,
            "loai": thuoc.__class__.__name__
        }
        if isinstance(thuoc, ThuocKeDon):
            info["ma_bac_si"] = thuoc.ma_bac_si
            info["canh_bao_lieu_dung"] = thuoc.canh_bao_lieu_dung
        elif isinstance(thuoc, ThucPhamChucNang):
            info["nha_san_xuat"] = thuoc.nha_san_xuat
            
        data[thuoc.ma_thuoc] = info

    try:
        with open(FILE_THUOC, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Lỗi: Không thể ghi dữ liệu thuốc xuống ổ đĩa ({e}).")

def doc_lich_su_don_hang():
    """Đọc toàn bộ lịch sử các hóa đơn cũ phục vụ việc vẽ biểu đồ báo cáo."""
    if not os.path.exists(FILE_DON_HANG):
        return []
    try:
        with open(FILE_DON_HANG, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def luu_don_hang_vao_lich_su(don_thuoc_obj):
    """Khi xuất hóa đơn xong, lưu thông tin đơn hàng vào lịch sử JSON."""
    lich_su = doc_lich_su_don_hang()
    
    danh_sach_item = []
    for thuoc, so_luong in don_thuoc_obj.danh_sach_mua.items():
        danh_sach_item.append({
            "ma_thuoc": thuoc.ma_thuoc,
            "ten_thuoc": thuoc.ten_thuoc,
            "so_luong": so_luong,
            "gia_ban_luc_do": thuoc.tinh_gia_ban()
        })
        
    don_hang_data = {
        "ma_don": don_thuoc_obj.ma_don,
        "ngay_ke": don_thuoc_obj.ngay_ke,
        "tong_tien": don_thuoc_obj.tinh_tong_tien(),
        "chi_tiet": danh_sach_item
    }
    
    lich_su.append(don_hang_data)
    
    try:
        with open(FILE_DON_HANG, "w", encoding="utf-8") as f:
            json.dump(lich_su, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Lỗi: Không thể ghi dữ liệu hóa đơn xuống ổ đĩa ({e}).")