"""
CLI E-Commerce Order Management & Recommendation Engine
Topik 3 – Domain: Platform Belanja Online
Struktur Data: Queue (Priority), BST, Graph, Stack
"""

import heapq
import random
from collections import defaultdict, deque
from datetime import datetime, timedelta

random.seed(99)

# ─────────────────────────────────────────────
# PARAMETER SISTEM
# ─────────────────────────────────────────────
JUMLAH_PRODUK   = 100          # P001–P100
JUMLAH_PELANGGAN = 50          # C001–C050
ORDER_SIMULASI  = 300
TIER_MAP        = {"PREMIUM": 0, "REGULAR": 1, "ECONOMY": 2}
TIER_LIST       = ["PREMIUM", "REGULAR", "ECONOMY"]

NAMA_PRODUK_POOL = [
    "Laptop", "Mouse", "Keyboard", "Monitor", "Headphone",
    "SSD", "RAM", "GPU", "CPU", "Webcam",
    "Charger", "Kabel", "Hub USB", "Printer", "Scanner",
    "Speaker", "Microphone", "Router", "Switch", "Modem",
    "Flashdisk", "HDD", "Powerbank", "Earphone", "Smartwatch"
]

# ─────────────────────────────────────────────
# 1. BST – KATALOG PRODUK
# ─────────────────────────────────────────────
class BSTNode:
    def __init__(self, kode, nama, harga, stok):
        self.kode  = kode
        self.nama  = nama
        self.harga = harga
        self.stok  = stok
        self.left  = None
        self.right = None


class BST:
    """Binary Search Tree untuk katalog produk. Key = kode produk (string)."""

    def __init__(self):
        self.root = None

    # INSERT – O(log n) average, O(n) worst
    def insert(self, kode, nama, harga, stok):
        self.root = self._insert(self.root, kode, nama, harga, stok)

    def _insert(self, node, kode, nama, harga, stok):
        if node is None:
            return BSTNode(kode, nama, harga, stok)
        if kode < node.kode:
            node.left  = self._insert(node.left,  kode, nama, harga, stok)
        elif kode > node.kode:
            node.right = self._insert(node.right, kode, nama, harga, stok)
        else:
            # update
            node.nama  = nama
            node.harga = harga
            node.stok  = stok
        return node

    # SEARCH – O(log n) average
    def search(self, kode):
        return self._search(self.root, kode)

    def _search(self, node, kode):
        if node is None or node.kode == kode:
            return node
        if kode < node.kode:
            return self._search(node.left, kode)
        return self._search(node.right, kode)

    # UPDATE STOK – O(log n)
    def update_stok(self, kode, qty):
        node = self.search(kode)
        if node:
            node.stok += qty
            return True
        return False

    # IN-ORDER (untuk laporan) – O(n)
    def inorder(self):
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, node, hasil):
        if node:
            self._inorder(node.left, hasil)
            hasil.append(node)
            self._inorder(node.right, hasil)


# ─────────────────────────────────────────────
# 2. PRIORITY QUEUE – ORDER MANAGEMENT
# ─────────────────────────────────────────────
class PriorityQueue:
    """
    Min-heap berdasarkan (tier_priority, timestamp, order_id).
    PREMIUM=0, REGULAR=1, ECONOMY=2
    Enqueue: O(log n) | Dequeue: O(log n) | Peek: O(1)
    """

    def __init__(self):
        self._heap    = []
        self._counter = 0   # tie-breaker urutan masuk

    def enqueue(self, order):
        tier_p = TIER_MAP.get(order["tier"], 2)
        heapq.heappush(self._heap, (tier_p, self._counter, order))
        self._counter += 1

    def dequeue(self):
        if self._heap:
            _, _, order = heapq.heappop(self._heap)
            return order
        return None

    def peek(self):
        if self._heap:
            return self._heap[0][2]
        return None

    def is_empty(self):
        return len(self._heap) == 0

    def size(self):
        return len(self._heap)


