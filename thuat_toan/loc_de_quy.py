def loc_theo_hoat_chat_de_quy(danh_sach_thuoc, hoat_chat, chi_muc=0):
    """
    Sử dụng đệ quy để tìm kiếm và lọc ra các thuốc chứa cùng thành phần hoạt chất.
    """
   
    if chi_muc >= len(danh_sach_thuoc):
        return []
    
    thuoc_hien_tai = danh_sach_thuoc[chi_muc]
    
    chuoi_thanh_phan = thuoc_hien_tai.thanh_phan.lower() if hasattr(thuoc_hien_tai, 'thanh_phan') else ""
    
    ket_qua_tiep_theo = loc_theo_hoat_chat_de_quy(danh_sach_thuoc, hoat_chat, chi_muc + 1)
    
    if hoat_chat.lower() in chuoi_thanh_phan:
        return [thuoc_hien_tai] + ket_qua_tiep_theo
    else:
        return ket_qua_tiep_theo