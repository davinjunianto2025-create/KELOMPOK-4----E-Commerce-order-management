class ProductNode:
    """Node untuk menyimpan data setiap produk dalam BST."""
    def __init__(self, kode, nama, harga, stok):
        self.kode = kode
        self.nama = nama
        self.harga = harga
        self.stok = stok
        self.left = None
        self.right = None

class BSTKatalog:
    """Implementasi BST untuk Katalog Produk."""
    def __init__(self):
        self.root = None

    def insert(self, kode, nama, harga, stok):
        """Menambahkan produk baru. Big-O Rata-rata: O(log n)"""
        if self.root is None:
            self.root = ProductNode(kode, nama, harga, stok)
        else:
            self._insert_recursive(self.root, kode, nama, harga, stok)

    def _insert_recursive(self, node, kode, nama, harga, stok):
        if kode < node.kode:
            if node.left is None:
                node.left = ProductNode(kode, nama, harga, stok)
            else:
                self._insert_recursive(node.left, kode, nama, harga, stok)
        elif kode > node.kode:
            if node.right is None:
                node.right = ProductNode(kode, nama, harga, stok)
            else:
                self._insert_recursive(node.right, kode, nama, harga, stok)
        else:
            node.stok += stok

    def search(self, kode):
        """Mencari produk berdasarkan kode. Big-O Rata-rata: O(log n)"""
        return self._search_recursive(self.root, kode)

    def _search_recursive(self, node, kode):
        if node is None or node.kode == kode:
            return node
        
        if kode < node.kode:
            return self._search_recursive(node.left, kode)
        
        return self._search_recursive(node.right, kode)

    def update_stok(self, kode, qty_change):
        """
        Mengupdate stok produk (bisa bertambah atau berkurang).
        Sesuai spesifikasi: Jika stok habis (<= 0), produk akan dihapus (delete).
        """
        node = self.search(kode)
        if node:
            node.stok += qty_change
            if node.stok <= 0:
                print(f"Peringatan: Stok {kode} habis. Menghapus produk dari katalog...")
                self.delete(kode)
            else:
                print(f"Sukses: Stok {kode} diupdate menjadi {node.stok}.")
            return True
        else:
            print(f"Gagal: Produk dengan kode {kode} tidak ditemukan.")
            return False

    def delete(self, kode):
        """Menghapus produk dari katalog. Big-O Rata-rata: O(log n)"""
        self.root = self._delete_recursive(self.root, kode)

    def _delete_recursive(self, node, kode):
        if node is None:
            return node

        if kode < node.kode:
            node.left = self._delete_recursive(node.left, kode)
        elif kode > node.kode:
            node.right = self._delete_recursive(node.right, kode)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._get_min_value_node(node.right)
            
            node.kode = temp.kode
            node.nama = temp.nama
            node.harga = temp.harga
            node.stok = temp.stok
            
            node.right = self._delete_recursive(node.right, temp.kode)

        return node

    def _get_min_value_node(self, node):
        """Mencari node dengan nilai terkecil (paling kiri)"""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        """Menampilkan katalog terurut berdasarkan kode produk. Big-O: O(N)"""
        print("\n" + "="*60)
        print(f"{'KODE':<8} | {'NAMA PRODUK':<25} | {'HARGA':<10} | {'STOK'}")
        print("="*60)
        self._inorder_recursive(self.root)
        print("="*60 + "\n")

    def _inorder_recursive(self, node):
        if node is not None:
            self._inorder_recursive(node.left)
            print(f"{node.kode:<8} | {node.nama:<25} | Rp{node.harga:<8} | {node.stok}")
            self._inorder_recursive(node.right)


# ==========================================
# CONTOH PENGGUNAAN (SIMULASI)
# ==========================================
if __name__ == "__main__":
    katalog = BSTKatalog()

    # 1. INSERT Data (Diacak agar BST seimbang)
    katalog.insert("P050", "Sepatu Asics Novablast", 1500000, 10)
    katalog.insert("P025", "Kemeja Coklat", 250000, 15)
    katalog.insert("P075", "Celana Chino Cream", 300000, 20)
    katalog.insert("P010", "Kaos Polos Hitam", 75000, 50)
    katalog.insert("P030", "Jaket Hoodie Hijau", 450000, 5)

    # 2. Tampilkan Katalog (Inorder: P010 -> P025 -> P030 -> P050 -> P075)
    print(">>> Menampilkan Katalog Awal:")
    katalog.inorder()

    # 3. SEARCH
    cari = katalog.search("P050")
    if cari:
        print(f">>> Ditemukan: {cari.nama} harganya Rp{cari.harga}")

    # 4. UPDATE STOK
    print("\n>>> Mengurangi stok P025 sebanyak 5...")
    katalog.update_stok("P025", -5)

    # 5. DELETE (Otomatis saat stok habis)
    print("\n>>> Mengurangi stok P030 sebanyak 5 (stok jadi 0)...")
    katalog.update_stok("P030", -5)

    # Tampilkan Katalog Akhir
    print("\n>>> Menampilkan Katalog Akhir (P030 harusnya hilang):")
    katalog.inorder()