class Node:
    """Class untuk merepresentasikan satu node dalam Binary Search Tree."""
    def __init__(self, key):
        self.key = key
        self.left = None   # Pointer ke anak kiri
        self.right = None  # Pointer ke anak kanan


class BinarySearch Tree:
    """Class utama untuk manajemen operasi Binary Search Tree."""
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Fungsi publik untuk menambah data baru ke dalam BST."""
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, current_node, key):
        """Helper function untuk menyisipkan node secara rekursif."""
        if key < current_node.key:
            if current_node.left is None:
                current_node.left = Node(key)
            else:
                self._insert_recursive(current_node.left, key)
        elif key > current_node.key:
            if current_node.right is None:
                current_node.right = Node(key)
            else:
                self._insert_recursive(current_node.right, key)
        # Jika key == current_node.key, data duplikat diabaikan (karakteristik dasar BST)

    def search(self, key):
        """Fungsi publik untuk mencari apakah sebuah key ada di dalam BST."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, current_node, key):
        """Helper function untuk pencarian secara rekursif."""
        # Base Cases: root kosong atau key ditemukan
        if current_node is None or current_node.key == key:
            return current_node is not None

        # Key lebih kecil dari root, cari ke kiri
        if key < current_node.key:
            return self._search_recursive(current_node.left, key)

        # Key lebih besar dari root, cari ke kanan
        return self._search_recursive(current_node.right, key)

    # --- FUNGSI TRAVERSAL (Cetak Data) ---

    def inorder(self):
        """In-order Traversal (Kiri, Root, Kanan) -> Menghasilkan data berurutan."""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, current_node, result):
        if current_node:
            self._inorder_recursive(current_node.left, result)
            result.append(current_node.key)
            self._inorder_recursive(current_node.right, result)

    def preorder(self):
        """Pre-order Traversal (Root, Kiri, Kanan)."""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, current_node, result):
        if current_node:
            result.append(current_node.key)
            self._preorder_recursive(current_node.left, result)
            self._preorder_recursive(current_node.right, result)

    def postorder(self):
        """Post-order Traversal (Kiri, Kanan, Root)."""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, current_node, result):
        if current_node:
            self._postorder_recursive(current_node.left, result)
            self._postorder_recursive(current_node.right, result)
            result.append(current_node.key)


# --- CONTOH PENGGUNAAN MODUL ---
if __name__ == "__main__":
    # 1. Inisialisasi BST baru
    pohon = BinarySearchTree()

    # 2. Memasukkan data contoh
    # Jika diurutkan secara hierarki, 50 akan jadi Root
    data_input = [50, 30, 20, 40, 70, 60, 80]
    print(f"Memasukkan data ke BST: {data_input}")
    
    for angka in data_input:
        pohon.insert(angka)

    print("\n--- HASIL TRAVERSAL ---")
    # Kelebihan In-order pada BST: hasilnya otomatis terurut dari terkecil ke terbesar
    print(f"In-order Traversal   : {pohon.inorder()}")
    print(f"Pre-order Traversal  : {pohon.preorder()}")
    print(f"Post-order Traversal : {pohon.postorder()}")

    print("\n--- UJI PENCARIAN (SEARCH) ---")
    target_cari = 60
    if pohon.search(target_cari):
        print(f"Data {target_cari} ditemukan di dalam BST! ✓")
    else:
        print(f"Data {target_cari} TIDAK ditemukan di dalam BST. ✗")
        
    target_salah = 100
    if pohon.search(target_salah):
        print(f"Data {target_salah} ditemukan di dalam BST! ✓")
    else:
        print(f"Data {target_salah} TIDAK ditemukan di dalam BST. ✗")
