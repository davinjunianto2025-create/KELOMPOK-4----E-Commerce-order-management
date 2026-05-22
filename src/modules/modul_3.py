"""
=============================================================
MODUL 3 - Graph Rekomendasi (Co-Purchase)
Topik 3: E-Commerce Order Management & Recommendation Engine
ELT60213 Algoritma dan Struktur Data - TA 2025/2026

Struktur Data: Graph tidak berarah berbobot (adjacency list)
Algoritma   : BFS berbasis Queue Linked List (implementasi dari nol)

Deskripsi:
  - Edge (P_i, P_j, w) berarti produk i dan j sering dibeli bersama
    dengan frekuensi co-purchase = w
  - BFS dari produk yang baru dibeli merekomendasikan produk
    terdekat (hop <= 2)
  - Semua struktur data (Queue, Graph) diimplementasi DARI NOL,
    tanpa menggunakan collections.deque atau library sejenis
"""

import time
import random
from typing import Optional

random.seed(99)


# ──────────────────────────────────────────────────────────────
# 1. NODE LINKED LIST  (dipakai oleh Queue maupun adjacency list)
# ──────────────────────────────────────────────────────────────
class LLNode:
    """Node generik untuk Singly Linked List."""

    def __init__(self, data=None):
        self.data = data
        self.next: Optional["LLNode"] = None


# ──────────────────────────────────────────────────────────────
# 2. QUEUE BERBASIS LINKED LIST  (dipakai BFS di dalam graph)
# ──────────────────────────────────────────────────────────────
class Queue:
    """
    FIFO Queue berbasis Singly Linked List.
    Digunakan oleh BFS di dalam GraphRekomendasi.

    Operasi          Big-O
    ─────────────── ──────
    enqueue(data)    O(1)   -- sisip di tail
    dequeue()        O(1)   -- ambil dari head
    peek()           O(1)
    is_empty()       O(1)
    """

    def __init__(self):
        self.head: Optional[LLNode] = None
        self.tail: Optional[LLNode] = None
        self._size: int = 0

    def enqueue(self, data) -> None:
        """Sisipkan data di ekor antrian.  Big-O: O(1)."""
        node = LLNode(data)
        if self.tail is None:          # queue kosong
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def dequeue(self):
        """Ambil dan kembalikan data dari kepala antrian.  Big-O: O(1)."""
        if self.head is None:
            return None
        val = self.head.data
        self.head = self.head.next
        if self.head is None:          # queue menjadi kosong
            self.tail = None
        self._size -= 1
        return val

    def peek(self):
        """Lihat data di kepala tanpa menghapus.  Big-O: O(1)."""
        return self.head.data if self.head else None

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size


# ──────────────────────────────────────────────────────────────
# 3. NODE TETANGGA  (satu slot di adjacency list)
# ──────────────────────────────────────────────────────────────
class NeighborNode:
    """
    Satu entri di adjacency list: menyimpan kode produk tujuan
    dan bobot (frekuensi co-purchase).
    """

    def __init__(self, kode: str, frekuensi: int = 1):
        self.kode = kode
        self.frekuensi = frekuensi
        self.next: Optional["NeighborNode"] = None


