
# Disediakan dari starter code (Halaman 12) 
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None

# Modul 4: Stack Riwayat Transaksi 
# Dikerjakan oleh: Reino Mifta Saputra (NIM: 25051030088)
class Stack:
    def __init__(self, kapasitas=10):
        self.top: Optional[LLNode] = None
        self.size: int = 0
        self.kapasitas = kapasitas

    def push(self, data) -> bool:
        """Big-O: O(1). Kembalikan False jika kapasitas penuh[cite: 26, 27]."""
        if self.size >= self.kapasitas:
            # Hapus elemen terbawah (implementasi opsional) [cite: 27]
            # Karena batas maksimum riwayat adalah 10 teratas, kita tolak 
            # transaksi ke-11 sesuai return dari starter code.
            return False
            
        # TODO: implementasikan (Diselesaikan)
        new_node = LLNode(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        return True

    def pop(self):
        """Big-O: O(1) untuk fitur UNDO_ORDER """
        # TODO: implementasikan (Diselesaikan)
        if self.top is None:
            return None
            
        node_dihapus = self.top
        self.top = self.top.next
        self.size -= 1
        return node_dihapus.data
        
    def lihat_riwayat(self):
        """
        Fungsi tambahan untuk mendukung CLI E-Commerce: RIWAYAT <cust>.
        Mengembalikan list transaksi untuk dicetak di layar.
        """
        daftar_riwayat = []
        current = self.top
        while current is not None:
            daftar_riwayat.append(current.data)
            current = current.next
        return dafta
      main
