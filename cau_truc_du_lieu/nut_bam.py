class NutBam:
    """Đại diện cho một nút (Node) trong cấu trúc liên kết để xử lý xung đột (Chaining)[cite: 19]."""
    def __init__(self, key, value):
        self.key = key          
        self.value = value      
        self.next = None       