# ─────────────────────────────────────────────
# 3. STACK – RIWAYAT ORDER (untuk CANCEL_LAST)
# ─────────────────────────────────────────────
class Stack:
    """
    Stack berbasis list Python.
    Push: O(1) | Pop: O(1) | Peek: O(1)
    """

    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self._data:
            return self._data.pop()
        return None

    def peek(self):
        if self._data:
            return self._data[-1]
        return None

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def get_history(self, cust=None):
        if cust is None:
            return list(reversed(self._data))
        return [o for o in reversed(self._data) if o["cust"] == cust]


# ─────────────────────────────────────────────
# 4. GRAPH – REKOMENDASI CO-PURCHASE
# ─────────────────────────────────────────────
class Graph:
    """
    Undirected weighted graph: node = kode_produk, edge = co-purchase count.
    Add edge: O(1) | Get neighbors: O(degree) | Rekomendasi: O(degree log degree)
    """

    def __init__(self):
        self._adj = defaultdict(lambda: defaultdict(int))

    def add_copurchase(self, prod_a, prod_b):
        if prod_a != prod_b:
            self._adj[prod_a][prod_b] += 1
            self._adj[prod_b][prod_a] += 1

    def get_rekomendasi(self, kode_produk, top_k=5):
        """Kembalikan top-k produk yang paling sering dibeli bersama kode_produk."""
        if kode_produk not in self._adj:
            return []
        neighbors = self._adj[kode_produk]
        sorted_nb = sorted(neighbors.items(), key=lambda x: -x[1])
        return sorted_nb[:top_k]


# ─────────────────────────────────────────────
# INISIALISASI DATA
# ─────────────────────────────────────────────
def init_data():
    katalog  = BST()
    pq       = PriorityQueue()
    stack    = Stack()
    graf     = Graph()

    # Generate 100 produk
    for i in range(1, JUMLAH_PRODUK + 1):
        kode  = f"P{i:03d}"
        nama  = random.choice(NAMA_PRODUK_POOL) + f" {i}"
        harga = random.randint(50_000, 4_999_999)   # inklusif kedua ujung
        stok  = random.randint(10, 199)
        katalog.insert(kode, nama, harga, stok)

    # Generate 300 order simulasi
    order_id_counter = [1]
    base_time = datetime(2024, 1, 1, 8, 0, 0)

    served_orders = []   # untuk build graph co-purchase

    for i in range(ORDER_SIMULASI):
        cust  = f"C{random.randint(1, JUMLAH_PELANGGAN):03d}"
        prod  = f"P{random.randint(1, JUMLAH_PRODUK):03d}"
        tier  = random.choice(TIER_LIST)
        qty   = random.randint(1, 4)
        ts    = base_time + timedelta(minutes=i * 3)

        order = {
            "id"    : f"ORD{order_id_counter[0]:04d}",
            "cust"  : cust,
            "prod"  : prod,
            "tier"  : tier,
            "qty"   : qty,
            "ts"    : ts.strftime("%Y-%m-%d %H:%M"),
            "status": "PENDING"
        }
        order_id_counter[0] += 1
        pq.enqueue(order)

    # Serve semua order simulasi untuk isi stack & graph
    while not pq.is_empty():
        o = pq.dequeue()
        o["status"] = "SERVED"
        stack.push(o)
        served_orders.append(o)

    # Build co-purchase graph dari order pelanggan yang sama
    cust_orders = defaultdict(list)
    for o in served_orders:
        cust_orders[o["cust"]].append(o["prod"])

    for cust, prods in cust_orders.items():
        for j in range(len(prods)):
            for k in range(j + 1, len(prods)):
                graf.add_copurchase(prods[j], prods[k])

    return katalog, pq, stack, graf, order_id_counter


# ─────────────────────────────────────────────
# HELPER PRINT
# ─────────────────────────────────────────────
SEPARATOR = "=" * 62

def header(title):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)

def bigo(op, complexity):
    print(f"  [Big-O] {op}: {complexity}")


# ─────────────────────────────────────────────
# OPERASI CLI
# ─────────────────────────────────────────────

