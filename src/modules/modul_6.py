"""
modul_6.py - CLI E-Commerce
E-Commerce Order Management & Recommendation Engine
Topik 3 | src/modules/modul_6.py

Perintah yang didukung:
  ORDER <cust> <prod> <tier>    -> tambah order ke antrian       O(1)
  SERVE                         -> layani order tertinggi         O(1)
  CANCEL_LAST                   -> batalkan order terakhir (Stack) O(1)
  CARI_PRODUK <kode>            -> cari produk di BST             O(log n)
  UPDATE_STOK <kode> <qty>      -> update stok produk             O(log n)
  REKOMENDASI <kode_produk>     -> rekomendasi via BFS Graph      O(V+E)
  RIWAYAT <cust>                -> riwayat 10 transaksi terakhir  O(n)
  LAPORAN_HARIAN                -> laporan + sorting              O(n²)
  KELUAR                        -> keluar CLI
"""

import sys
import os
import random
from datetime import datetime

# ── Path setup ────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.join(BASE_DIR, "..")
sys.path.insert(0, SRC_DIR)

# ── Try import modul project ──────────────────────────────────────────
try:
    from data_structures.bst   import BSTKatalogProduk
    from data_structures.stack import TransactionStackManager, OrderRecord
    BST_EXT   = True
    STACK_EXT = True
except ImportError:
    BST_EXT   = False
    STACK_EXT = False

try:
    from data_structures.queue_ll  import MultiPriorityQueue
    QUEUE_EXT = True
except ImportError:
    QUEUE_EXT = False

try:
    from data_structures.graph import GraphRekomendasi
    GRAPH_EXT = True
except ImportError:
    GRAPH_EXT = False

try:
    from data_structures.linked_list import LinkedListLaporan
    LL_EXT = True
except ImportError:
    LL_EXT = False


# ======================================================================
# INLINE FALLBACK — struktur data minimal jika modul belum tersedia
# ======================================================================

# ── BST Inline ────────────────────────────────────────────────────────
class _BSTNode:
    def __init__(self, kode, nama, harga, stok):
        self.kode  = kode
        self.nama  = nama
        self.harga = harga
        self.stok  = stok
        self.left  = self.right = None
    def __str__(self):
        return f"[{self.kode}] {self.nama} | Rp{self.harga:,.0f} | Stok: {self.stok}"

class _BST:
    def __init__(self): self.root = None; self.size = 0
    def insert(self, kode, nama, harga, stok):
        n = _BSTNode(kode, nama, harga, stok)
        if not self.root: self.root = n; self.size += 1; return
        c = self.root
        while True:
            if kode == c.kode: return
            if kode < c.kode:
                if not c.left:  c.left  = n; self.size += 1; return
                c = c.left
            else:
                if not c.right: c.right = n; self.size += 1; return
                c = c.right
    def search(self, kode):
        c = self.root
        while c:
            if kode == c.kode: return c
            c = c.left if kode < c.kode else c.right
        return None
    def update_stok(self, kode, delta):
        n = self.search(kode)
        if not n: return False
        if n.stok + delta < 0: return False
        n.stok += delta; return True
    def inorder(self):
        res = []
        def _in(node):
            if not node: return
            _in(node.left); res.append(node); _in(node.right)
        _in(self.root); return res

# ── Queue Inline ──────────────────────────────────────────────────────
class _Queue:
    TIERS = ["PREMIUM", "REGULAR", "ECONOMY"]
    def __init__(self):
        self._q   = {t: [] for t in self.TIERS}
        self._log = []          # semua order masuk (untuk laporan)
    def enqueue(self, cust, prod, tier):
        tier = tier.upper()
        if tier not in self.TIERS: tier = "ECONOMY"
        item = {"cust": cust, "prod": prod, "tier": tier,
                "waktu": datetime.now().strftime("%H:%M:%S"),
                "id": f"ORD-{cust}-{prod}-{datetime.now().strftime('%H%M%S')}"}
        self._q[tier].append(item)
        self._log.append(item)
        return item
    def dequeue(self):
        for t in self.TIERS:
            if self._q[t]: return self._q[t].pop(0)
        return None
    def cancel_last(self):
        for t in self.TIERS:
            if self._q[t]: return self._q[t].pop()
        return None
    def laporan(self): return list(self._log)
    def total(self): return sum(len(v) for v in self._q.values())

