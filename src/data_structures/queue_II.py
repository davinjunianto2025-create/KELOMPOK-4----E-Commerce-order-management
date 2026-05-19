class QueueNode:
    """Node untuk menyimpan data setiap order dalam Queue."""
    def _init_(self, id_pelanggan, kode_produk, tier):
        self.id_pelanggan = id_pelanggan
        self.kode_produk = kode_produk
        self.tier = tier  # PREMIUM, REGULAR, atau ECONOMY
        self.next = None

class QueueLinkedList:
    """Implementasi Queue berbasis Linked List dari nol."""
    def _init_(self):
        self.head = None  # Menunjuk ke elemen paling depan (yang akan di-serve)
        self.tail = None  # Menunjuk ke elemen paling belakang (tempat data baru masuk)
        self.size = 0

    def is_empty(self):
        """Memeriksa apakah antrean kosong."""
        return self.head is None

    def enqueue(self, id_pelanggan, kode_produk, tier):
        """Menambahkan order baru ke antrean paling belakang. Big-O: O(1)"""
        new_node = QueueNode(id_pelanggan, kode_produk, tier)
        
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
            
        self.size += 1

    def dequeue(self):
        """Mengambil dan menghapus order dari antrean paling depan. Big-O: O(1)"""
        if self.is_empty():
            return None
        
        removed_node = self.head
        self.head = self.head.next
        
        # Jika setelah dihapus queue menjadi kosong
        if self.head is None:
            self.tail = None
            
        self.size -= 1
        return removed_node

    def display_queue(self):
        """Menampilkan semua isi antrean saat ini. Big-O: O(N)"""
        if self.is_empty():
            print("  [Kosong] Tidak ada antrean.")
            return
            
        current = self.head
        count = 1
        while current:
            print(f"  {count}. [{current.tier}] Pelanggan: {current.id_pelanggan} -> Produk: {current.kode_produk}")
            current = current.next


# ==========================================
# CONTOH PENGGUNAAN (SIMULASI MODUL 1)
# ==========================================
if __name__ == "__main__":
    # Membuat objek Antrean
    antrean_toko = QueueLinkedList()

    print(">>> Menyimulasikan Masuknya Order (Enqueue)...")
    # Contoh data sesuai format spesifikasi: ORDER <pelanggan> <produk> <tier>
    antrean_toko.enqueue("C001", "P050", "PREMIUM")
    antrean_toko.enqueue("C002", "P010", "REGULAR")
    antrean_toko.enqueue("C003", "P075", "ECONOMY")

    print("\n--- DAFTAR ANTREAN SAAT INI ---")
    antrean_toko.display_queue()

    print("\n>>> Melakukan Pelayanan Order (Serve / Dequeue)...")
    served_order = antrean_toko.dequeue()
    if served_order:
        print(f"Sukses SERVE: Melayani order milik {served_order.id_pelanggan} ([{served_order.tier}] Produk: {served_order.kode_produk})")

    print("\n--- DAFTAR ANTREAN SETELAH SERVE ---")
    antrean_toko.display_queue()