def cmd_order(args, pq, katalog, order_counter):
    """ORDER <cust> <prod> <tier>  – Tambah order ke priority queue."""
    if len(args) < 3:
        print("  Usage: ORDER <cust> <prod> <tier>")
        bigo("ORDER (enqueue)", "O(log n)")
        return
    cust, prod, tier = args[0].upper(), args[1].upper(), args[2].upper()
    if tier not in TIER_MAP:
        print(f"  Tier tidak valid. Pilih: PREMIUM, REGULAR, ECONOMY")
        return
    node = katalog.search(prod)
    if not node:
        print(f"  Produk {prod} tidak ditemukan di katalog.")
        bigo("ORDER (enqueue)", "O(log n)")
        return
    order = {
        "id"    : f"ORD{order_counter[0]:04d}",
        "cust"  : cust,
        "prod"  : prod,
        "tier"  : tier,
        "qty"   : 1,
        "ts"    : datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "PENDING"
    }
    order_counter[0] += 1
    pq.enqueue(order)
    print(f"  ✓ Order {order['id']} ditambahkan.")
    print(f"    Pelanggan : {cust}  |  Produk : {prod} ({node.nama})")
    print(f"    Tier      : {tier}  |  Antrian saat ini: {pq.size()} order")
    bigo("ORDER (enqueue)", "O(log n)")


def cmd_serve(pq, stack, katalog):
    """SERVE – Proses order dengan prioritas tertinggi."""
    if pq.is_empty():
        print("  Antrian kosong. Tidak ada order untuk diproses.")
        bigo("SERVE (dequeue)", "O(log n)")
        return
    order = pq.dequeue()
    order["status"] = "SERVED"
    stack.push(order)
    node = katalog.search(order["prod"])
    nama_prod = node.nama if node else order["prod"]
    print(f"  ✓ Order {order['id']} DIPROSES.")
    print(f"    Pelanggan : {order['cust']}  |  Tier   : {order['tier']}")
    print(f"    Produk    : {order['prod']} ({nama_prod})")
    print(f"    Sisa antrian: {pq.size()} order")
    bigo("SERVE (dequeue)", "O(log n)")


def cmd_cancel_last(stack, pq):
    """CANCEL_LAST – Batalkan order terakhir yang diproses (pop dari stack)."""
    if stack.is_empty():
        print("  Tidak ada order yang bisa dibatalkan.")
        bigo("CANCEL_LAST (stack pop)", "O(1)")
        return
    order = stack.pop()
    order["status"] = "CANCELLED"
    # Masukkan kembali ke queue jika mau re-proses
    pq.enqueue(order)
    print(f"  ✓ Order {order['id']} DIBATALKAN dan dikembalikan ke antrian.")
    print(f"    Pelanggan : {order['cust']}  |  Tier : {order['tier']}")
    print(f"    Produk    : {order['prod']}")
    bigo("CANCEL_LAST (stack pop + re-enqueue)", "O(1) + O(log n)")


def cmd_cari_produk(args, katalog):
    """CARI_PRODUK <kode> – Cari produk di BST."""
    if not args:
        print("  Usage: CARI_PRODUK <kode>")
        bigo("CARI_PRODUK (BST search)", "O(log n)")
        return
    kode = args[0].upper()
    node = katalog.search(kode)
    if node:
        print(f"  ✓ Produk ditemukan:")
        print(f"    Kode  : {node.kode}")
        print(f"    Nama  : {node.nama}")
        print(f"    Harga : Rp {node.harga:,.0f}")
        print(f"    Stok  : {node.stok} unit")
    else:
        print(f"  ✗ Produk {kode} tidak ditemukan.")
    bigo("CARI_PRODUK (BST search)", "O(log n)")


def cmd_update_stok(args, katalog):
    """UPDATE_STOK <kode> <qty> – Update stok produk (qty bisa negatif)."""
    if len(args) < 2:
        print("  Usage: UPDATE_STOK <kode> <qty>")
        bigo("UPDATE_STOK (BST search + update)", "O(log n)")
        return
    kode = args[0].upper()
    try:
        qty = int(args[1])
    except ValueError:
        print("  qty harus berupa angka integer.")
        return
    node = katalog.search(kode)
    if not node:
        print(f"  ✗ Produk {kode} tidak ditemukan.")
        bigo("UPDATE_STOK", "O(log n)")
        return
    stok_lama = node.stok
    success = katalog.update_stok(kode, qty)
    if success:
        print(f"  ✓ Stok {kode} ({node.nama}) diperbarui.")
        print(f"    Stok lama : {stok_lama}  →  Stok baru : {node.stok}")
    bigo("UPDATE_STOK (BST search + update)", "O(log n)")


