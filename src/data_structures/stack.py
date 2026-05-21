"""
BST Katalog Produk - E-Commerce Order Management & Recommendation Engine
Topik 3 | Domain: Platform Belanja Online

Struktur Data: Binary Search Tree (BST)
Key: kode_produk (P001 - P100)
Setiap node menyimpan: kode, nama, harga, stok

Operasi:
  - insert        : tambah produk baru         -> O(log n) avg
  - search        : cari produk by kode        -> O(log n) avg
  - update_stok   : perbarui stok produk       -> O(log n) avg
  - inorder       : katalog urut by kode       -> O(n)
  - delete        : hapus produk (discontinued) -> O(log n) avg
"""


class ProductNode:
    """Node BST yang merepresentasikan satu produk."""

    def __init__(self, kode: str, nama: str, harga: float, stok: int):
        self.kode  = kode          # primary key
        self.nama  = nama
        self.harga = harga
        self.stok  = stok
        self.left  = None
        self.right = None

    def __repr__(self) -> str:
        return (
            f"[{self.kode}] {self.nama} | "
            f"Harga: Rp{self.harga:,.0f} | Stok: {self.stok}"
        )


class BSTKatalogProduk:
    """
    Binary Search Tree untuk katalog produk e-commerce.
    Urutan berdasarkan kode_produk (string lexicographic).
    """

    def __init__(self):
        self._root = None
        self._size = 0

    # ------------------------------------------------------------------
    # INSERT  ->  O(log n) average, O(n) worst
    # ------------------------------------------------------------------
    def insert(self, kode: str, nama: str, harga: float, stok: int) -> bool:
        """
        Tambahkan produk baru ke katalog.
        Return True jika berhasil, False jika kode sudah ada.
        """
        new_node = ProductNode(kode, nama, harga, stok)
        if self._root is None:
            self._root = new_node
            self._size += 1
            return True

        current = self._root
        while True:
            if kode == current.kode:
                print(f"[BST] Produk '{kode}' sudah ada di katalog.")
                return False
            elif kode < current.kode:
                if current.left is None:
                    current.left = new_node
                    self._size += 1
                    return True
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    self._size += 1
                    return True
                current = current.right

    # ------------------------------------------------------------------
    # SEARCH  ->  O(log n) average
    # ------------------------------------------------------------------
    def search(self, kode: str) -> ProductNode | None:
        """Cari dan kembalikan node produk berdasarkan kode. None jika tidak ada."""
        current = self._root
        while current:
            if kode == current.kode:
                return current
            elif kode < current.kode:
                current = current.left
            else:
                current = current.right
        return None

    # ------------------------------------------------------------------
    # UPDATE STOK  ->  O(log n) average
    # ------------------------------------------------------------------
    def update_stok(self, kode: str, delta: int) -> bool:
        """
        Update stok produk.
        delta positif  -> tambah stok
        delta negatif  -> kurangi stok (tidak boleh < 0)
        Return True jika berhasil.
        """
        node = self.search(kode)
        if node is None:
            print(f"[BST] Produk '{kode}' tidak ditemukan.")
            return False
        new_stok = node.stok + delta
        if new_stok < 0:
            print(f"[BST] Stok tidak cukup. Stok saat ini: {node.stok}")
            return False
        node.stok = new_stok
        return True

    # ------------------------------------------------------------------
    # INORDER (katalog terurut)  ->  O(n)
    # ------------------------------------------------------------------
    def inorder(self) -> list[ProductNode]:
        """Kembalikan daftar produk terurut ascending by kode_produk."""
        result: list[ProductNode] = []
        self._inorder_recursive(self._root, result)
        return result

    def _inorder_recursive(self, node: ProductNode | None, result: list):
        if node is None:
            return
        self._inorder_recursive(node.left, result)
        result.append(node)
        self._inorder_recursive(node.right, result)

    def print_katalog(self):
        """Tampilkan seluruh katalog terurut by kode."""
        items = self.inorder()
        if not items:
            print("[BST] Katalog kosong.")
            return
        print(f"\n{'='*55}")
        print(f"{'KATALOG PRODUK':^55}")
        print(f"{'='*55}")
        for item in items:
            print(f"  {item}")
        print(f"{'='*55}")
        print(f"  Total produk: {self._size}")

    # ------------------------------------------------------------------
    # DELETE  ->  O(log n) average
    # ------------------------------------------------------------------
    def delete(self, kode: str) -> bool:
        """
        Hapus produk dari katalog (discontinued).
        Return True jika berhasil.
        """
        self._root, deleted = self._delete_recursive(self._root, kode)
        if deleted:
            self._size -= 1
        else:
            print(f"[BST] Produk '{kode}' tidak ditemukan.")
        return deleted

    def _delete_recursive(
        self, node: ProductNode | None, kode: str
    ) -> tuple[ProductNode | None, bool]:
        if node is None:
            return None, False

        deleted = False
        if kode < node.kode:
            node.left, deleted = self._delete_recursive(node.left, kode)
        elif kode > node.kode:
            node.right, deleted = self._delete_recursive(node.right, kode)
        else:
            # Node ditemukan — 3 kasus
            deleted = True
            if node.left is None:
                return node.right, deleted
            elif node.right is None:
                return node.left, deleted
            else:
                # Ganti dengan in-order successor (node terkecil di subtree kanan)
                successor = self._find_min(node.right)
                node.kode  = successor.kode
                node.nama  = successor.nama
                node.harga = successor.harga
                node.stok  = successor.stok
                node.right, _ = self._delete_recursive(node.right, successor.kode)

        return node, deleted

    def _find_min(self, node: ProductNode) -> ProductNode:
        while node.left:
            node = node.left
        return node

    # ------------------------------------------------------------------
    # UTILITY
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0


# ======================================================================
# DEMO / QUICK TEST
# ======================================================================
if __name__ == "__main__":
    katalog = BSTKatalogProduk()

    # Seed data produk
    produk_data = [
        ("P050", "Laptop Gaming",     15_000_000, 10),
        ("P010", "Mouse Wireless",       250_000, 50),
        ("P075", "Monitor 27 inch",    4_500_000, 8),
        ("P001", "Keyboard Mekanikal",   850_000, 30),
        ("P090", "Headset Bluetooth",    600_000, 20),
        ("P030", "Webcam HD",            450_000, 15),
    ]
    for kode, nama, harga, stok in produk_data:
        katalog.insert(kode, nama, harga, stok)

    # Tampilkan katalog inorder
    katalog.print_katalog()

    # Search
    print("\n[SEARCH P030]")
    node = katalog.search("P030")
    print(f"  Ditemukan: {node}" if node else "  Tidak ditemukan.")

    # Update stok
    print("\n[UPDATE STOK P010 -5]")
    katalog.update_stok("P010", -5)
    print(f"  Stok baru P010: {katalog.search('P010').stok}")

    # Delete
    print("\n[DELETE P075]")
    katalog.delete("P075")
    katalog.print_katalog()
