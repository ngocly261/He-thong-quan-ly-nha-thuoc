from datetime import datetime

def parse_date(date_str):
    """Chuyển đổi chuỗi ngày dạng DD/MM/YYYY sang đối tượng datetime để so sánh."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return datetime.min

def heapify(arr, n, i, key_func):
    """Hàm hiệu chỉnh cấu trúc Heap."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and key_func(arr[left]) > key_func(arr[largest]):
        largest = left

    if right < n and key_func(arr[right]) > key_func(arr[largest]):
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, key_func)

def heap_sort(arr, key_func=None):
    """
    Cài đặt thuật toán Heap Sort để sắp xếp danh sách.
    Mặc định sắp xếp thuốc theo hạn sử dụng tăng dần (Sắp hết hạn/Đã hết hạn lên đầu).
    """
    if key_func is None:
        
        key_func = lambda x: parse_date(x.han_su_dung) if hasattr(x, 'han_su_dung') else x

    n = len(arr)


    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, key_func)

    
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, key_func)
        
    return arr