def cmd_rekomendasi(args, graf, katalog):
    """REKOMENDASI <kode_produk> – Top-5 produk co-purchase."""
    if not args:
        print("  Usage: REKOMENDASI <kode_produk>")
        bigo("REKOMENDASI (graph neighbor sort)", "O(degree · log degree)")
        return
    kode = args[0].upper()
    node = katalog.search(kode)
    if not node:
        print(f"  ✗ Produk {kode} tidak ditemukan di katalog.")
        bigo("REKOMENDASI", "O(degree · log degree)")
        return
    rekomen = graf.get_rekomendasi(kode, top_k=5)
    print(f"  Rekomendasi co-purchase untuk {kode} ({node.nama}):")
    if not rekomen:
        print("  Belum ada data co-purchase untuk produk ini.")
    else:
        for rank, (prod, count) in enumerate(rekomen, 1):
            n = katalog.search(prod)
            nama = n.nama if n else prod
            print(f"    {rank}. {prod} – {nama}  (dibeli bersama {count}x)")
    bigo("REKOMENDASI (graph neighbor sort)", "O(degree · log degree)")


def cmd_riwayat(args, stack, katalog):
    """RIWAYAT <cust> – Tampilkan riwayat order pelanggan dari stack."""
    if not args:
        print("  Usage: RIWAYAT <cust>")
        bigo("RIWAYAT (stack scan)", "O(n)")
        return
    cust = args[0].upper()
    history = stack.get_history(cust)
    print(f"  Riwayat order pelanggan {cust}:")
    if not history:
        print("  Belum ada riwayat order.")
    else:
        print(f"  {'No':<4} {'Order ID':<10} {'Produk':<8} {'Tier':<10} {'Qty':<5} {'Status':<12} {'Waktu'}")
        print("  " + "-" * 64)
        for i, o in enumerate(history[:20], 1):   # tampilkan maks 20
            node = katalog.search(o["prod"])
            nama = (node.nama[:10] + "..") if node and len(node.nama) > 10 else (node.nama if node else o["prod"])
            print(f"  {i:<4} {o['id']:<10} {o['prod']:<8} {o['tier']:<10} {o['qty']:<5} {o['status']:<12} {o['ts']}")
        if len(history) > 20:
            print(f"  ... dan {len(history)-20} order lainnya.")
    bigo("RIWAYAT (stack scan)", "O(n)")


def cmd_laporan_harian(stack, katalog, pq):
    """LAPORAN_HARIAN – Ringkasan statistik sistem hari ini."""
    header("LAPORAN HARIAN SISTEM E-COMMERCE")

    history = stack.get_history()
    total_served    = len([o for o in history if o["status"] == "SERVED"])
    total_cancelled = len([o for o in history if o["status"] == "CANCELLED"])

    # Hitung per tier
    tier_count = defaultdict(int)
    for o in history:
        tier_count[o["tier"]] += 1

    # Top 5 produk terlaris
    prod_count = defaultdict(int)
    for o in history:
        prod_count[o["prod"]] += o.get("qty", 1)
    top5 = sorted(prod_count.items(), key=lambda x: -x[1])[:5]

    # Top 5 pelanggan aktif
    cust_count = defaultdict(int)
    for o in history:
        cust_count[o["cust"]] += 1
    top5_cust = sorted(cust_count.items(), key=lambda x: -x[1])[:5]

    print(f"\n  Total order diproses   : {total_served}")
    print(f"  Total order dibatalkan : {total_cancelled}")
    print(f"  Order dalam antrian    : {pq.size()}")

    print(f"\n  Order per Tier:")
    for tier in TIER_LIST:
        print(f"    {tier:<10}: {tier_count.get(tier, 0)} order")

    print(f"\n  Top 5 Produk Terlaris:")
    for rank, (prod, qty) in enumerate(top5, 1):
        node = katalog.search(prod)
        nama = node.nama if node else prod
        print(f"    {rank}. {prod} – {nama} ({qty} unit)")

    print(f"\n  Top 5 Pelanggan Teraktif:")
    for rank, (cust, cnt) in enumerate(top5_cust, 1):
        print(f"    {rank}. {cust} – {cnt} order")

    # Katalog: stok rendah
    semua = katalog.inorder()
    rendah = [n for n in semua if n.stok < 20]
    print(f"\n  Produk stok rendah (<20 unit): {len(rendah)} produk")
    for n in rendah[:5]:
        print(f"    {n.kode} – {n.nama} (stok: {n.stok})")
    if len(rendah) > 5:
        print(f"    ... dan {len(rendah)-5} lainnya.")

    bigo("LAPORAN_HARIAN (queue size O(1), stack scan O(n), BST inorder O(n))", "O(n)")


