class TransactionNode:
    """Node untuk menyimpan data setiap transaksi."""
    def __init__(self, data_order):
        self.data = data_order
        self.next = None
        self.prev = None  

class StackRiwayat:
    """Implementasi Stack dari nol untuk menyimpan maksimal 10 transaksi."""
    def __init__(self, limit=10):
        self.top = None
        self.bottom = None
        self.size = 0
        self.limit = limit

    def push(self, data_order):
        """Menambahkan order baru ke tumpukan paling atas. Big-O: O(1)"""
        new_node = TransactionNode(data_order)
        
        if self.size == 0:
            self.top = self.bottom = new_node
        else:
            new_node.next = self.top
            self.top.prev = new_node
            self.top = new_node
        
        self.size += 1

        if self.size > self.limit:
            self.bottom = self.bottom.prev
            self.bottom.next = None
            self.size -= 1

    def pop(self):
        """Mengambil dan menghapus order terakhir (untuk UNDO). Big-O: O(1)"""
        if self.size == 0:
            return None
        
        popped_data = self.top.data
        self.top = self.top.next
        
        if self.top:
            self.top.prev = None
        else:
            self.bottom = None  # Jika stack jadi kosong
            
        self.size -= 1
        return popped_data

    def display_riwayat(self):
        """Menampilkan riwayat dari atas ke bawah. Big-O: O(N) di mana N max 10"""
        if self.size == 0:
            print("  [Kosong] Tidak ada riwayat transaksi.")
            return
            
        current = self.top
        count = 1
        while current and count <= self.limit:
            print(f"  {count}. {current.data}")
            current = current.next
            count += 1


class ECommerceHistoryManager:
    """Manager untuk menangani stack riwayat banyak pelanggan."""
    def __init__(self):
        self.riwayat_pelanggan = {}

    def tambah_order(self, id_pelanggan, detail_order):
        """Menyimulasikan saat pelanggan berhasil membuat order."""
        if id_pelanggan not in self.riwayat_pelanggan:
            self.riwayat_pelanggan[id_pelanggan] = StackRiwayat(limit=10)
            
        self.riwayat_pelanggan[id_pelanggan].push(detail_order)
        print(f"Sukses: Order '{detail_order}' masuk ke riwayat {id_pelanggan}.")

    def undo_order(self, id_pelanggan):
        """Implementasi fitur UNDO_ORDER <pelanggan>"""
        if id_pelanggan not in self.riwayat_pelanggan or self.riwayat_pelanggan[id_pelanggan].size == 0:
            print(f"Gagal: Tidak ada order yang bisa di-undo untuk {id_pelanggan}.")
            return
            
        order_dibatalkan = self.riwayat_pelanggan[id_pelanggan].pop()
        print(f"UNDO_ORDER sukses: Pesanan '{order_dibatalkan}' milik {id_pelanggan} telah dibatalkan.")

    def riwayat(self, id_pelanggan):
        """Implementasi fitur RIWAYAT <pelanggan>"""
        print(f"\n--- RIWAYAT 10 TRANSAKSI TERAKHIR: {id_pelanggan} ---")
        if id_pelanggan not in self.riwayat_pelanggan:
            print("  [Kosong] Tidak ada riwayat transaksi.")
        else:
            self.riwayat_pelanggan[id_pelanggan].display_riwayat()
        print("-" * 45)


# ==========================================
# CONTOH PENGGUNAAN (SIMULASI)
# ==========================================
if __name__ == "__main__":
    sistem_riwayat = ECommerceHistoryManager()

    # Simulasi pelanggan C001 melakukan banyak order
    print(">>> Pelanggan C001 melakukan order...")
    for i in range(1, 13):
        sistem_riwayat.tambah_order("C001", f"Order Produk P0{i:02d}")

    # Cek riwayat (Hanya akan menampilkan 10 terakhir, order P001 dan P002 sudah otomatis terhapus)
    sistem_riwayat.riwayat("C001")

    # Pelanggan C001 melakukan UNDO order terakhirnya
    print("\n>>> Pelanggan C001 melakukan UNDO...")
    sistem_riwayat.undo_order("C001")
    sistem_riwayat.undo_order("C001")

    # Cek riwayat lagi setelah di-undo
    sistem_riwayat.riwayat("C001")