# ──────────────────────────────────────────────────────────────
# 4. GRAPH REKOMENDASI
# ──────────────────────────────────────────────────────────────
class GraphRekomendasi:
    """
    Graf tidak berarah berbobot menggunakan adjacency list
    berbasis Linked List.

    Setiap key di self.adj adalah kode_produk (str).
    Value-nya adalah kepala NeighborNode (Linked List tetangga).

    Operasi                  Big-O
    ──────────────────────── ──────────────────────────────────
    inisialisasi_produk(n)   O(n)
    add_copurchase(a, b)     O(deg(a) + deg(b))  -- cari duplikat
    rekomendasikan(k, hop)   O(V + E)            -- BFS
    get_neighbors(k)         O(deg(k))
    tampilkan_graph()        O(V + E)
    """

    def __init__(self):
        # adj[kode] = kepala NeighborNode (None jika belum ada tetangga)
        self.adj: dict[str, Optional[NeighborNode]] = {}

    # ── Inisialisasi node produk ──────────────────────────────
    def inisialisasi_produk(self, kode: str) -> None:
        """
        Daftarkan produk ke graph (tanpa edge).
        Dipanggil saat katalog BST dimuat.
        Big-O: O(1)
        """
        if kode not in self.adj:
            self.adj[kode] = None

    # ── Tambah / tingkatkan bobot edge co-purchase ────────────
    def add_copurchase(self, kode_a: str, kode_b: str) -> None:
        """
        Tambah edge (kode_a, kode_b) atau naikkan bobotnya +1
        jika edge sudah ada.  Graf tidak berarah → dua arah.

        Big-O: O(deg(a) + deg(b))
          -- harus scan linked list untuk cek duplikat
        """
        if kode_a == kode_b:
            return  # self-loop tidak relevan

        # Pastikan kedua node terdaftar
        if kode_a not in self.adj:
            self.adj[kode_a] = None
        if kode_b not in self.adj:
            self.adj[kode_b] = None

        # ---- arah a → b ----
        self._upsert_edge(kode_a, kode_b)
        # ---- arah b → a ----
        self._upsert_edge(kode_b, kode_a)

    def _upsert_edge(self, src: str, dst: str) -> None:
        """
        Bantu: sisipkan atau naikkan bobot edge src→dst.
        Big-O: O(deg(src))
        """
        curr = self.adj[src]
        while curr is not None:
            if curr.kode == dst:
                curr.frekuensi += 1   # sudah ada → naikkan bobot
                return
            curr = curr.next
        # belum ada → sisipkan di depan linked list (O(1) insert)
        new_node = NeighborNode(dst, 1)
        new_node.next = self.adj[src]
        self.adj[src] = new_node

    # ── Ambil semua tetangga ──────────────────────────────────
    def get_neighbors(self, kode: str) -> list[tuple[str, int]]:
        """
        Kembalikan list (kode_tetangga, frekuensi) terurut
        frekuensi descending.
        Big-O: O(deg(kode))
        """
        if kode not in self.adj:
            return []
        result = []
        curr = self.adj[kode]
        while curr is not None:
            result.append((curr.kode, curr.frekuensi))
            curr = curr.next
        # urutkan descending berdasarkan frekuensi (semakin sering, makin relevan)
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    # ── BFS Rekomendasi ───────────────────────────────────────
    def rekomendasikan(
        self, kode_produk: str, max_hop: int = 2
    ) -> list[tuple[str, int, int]]:
        """
        BFS berbasis Queue Linked List hingga kedalaman max_hop.
        Mengembalikan list (kode_produk, frekuensi, hop) yang
        diurutkan: hop ASC, frekuensi DESC.

        Produk sumber TIDAK ikut dalam hasil.

        Big-O: O(V + E)
          V = jumlah produk, E = jumlah edge co-purchase

        Parameter
        ─────────
        kode_produk : kode produk yang baru dibeli
        max_hop     : kedalaman BFS maksimum (default 2)

        Return
        ──────
        list[(kode, frekuensi_ke_sumber, hop)]
        """
        if kode_produk not in self.adj:
            return []

        visited: set[str] = {kode_produk}   # O(1) lookup
        rekomendasi: list[tuple[str, int, int]] = []

        # Queue item: (kode, hop, frekuensi_edge_ke_sumber)
        q = Queue()
        q.enqueue((kode_produk, 0, 0))

        while not q.is_empty():
            kode_curr, hop_curr, freq_curr = q.dequeue()

            if hop_curr >= max_hop:
                continue   # sudah mencapai batas kedalaman

            curr = self.adj.get(kode_curr)
            while curr is not None:
                if curr.kode not in visited:
                    visited.add(curr.kode)
                    hop_baru = hop_curr + 1
                    rekomendasi.append((curr.kode, curr.frekuensi, hop_baru))
                    q.enqueue((curr.kode, hop_baru, curr.frekuensi))
                curr = curr.next

        # Urutkan: hop ASC, lalu frekuensi DESC
        rekomendasi.sort(key=lambda x: (x[2], -x[1]))
        return rekomendasi

    # ── Info graph ────────────────────────────────────────────
    def jumlah_node(self) -> int:
        return len(self.adj)

    def jumlah_edge(self) -> int:
        """Hitung jumlah edge unik (tidak berarah). Big-O: O(V+E)."""
        total = 0
        for kode in self.adj:
            curr = self.adj[kode]
            while curr is not None:
                total += 1
                curr = curr.next
        return total // 2   # tiap edge dihitung dua kali

    def tampilkan_graph(self, maks_tampil: int = 10) -> None:
        """
        Cetak adjacency list (maks_tampil node pertama).
        Big-O: O(V + E)
        """
        print(f"\n{'='*55}")
        print(f"  GRAPH REKOMENDASI CO-PURCHASE")
        print(f"  Node (produk) : {self.jumlah_node()}")
        print(f"  Edge unik     : {self.jumlah_edge()}")
        print(f"{'='*55}")
        count = 0
        for kode, head in self.adj.items():
            if count >= maks_tampil:
                print(f"  ... (dan {self.jumlah_node() - maks_tampil} node lainnya)")
                break
            tetangga = self.get_neighbors(kode)
            if tetangga:
                info = ", ".join(
                    f"{k}(f={f})" for k, f in tetangga[:5]
                )
                print(f"  {kode} → [{info}]")
            count += 1
        print(f"{'='*55}\n")