# ─────────────────────────────────────────────
# BANTUAN
# ─────────────────────────────────────────────
HELP_TEXT = """
  DAFTAR PERINTAH:
  ─────────────────────────────────────────────────────────────
  ORDER <cust> <prod> <tier>   Tambah order ke antrian
                               Tier: PREMIUM | REGULAR | ECONOMY
  SERVE                        Proses order prioritas tertinggi
  CANCEL_LAST                  Batalkan order terakhir diproses
  CARI_PRODUK <kode>           Cari produk di katalog (BST)
  UPDATE_STOK <kode> <qty>     Update stok (+/- qty)
  REKOMENDASI <kode_produk>    Lihat rekomendasi co-purchase
  RIWAYAT <cust>               Riwayat order pelanggan
  LAPORAN_HARIAN               Laporan statistik sistem
  BANTUAN                      Tampilkan menu ini
  KELUAR                       Keluar dari aplikasi
  ─────────────────────────────────────────────────────────────
  Contoh:
    ORDER C001 P005 PREMIUM
    CARI_PRODUK P010
    UPDATE_STOK P010 -5
    REKOMENDASI P010
    RIWAYAT C001
"""

# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────
def main():
    print(SEPARATOR)
    print("  CLI E-COMMERCE – Order Management & Recommendation")
    print("  Topik 3 | Struktur Data: Queue, BST, Graph, Stack")
    print(SEPARATOR)
    print("  Menginisialisasi data sistem...")

    katalog, pq, stack, graf, order_counter = init_data()

    print(f"  ✓ {JUMLAH_PRODUK} produk dimuat ke BST.")
    print(f"  ✓ {ORDER_SIMULASI} order simulasi diproses (seed=99).")
    print(f"  ✓ Graf rekomendasi co-purchase dibangun.")
    print(f"  ✓ Riwayat order tersimpan di Stack ({stack.size()} entri).")
    print(f"\n  Ketik BANTUAN untuk melihat daftar perintah.")
    print(SEPARATOR)

    while True:
        try:
            raw = input("\n  e-commerce> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Sesi diakhiri.")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd   = parts[0].upper()
        args  = parts[1:]

        print()  # spacing

        if cmd == "ORDER":
            cmd_order(args, pq, katalog, order_counter)

        elif cmd == "SERVE":
            cmd_serve(pq, stack, katalog)

        elif cmd == "CANCEL_LAST":
            cmd_cancel_last(stack, pq)

        elif cmd == "CARI_PRODUK":
            cmd_cari_produk(args, katalog)

        elif cmd == "UPDATE_STOK":
            cmd_update_stok(args, katalog)

        elif cmd == "REKOMENDASI":
            cmd_rekomendasi(args, graf, katalog)

        elif cmd == "RIWAYAT":
            cmd_riwayat(args, stack, katalog)

        elif cmd == "LAPORAN_HARIAN":
            cmd_laporan_harian(stack, katalog, pq)

        elif cmd in ("BANTUAN", "HELP", "?"):
            print(HELP_TEXT)

        elif cmd == "KELUAR":
            print("  Sampai jumpa! Sistem ditutup.")
            break

        else:
            print(f"  Perintah '{cmd}' tidak dikenali. Ketik BANTUAN untuk bantuan.")


if __name__ == "__main__":
    main()