# ── Stack Inline ──────────────────────────────────────────────────────
class _StackMgr:
    def __init__(self):
        self._stacks = {}
    def _get(self, cust):
        if cust not in self._stacks:
            self._stacks[cust] = []
        return self._stacks[cust]
    def push(self, cust, order):
        s = self._get(cust)
        if len(s) >= 10: s.pop(0)
        s.append(order)
    def pop(self, cust):
        s = self._get(cust)
        return s.pop() if s else None
    def riwayat(self, cust): return list(reversed(self._get(cust)))

# ── Graph BFS Inline ─────────────────────────────────────────────────
class _Graph:
    def __init__(self):
        self._adj = {}
    def add_edge(self, u, v, w=1):
        self._adj.setdefault(u, {})[v] = w
        self._adj.setdefault(v, {})[u] = w
    def bfs_recommend(self, start, max_hop=2):
        if start not in self._adj: return []
        visited = {start}
        queue   = [(start, 0)]
        result  = []
        while queue:
            node, hop = queue.pop(0)
            if hop > max_hop: continue
            for nbr, w in self._adj.get(node, {}).items():
                if nbr not in visited:
                    visited.add(nbr)
                    result.append((nbr, w, hop + 1))
                    queue.append((nbr, hop + 1))
        result.sort(key=lambda x: (-x[1], x[2]))
        return result

# ── Sorting (Linked List node) ────────────────────────────────────────
class _LLNode:
    def __init__(self, data): self.data = data; self.next = None

class _LL:
    def __init__(self): self.head = None; self._size = 0
    def append(self, data):
        n = _LLNode(data)
        if not self.head: self.head = n; self._size += 1; return
        c = self.head
        while c.next: c = c.next
        c.next = n; self._size += 1
    def to_list(self):
        r, c = [], self.head
        while c: r.append(c.data); c = c.next
        return r
    def from_list(self, lst):
        self.head = None; self._size = 0
        for item in lst: self.append(item)
    def bubble_sort_harga(self):
        if not self.head: return
        swapped = True
        while swapped:
            swapped = False; c = self.head
            while c and c.next:
                if c.data["total"] < c.next.data["total"]:
                    c.data, c.next.data = c.next.data, c.data
                    swapped = True
                c = c.next
    def insertion_sort_waktu(self):
        items = self.to_list()
        for i in range(1, len(items)):
            key = items[i]; j = i - 1
            while j >= 0 and items[j]["waktu"] > key["waktu"]:
                items[j + 1] = items[j]; j -= 1
            items[j + 1] = key
        self.from_list(items)


# ======================================================================
# WARNA TERMINAL
# ======================================================================
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    ORANGE = "\033[38;5;208m"

def ok(msg):   print(f"  {C.GREEN}✓{C.RESET} {msg}")
def err(msg):  print(f"  {C.RED}✗{C.RESET} {msg}")
def info(msg): print(f"  {C.CYAN}→{C.RESET} {msg}")
def bigo(op, complexity):
    print(f"  {C.YELLOW}Big-O {op}: {C.BOLD}{complexity}{C.RESET}")


# ======================================================================
# SISTEM UTAMA
# ======================================================================

class ECommerceSystem:
    """Sistem CLI E-Commerce terintegrasi."""

    NAMA_PRODUK = [
        "Laptop Gaming", "Mouse Wireless", "Keyboard Mekanikal",
        "Monitor 27\"", "Headset Bluetooth", "Webcam HD",
        "SSD 1TB", "RAM 16GB", "GPU RTX", "Charger USB-C",
        "Microphone USB", "Speaker Portable", "Tablet Android",
        "Smartwatch", "Router WiFi 6", "Power Bank 20000mAh",
        "Kamera Mirrorless", "Drone Mini", "VR Headset", "Game Controller",
    ]

    def __init__(self):
        # Inisialisasi struktur data
        self.katalog = BSTKatalogProduk() if BST_EXT   else _BST()
        self.antrian = MultiPriorityQueue() if QUEUE_EXT else _Queue()
        self.stack   = TransactionStackManager() if STACK_EXT else _StackMgr()
        self.graph   = GraphRekomendasi() if GRAPH_EXT else _Graph()
        self.ll      = LinkedListLaporan() if LL_EXT else _LL()

        self._order_counter = 0
        self._seed_data()

    def _seed_data(self):
        """Seed 100 produk (P001–P100) dan graph rekomendasi."""
        random.seed(99)

        # Seed produk ke BST
        for i in range(1, 101):
            kode  = f"P{i:03d}"
            nama  = self.NAMA_PRODUK[i % len(self.NAMA_PRODUK)]
            harga = random.randint(50_000, 15_000_000)
            stok  = random.randint(5, 100)
            self.katalog.insert(kode, nama, harga, stok)

        # Seed graph co-purchase (edge acak antar produk)
        produk_list = [f"P{i:03d}" for i in range(1, 101)]
        for _ in range(200):
            u = random.choice(produk_list)
            v = random.choice(produk_list)
            if u != v:
                w = random.randint(1, 10)
                self.graph.add_edge(u, v, w)

    def _new_order_id(self, cust: str) -> str:
        self._order_counter += 1
        ts = datetime.now().strftime("%H%M%S")
        return f"ORD-{cust}-{ts}-{self._order_counter:04d}"