# ──────────────────────────────────────────────────────────────
# 5. GENERATOR DATA SIMULASI  (seed=99, reproducible)
# ──────────────────────────────────────────────────────────────
def simulasi_copurchase(
    graph: GraphRekomendasi,
    kode_produk_list: list[str],
    n_order: int = 300,
) -> None:
    """
    Simulasikan 300 order acak.  Setiap order memilih 2–4 produk
    secara acak; semua pasangan produk dalam satu order dicatat
    sebagai co-purchase.

    Big-O: O(n_order * k²)  dengan k = produk per order (maks 4)
             ≈ O(n_order)  karena k konstan
    """
    random.seed(99)
    for _ in range(n_order):
        k = random.randint(2, 4)
        produk_dibeli = random.sample(kode_produk_list, k)
        # semua pasangan dalam satu order → co-purchase
        for i in range(len(produk_dibeli)):
            for j in range(i + 1, len(produk_dibeli)):
                graph.add_copurchase(produk_dibeli[i], produk_dibeli[j])


# ──────────────────────────────────────────────────────────────
# 6. EKSPERIMEN RUNTIME  (Big-O verification)
# ──────────────────────────────────────────────────────────────
def eksperimen_runtime(kode_list: list[str]) -> None:
    """
    Ukur waktu eksekusi rekomendasikan() untuk tiga ukuran dataset.
    N = jumlah order simulasi yang membangun graph.
    """
    print("\n" + "="*55)
    print("  EKSPERIMEN RUNTIME - BFS rekomendasikan()")
    print("="*55)
    print(f"  {'N order':>10} | {'Waktu (ms)':>12} | {'Node dijelajahi':>16}")
    print(f"  {'-'*10}-+-{'-'*12}-+-{'-'*16}")

    for n in [50, 200, 300]:
        g = GraphRekomendasi()
        for k in kode_list:
            g.inisialisasi_produk(k)
        simulasi_copurchase(g, kode_list, n_order=n)

        # ukur waktu BFS dari produk pertama
        mulai = time.perf_counter()
        hasil = g.rekomendasikan(kode_list[0], max_hop=2)
        selesai = time.perf_counter()

        waktu_ms = (selesai - mulai) * 1000
        print(f"  {n:>10} | {waktu_ms:>12.4f} | {len(hasil):>16}")

    print("="*55)
    print("  Catatan: BFS O(V+E) → waktu tumbuh linear terhadap E")
    print("="*55 + "\n")


# ──────────────────────────────────────────────────────────────
# 7. DEMO STANDALONE
# ──────────────────────────────────────────────────────────────
def demo():
    print("="*55)
    print("  MODUL 3 - GRAPH REKOMENDASI CO-PURCHASE")
    print("  Topik 3: E-Commerce Order Management")
    print("  ELT60213 Algoritma dan Struktur Data")
    print("="*55)

    # ── Inisialisasi 100 produk (P001–P100) ──────────────────
    kode_list = [f"P{i:03d}" for i in range(1, 101)]

    graph = GraphRekomendasi()
    for k in kode_list:
        graph.inisialisasi_produk(k)

    # ── Simulasi 300 order co-purchase (seed=99) ─────────────
    print("\n[1] Simulasi 300 order co-purchase (seed=99) ...")
    simulasi_copurchase(graph, kode_list, n_order=300)
    print(f"    Graph berhasil dibangun:")
    print(f"      Jumlah node (produk) : {graph.jumlah_node()}")
    print(f"      Jumlah edge unik      : {graph.jumlah_edge()}")
    print(f"    Big-O add_copurchase   : O(deg(u))  per panggilan")

    # ── Tampilkan sebagian adjacency list ────────────────────
    graph.tampilkan_graph(maks_tampil=8)

    # ── Demo BFS Rekomendasi ─────────────────────────────────
    print("[2] Demo BFS Rekomendasi (hop <= 2)")
    for target in ["P001", "P050", "P099"]:
        rekomendasi = graph.rekomendasikan(target, max_hop=2)
        print(f"\n    Produk dibeli : {target}")
        print(f"    Rekomendasi (maks 5 teratas):")
        for kode, freq, hop in rekomendasi[:5]:
            print(f"      hop={hop}  {kode}  frekuensi={freq}")
        print(f"    Total rekomendasi ditemukan : {len(rekomendasi)}")
        print(f"    Big-O rekomendasikan()      : O(V + E)")

    # ── Tambah co-purchase manual ────────────────────────────
    print("\n[3] Tambah co-purchase manual: P010 ↔ P020 (x3)")
    for _ in range(3):
        graph.add_copurchase("P010", "P020")
    neighbors_p010 = graph.get_neighbors("P010")
    p020_info = next((x for x in neighbors_p010 if x[0] == "P020"), None)
    if p020_info:
        print(f"    Edge P010–P020 frekuensi sekarang : {p020_info[1]}")

    # ── Eksperimen Runtime ───────────────────────────────────
    print("\n[4] Eksperimen Runtime")
    eksperimen_runtime(kode_list)

    # ── Ringkasan Big-O ──────────────────────────────────────
    print("="*55)
    print("  RINGKASAN BIG-O MODUL 3 - GRAPH REKOMENDASI")
    print("="*55)
    rows = [
        ("inisialisasi_produk(n)", "O(1) per produk", "O(V)"),
        ("add_copurchase(a, b)",   "O(deg(a)+deg(b))", "O(1)"),
        ("get_neighbors(k)",       "O(deg(k))",         "O(deg(k))"),
        ("rekomendasikan(k, hop)", "O(V + E)",          "O(V)"),
        ("jumlah_edge()",          "O(V + E)",          "O(1)"),
    ]
    print(f"  {'Operasi':<30} {'Waktu':>15} {'Ruang':>8}")
    print(f"  {'-'*30}   {'-'*15}   {'-'*8}")
    for op, wkt, rng in rows:
        print(f"  {op:<30} {wkt:>15} {rng:>8}")
    print("="*55)


if __name__ == "__main__":
    demo()
    