# ======================================================================
# HANDLER SETIAP PERINTAH
# ======================================================================

    # ── ORDER <cust> <prod> <tier> ────────────────────────────────────
    def cmd_order(self, args: list):
        if len(args) < 3:
            err("Format: ORDER <cust> <prod> <tier>")
            err("Contoh: ORDER C001 P010 PREMIUM")
            return

        cust, prod, tier = args[0].upper(), args[1].upper(), args[2].upper()

        if tier not in ["PREMIUM", "REGULAR", "ECONOMY"]:
            err(f"Tier tidak valid: {tier}. Pilih PREMIUM / REGULAR / ECONOMY")
            return

        # Cek produk ada di katalog
        node = self.katalog.search(prod)
        if not node:
            err(f"Produk {prod} tidak ditemukan di katalog.")
            return
        if node.stok <= 0:
            err(f"Stok {prod} habis!")
            return

        # Masukkan ke antrian
        item = self.antrian.enqueue(cust, prod, tier)

        # Simpan ke stack riwayat
        oid = self._new_order_id(cust)
        if STACK_EXT:
            rec = OrderRecord(oid, prod, 1, tier, node.harga)
            self.stack._get_or_create(cust).push(rec)
        else:
            self.stack.push(cust, {
                "id": oid, "prod": prod, "tier": tier,
                "harga": node.harga, "total": node.harga,
                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "AKTIF"
            })

        # Simpan ke linked list laporan
        self.ll.append({
            "id": oid, "cust": cust, "prod": prod, "tier": tier,
            "total": node.harga,
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

        ok(f"Order masuk antrian [{tier}] — {cust} | {prod} | {node.nama}")
        info(f"Harga satuan: Rp{node.harga:,.0f}")
        bigo("enqueue", "O(1)")

    # ── SERVE ─────────────────────────────────────────────────────────
    def cmd_serve(self, args: list):
        item = self.antrian.dequeue()
        if not item:
            err("Antrian kosong. Tidak ada order yang bisa dilayani.")
            return

        # Kurangi stok
        if isinstance(item, dict):
            cust, prod, tier = item["cust"], item["prod"], item["tier"]
        else:
            cust = getattr(item, "cust", str(item))
            prod = getattr(item, "prod", "?")
            tier = getattr(item, "tier", "?")

        self.katalog.update_stok(prod, -1)

        print(f"\n  {C.ORANGE}{'▶ MELAYANI ORDER ':─<45}{C.RESET}")
        ok(f"Pelanggan : {cust}")
        ok(f"Produk    : {prod}")
        ok(f"Tier      : {tier}")
        node = self.katalog.search(prod)
        if node:
            ok(f"Stok sisa : {node.stok}")
        bigo("serve (dequeue)", "O(1)")

    # ── CANCEL_LAST ───────────────────────────────────────────────────
    def cmd_cancel_last(self, args: list):
        item = self.antrian.cancel_last()
        if not item:
            err("Antrian kosong. Tidak ada yang bisa dibatalkan.")
            return
        if isinstance(item, dict):
            cust, prod, tier = item.get("cust","?"), item.get("prod","?"), item.get("tier","?")
        else:
            cust = getattr(item, "cust", "?")
            prod = getattr(item, "prod", "?")
            tier = getattr(item, "tier", "?")

        ok(f"Order terakhir dibatalkan dari antrian: {cust} | {prod} | {tier}")
        bigo("CANCEL_LAST (Stack pop)", "O(1)")

    # ── CARI_PRODUK <kode> ────────────────────────────────────────────
    def cmd_cari_produk(self, args: list):
        if not args:
            err("Format: CARI_PRODUK <kode>   Contoh: CARI_PRODUK P010")
            return
        kode = args[0].upper()
        node = self.katalog.search(kode)
        if not node:
            err(f"Produk {kode} tidak ditemukan.")
        else:
            print(f"\n  {C.BLUE}{'─'*45}{C.RESET}")
            ok(f"Kode  : {node.kode}")
            ok(f"Nama  : {node.nama}")
            ok(f"Harga : Rp{node.harga:,.0f}")
            ok(f"Stok  : {node.stok}")
            print(f"  {C.BLUE}{'─'*45}{C.RESET}")
        bigo("CARI_PRODUK (BST search)", "O(log n)")

    # ── UPDATE_STOK <kode> <qty> ──────────────────────────────────────
    def cmd_update_stok(self, args: list):
        if len(args) < 2:
            err("Format: UPDATE_STOK <kode> <qty>   Contoh: UPDATE_STOK P010 +20")
            return
        kode = args[0].upper()
        try:
            delta = int(args[1])
        except ValueError:
            err("qty harus berupa angka. Contoh: +20 atau -5")
            return

        sukses = self.katalog.update_stok(kode, delta)
        if sukses:
            node = self.katalog.search(kode)
            ok(f"Stok {kode} diperbarui → {node.stok} unit")
        else:
            err(f"Gagal update stok {kode}.")
        bigo("UPDATE_STOK (BST search+update)", "O(log n)")

    # ── REKOMENDASI <kode_produk> ─────────────────────────────────────
    def cmd_rekomendasi(self, args: list):
        if not args:
            err("Format: REKOMENDASI <kode_produk>   Contoh: REKOMENDASI P010")
            return
        kode    = args[0].upper()
        results = self.graph.bfs_recommend(kode, max_hop=2)

        if not results:
            err(f"Tidak ada rekomendasi untuk {kode}. (Belum ada data co-purchase)")
            bigo("REKOMENDASI (BFS)", "O(V+E)")
            return

        print(f"\n  {C.CYAN}Rekomendasi untuk {kode} (BFS, hop ≤ 2):{C.RESET}")
        print(f"  {'─'*50}")
        for i, (prod, freq, hop) in enumerate(results[:5], 1):
            node = self.katalog.search(prod)
            nama = node.nama if node else "?"
            ok(f"{i}. {prod} | {nama} | freq={freq} | hop={hop}")
        bigo("REKOMENDASI (BFS)", "O(V+E)")

    # ── RIWAYAT <cust> ────────────────────────────────────────────────
    def cmd_riwayat(self, args: list):
        if not args:
            err("Format: RIWAYAT <cust>   Contoh: RIWAYAT C001")
            return
        cust = args[0].upper()

        if STACK_EXT:
            self.stack.tampilkan_riwayat(cust)
        else:
            orders = self.stack.riwayat(cust)
            print(f"\n  {'='*55}")
            print(f"  {'RIWAYAT TRANSAKSI — ' + cust:^55}")
            print(f"  {'='*55}")
            if not orders:
                print("  (Belum ada transaksi)")
            else:
                for i, o in enumerate(orders, 1):
                    print(f"  {i:>2}. {o.get('waktu','?')} | {o.get('id','?')} | "
                          f"{o.get('prod','?')} | {o.get('tier','?')} | "
                          f"Rp{o.get('total',0):,.0f}")
            print(f"  {'='*55}")
        bigo("RIWAYAT (Stack traversal)", "O(n)")

    # ── LAPORAN_HARIAN ────────────────────────────────────────────────
    def cmd_laporan_harian(self, args: list):
        import time

        items = self.ll.to_list()
        if not items:
            err("Belum ada order yang diproses hari ini.")
            return

        # (a) Bubble Sort by total_harga descending
        ll_bubble = _LL()
        for item in items: ll_bubble.append(item)
        t0 = time.perf_counter()
        ll_bubble.bubble_sort_harga()
        t_bubble = (time.perf_counter() - t0) * 1000

        # (b) Insertion Sort by waktu_pesan ascending
        ll_insert = _LL()
        for item in items: ll_insert.append(item)
        t0 = time.perf_counter()
        ll_insert.insertion_sort_waktu()
        t_insert = (time.perf_counter() - t0) * 1000

        n = len(items)

        print(f"\n  {C.ORANGE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{'LAPORAN HARIAN E-COMMERCE':^55}{C.RESET}")
        print(f"  {C.ORANGE}{'═'*55}{C.RESET}")
        print(f"  Total order hari ini: {n}")
        print()

        # Tampilkan top 5 by harga
        sorted_harga = ll_bubble.to_list()
        print(f"  {C.CYAN}Top 5 Order by Total Harga (Descending):{C.RESET}")
        print(f"  {'─'*55}")
        for i, o in enumerate(sorted_harga[:5], 1):
            print(f"  {i}. {o.get('id','?')[:20]:<22} "
                  f"{o.get('cust','?'):<6} "
                  f"Rp{o.get('total',0):>12,.0f}")

        print()

        # Tampilkan top 5 by waktu
        sorted_waktu = ll_insert.to_list()
        print(f"  {C.CYAN}Top 5 Order by Waktu Pesan (Ascending):{C.RESET}")
        print(f"  {'─'*55}")
        for i, o in enumerate(sorted_waktu[:5], 1):
            print(f"  {i}. {o.get('waktu','?')} | "
                  f"{o.get('cust','?')} | "
                  f"{o.get('prod','?')} | "
                  f"{o.get('tier','?')}")

        print()
        print(f"  {C.YELLOW}Runtime Sorting (N={n}):{C.RESET}")
        print(f"  Bubble Sort    (by harga)  : {t_bubble:.4f} ms")
        print(f"  Insertion Sort (by waktu)  : {t_insert:.4f} ms")
        faster = "Insertion Sort" if t_insert < t_bubble else "Bubble Sort"
        print(f"  → {C.GREEN}{faster} lebih cepat{C.RESET}")
        print(f"  {C.ORANGE}{'═'*55}{C.RESET}")
        bigo("LAPORAN_HARIAN (sorting)", "O(n²)")


# ======================================================================
# CLI LOOP
# ======================================================================

BANNER = f"""
{C.ORANGE}╔══════════════════════════════════════════════════════╗
║     E-COMMERCE ORDER MANAGEMENT & RECOMMENDATION    ║
║              TOPIK 3 — CLI TERINTEGRASI             ║
╚══════════════════════════════════════════════════════╝{C.RESET}
{C.CYAN}Perintah:{C.RESET}
  ORDER <cust> <prod> <tier>    → tambah order         O(1)
  SERVE                          → layani order          O(1)
  CANCEL_LAST                    → batalkan order terakhir O(1)
  CARI_PRODUK <kode>             → cari produk BST       O(log n)
  UPDATE_STOK <kode> <qty>       → update stok           O(log n)
  REKOMENDASI <kode>             → rekomendasi BFS       O(V+E)
  RIWAYAT <cust>                 → riwayat transaksi     O(n)
  LAPORAN_HARIAN                 → laporan + sorting     O(n²)
  KELUAR                         → keluar
{C.YELLOW}Contoh:{C.RESET}
  ORDER C001 P010 PREMIUM
  CARI_PRODUK P050
  REKOMENDASI P010
"""

COMMANDS = {
    "ORDER":         "cmd_order",
    "SERVE":         "cmd_serve",
    "CANCEL_LAST":   "cmd_cancel_last",
    "CARI_PRODUK":   "cmd_cari_produk",
    "UPDATE_STOK":   "cmd_update_stok",
    "REKOMENDASI":   "cmd_rekomendasi",
    "RIWAYAT":       "cmd_riwayat",
    "LAPORAN_HARIAN":"cmd_laporan_harian",
}


def run_cli():
    print(BANNER)
    system = ECommerceSystem()
    ok("Sistem diinisialisasi. 100 produk dimuat ke BST. Graph rekomendasi siap.")
    print()

    while True:
        try:
            raw = input(f"{C.BOLD}{C.WHITE}ecommerce>{C.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{C.YELLOW}Sampai jumpa!{C.RESET}")
            break

        if not raw:
            continue

        parts = raw.upper().split()
        cmd   = parts[0]
        args  = parts[1:]   # sisa argumen (sudah uppercase)

        if cmd == "KELUAR":
            print(f"\n{C.YELLOW}Terima kasih telah menggunakan sistem. Sampai jumpa!{C.RESET}\n")
            break

        if cmd in COMMANDS:
            print()
            try:
                getattr(system, COMMANDS[cmd])(args)
            except Exception as exc:
                err(f"Error: {exc}")
            print()
        else:
            err(f"Perintah tidak dikenal: {cmd}")
            info("Ketik KELUAR untuk keluar, atau lihat daftar perintah di atas.")


if __name__ == "__main__":
    run_cli()
