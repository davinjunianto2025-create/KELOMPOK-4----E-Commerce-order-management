"""
ELT60213 – Algoritma dan Struktur Data
Topik 3: E-Commerce Order Management & Recommendation Engine
Kelompok 4 | TA 2025/2026 | seed = 99
"""

import time, random
import numpy as np
from typing import Optional, List, Dict, Tuple

np.random.seed(99)
random.seed(99)

# ──────────────────────────────────────────
# DATACLASS
# ──────────────────────────────────────────
class Produk:
    def __init__(self, kode, nama, harga, stok):
        self.kode = kode; self.nama = nama
        self.harga = harga; self.stok = stok

class Order:
    def __init__(self, order_id, pelanggan, produk_kode, tier, qty, total_harga, waktu_pesan):
        self.order_id = order_id; self.pelanggan = pelanggan
        self.produk_kode = produk_kode; self.tier = tier
        self.qty = qty; self.total_harga = total_harga
        self.waktu_pesan = waktu_pesan

# ──────────────────────────────────────────
# NODE LINKED LIST
# ──────────────────────────────────────────
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None

# ──────────────────────────────────────────
# QUEUE berbasis Linked List
# ──────────────────────────────────────────
class Queue:
    def __init__(self):
        self.head = self.tail = None
        self._size = 0

    def enqueue(self, data):
        node = LLNode(data)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def dequeue(self):
        if self.is_empty(): return None
        data = self.head.data
        self.head = self.head.next
        if not self.head: self.tail = None
        self._size -= 1
        return data

    def is_empty(self): return self._size == 0
    def __len__(self): return self._size

    def to_list(self):
        r, c = [], self.head
        while c: r.append(c.data); c = c.next
        return r

# ──────────────────────────────────────────
# STACK berbasis Linked List
# ──────────────────────────────────────────
class Stack:
    def __init__(self, kapasitas=10):
        self.top = None
        self._size = 0
        self.kapasitas = kapasitas

    def push(self, data):
        if self._size >= self.kapasitas:
            items = self.to_list()[:-1]  # buang terlama
            self.top = None; self._size = 0
            for item in reversed(items):
                node = LLNode(item); node.next = self.top
                self.top = node; self._size += 1
        node = LLNode(data); node.next = self.top
        self.top = node; self._size += 1

    def pop(self):
        if self.is_empty(): return None
        data = self.top.data; self.top = self.top.next
        self._size -= 1; return data

    def is_empty(self): return self._size == 0
    def __len__(self): return self._size

    def to_list(self):
        r, c = [], self.top
        while c: r.append(c.data); c = c.next
        return r

# ──────────────────────────────────────────
# BST KATALOG PRODUK
# ──────────────────────────────────────────
class BSTNode:
    def __init__(self, produk):
        self.produk = produk
        self.left = self.right = None

class BSTKatalog:
    def __init__(self): self.root = None

    def insert(self, produk):
        self.root = self._ins(self.root, produk)

    def _ins(self, node, produk):
        if node is None: return BSTNode(produk)
        if produk.kode < node.produk.kode:
            node.left = self._ins(node.left, produk)
        elif produk.kode > node.produk.kode:
            node.right = self._ins(node.right, produk)
        return node

    def search(self, kode):
        node = self._srch(self.root, kode)
        return node.produk if node else None

    def _srch(self, node, kode):
        if node is None or node.produk.kode == kode: return node
        return self._srch(node.left, kode) if kode < node.produk.kode \
               else self._srch(node.right, kode)

    def update_stok(self, kode, delta):
        node = self._srch(self.root, kode)
        if node: node.produk.stok += delta; return True
        return False

    def inorder(self):
        r = []; self._ino(self.root, r); return r

    def _ino(self, node, r):
        if node: self._ino(node.left, r); r.append(node.produk); self._ino(node.right, r)

# ──────────────────────────────────────────
# GRAPH REKOMENDASI
# ──────────────────────────────────────────
class GraphRekomendasi:
    def __init__(self): self.adj: Dict[str, List[Tuple[str,int]]] = {}

    def add_copurchase(self, a, b):
        for x, y in [(a,b),(b,a)]:
            if x not in self.adj: self.adj[x] = []
            for i,(nb,fr) in enumerate(self.adj[x]):
                if nb == y: self.adj[x][i] = (y, fr+1); break
            else: self.adj[x].append((y, 1))

    def rekomendasikan(self, kode, max_hop=2):
        if kode not in self.adj: return []
        visited = {kode}; freq_map = {}
        q = Queue(); q.enqueue((kode, 0))
        while not q.is_empty():
            curr, hop = q.dequeue()
            if hop >= max_hop: continue
            for nb, fr in self.adj.get(curr, []):
                if nb not in visited:
                    visited.add(nb)
                    freq_map[nb] = freq_map.get(nb, 0) + fr
                    q.enqueue((nb, hop+1))
        return sorted(freq_map.items(), key=lambda x: -x[1])

# ──────────────────────────────────────────
# LINKED LIST ORDER (untuk Sorting)
# ──────────────────────────────────────────
class OrderLL:
    def __init__(self): self.head = None; self._size = 0

    def append(self, order):
        node = LLNode(order)
        if not self.head: self.head = node; self._size += 1; return
        c = self.head
        while c.next: c = c.next
        c.next = node; self._size += 1

    def to_list(self):
        r, c = [], self.head
        while c: r.append(c.data); c = c.next
        return r

    def __len__(self): return self._size

    def bubble_sort_harga_desc(self):
        t = time.perf_counter()
        swapped = True
        while swapped:
            swapped = False; c = self.head
            while c and c.next:
                if c.data.total_harga < c.next.data.total_harga:
                    c.data, c.next.data = c.next.data, c.data; swapped = True
                c = c.next
        return (time.perf_counter() - t) * 1000

    def insertion_sort_waktu_asc(self):
        t = time.perf_counter()
        sorted_head = None; curr = self.head
        while curr:
            nxt = curr.next
            if not sorted_head or curr.data.waktu_pesan < sorted_head.data.waktu_pesan:
                curr.next = sorted_head; sorted_head = curr
            else:
                tmp = sorted_head
                while tmp.next and tmp.next.data.waktu_pesan <= curr.data.waktu_pesan:
                    tmp = tmp.next
                curr.next = tmp.next; tmp.next = curr
            curr = nxt
        self.head = sorted_head
        return (time.perf_counter() - t) * 1000

# ──────────────────────────────────────────
# GENERATE DATA
# ──────────────────────────────────────────
def generate_produk(n=100):
    tmpl = ['Laptop','Mouse','Keyboard','Monitor','Headset',
            'Webcam','USB Hub','Charger','Kabel HDMI','Speaker']
    return [Produk(f'P{i:03d}', f'{random.choice(tmpl)} Model-{i}',
                   round(random.uniform(50_000,5_000_000),-3),
                   random.randint(0,200)) for i in range(1,n+1)]

def generate_orders(produk_list, n=300):
    custs = [f'C{i:03d}' for i in range(1,51)]
    tiers = ['PREMIUM','REGULAR','REGULAR','ECONOMY']
    hasil = []
    for i in range(1,n+1):
        p = random.choice(produk_list)
        t = random.choice(tiers)
        q = random.randint(1,5)
        hasil.append(Order(i, random.choice(custs), p.kode, t,
                           q, p.harga*q, time.time()+i*0.01))
    return hasil

def build_graph(orders, graf):
    dari_cust: Dict[str, List[str]] = {}
    for o in orders:
        dari_cust.setdefault(o.pelanggan,[]).append(o.produk_kode)
    for prods in dari_cust.values():
        uniq = list(dict.fromkeys(prods))
        for i in range(len(uniq)):
            for j in range(i+1, min(i+4, len(uniq))):
                graf.add_copurchase(uniq[i], uniq[j])

# ──────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────
def main():
    # ── Init ──
    queues = {'PREMIUM': Queue(), 'REGULAR': Queue(), 'ECONOMY': Queue()}
    cust_stacks: Dict[str, Stack] = {}
    cancel_stack = Stack(kapasitas=50)
    bst = BSTKatalog()
    graf = GraphRekomendasi()
    order_ll = OrderLL()
    counter = 0

    produk_list = generate_produk(100)
    for p in produk_list: bst.insert(p)

    print("=" * 58)
    print("   E-COMMERCE ORDER MANAGEMENT & RECOMMENDATION ENGINE")
    print("   ELT60213 | Kelompok 4 | TA 2025/2026")
    print("=" * 58)
    print(f"  100 produk dimuat ke BST Katalog.")
    print("  Ketik BANTUAN untuk daftar perintah.\n")

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar. Sampai jumpa!"); break
        if not raw: continue
        parts = raw.upper().split()
        cmd = parts[0]

        # ── ORDER ──
        if cmd == 'ORDER':
            if len(parts) < 4:
                print("  [!] Format: ORDER <cust> <prod> <tier>"); continue
            cust, kode, tier = parts[1], parts[2], parts[3]
            if tier not in queues:
                print("  [!] Tier: PREMIUM | REGULAR | ECONOMY"); continue
            p = bst.search(kode)
            if not p: print(f"  [!] Produk {kode} tidak ditemukan."); continue
            if p.stok <= 0: print(f"  [!] Stok {kode} habis!"); continue
            counter += 1
            total = p.harga * 1
            order = Order(counter, cust, kode, tier, 1, total, time.time())
            queues[tier].enqueue(order)
            cancel_stack.push(order)
            bst.update_stok(kode, -1)
            print(f"  [OK] Order #{counter}: {cust} beli {kode} [{tier}]"
                  f" Rp{total:,.0f}  | enqueue O(1)")

        # ── SERVE ──
        elif cmd == 'SERVE':
            served = None
            for tier in ['PREMIUM','REGULAR','ECONOMY']:
                if not queues[tier].is_empty():
                    served = queues[tier].dequeue(); served_tier = tier; break
            if not served:
                print("  [!] Semua antrian kosong.")
            else:
                cust = served.pelanggan
                if cust not in cust_stacks: cust_stacks[cust] = Stack(10)
                cust_stacks[cust].push(served)
                order_ll.append(served)
                print(f"  [OK] Melayani Order #{served.order_id} | {served.pelanggan}"
                      f" - {served.produk_kode} [{served_tier}] Rp{served.total_harga:,.0f}")
                print(f"       Kompleksitas SERVE: O(1)")

        # ── CANCEL_LAST ──
        elif cmd == 'CANCEL_LAST':
            last = cancel_stack.pop()
            if not last: print("  [!] Tidak ada order untuk dibatalkan."); continue
            items = queues[last.tier].to_list()
            new = [o for o in items if o.order_id != last.order_id]
            if len(new) < len(items):
                queues[last.tier] = Queue()
                for o in new: queues[last.tier].enqueue(o)
                bst.update_stok(last.produk_kode, last.qty)
                print(f"  [OK] Order #{last.order_id} ({last.produk_kode}) dibatalkan."
                      f" Stok dikembalikan.  | Stack pop O(1)")
            else:
                print(f"  [!] Order #{last.order_id} sudah dilayani, tidak bisa dibatalkan.")

        # ── LAPORAN_ANTRIAN ──
        elif cmd == 'LAPORAN_ANTRIAN':
            print("\n  ── LAPORAN ANTRIAN ──────────────────────────")
            total = 0
            for tier in ['PREMIUM','REGULAR','ECONOMY']:
                items = queues[tier].to_list()
                n = len(items)
                total += n
                head_info = f"HEAD: Order#{items[0].order_id} ({items[0].pelanggan})" if items else "Kosong"
                print(f"  {tier:<10}: {n:>3} order  |  {head_info}")
            print(f"  {'─'*42}")
            print(f"  Total: {total} order\n")

        # ── CARI_PRODUK ──
        elif cmd == 'CARI_PRODUK':
            if len(parts) < 2: print("  [!] Format: CARI_PRODUK <kode>"); continue
            p = bst.search(parts[1])
            if not p: print(f"  [!] Produk {parts[1]} tidak ditemukan.")
            else:
                print(f"\n  ── Detail Produk ──────────────────────────")
                print(f"  Kode  : {p.kode}")
                print(f"  Nama  : {p.nama}")
                print(f"  Harga : Rp{p.harga:,.0f}")
                print(f"  Stok  : {p.stok} unit")
                print(f"  Kompleksitas: O(log n) = O(log 100) ≈ 7 langkah\n")

        # ── UPDATE_STOK ──
        elif cmd == 'UPDATE_STOK':
            if len(parts) < 3: print("  [!] Format: UPDATE_STOK <kode> <qty>"); continue
            try: qty = int(parts[2])
            except: print("  [!] qty harus angka."); continue
            if bst.update_stok(parts[1], qty):
                p = bst.search(parts[1])
                print(f"  [OK] Stok {parts[1]} diperbarui. Stok baru: {p.stok} unit  | O(log n)")
            else: print(f"  [!] Produk {parts[1]} tidak ditemukan.")

        # ── KATALOG ──
        elif cmd == 'KATALOG':
            n_show = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
            items = bst.inorder()[:n_show]
            print(f"\n  ── BST Katalog Inorder ({n_show} pertama) ─────────────")
            print(f"  {'Kode':<8} {'Nama':<30} {'Harga':>12} {'Stok':>6}")
            print(f"  {'─'*7} {'─'*29} {'─'*12} {'─'*6}")
            for p in items:
                print(f"  {p.kode:<8} {p.nama:<30} Rp{p.harga:>10,.0f} {p.stok:>5}")
            print(f"  Kompleksitas: O(n)\n")

        # ── REKOMENDASI ──
        elif cmd == 'REKOMENDASI':
            if len(parts) < 2: print("  [!] Format: REKOMENDASI <kode>"); continue
            rek = graf.rekomendasikan(parts[1])
            if not rek:
                print(f"  [!] Belum ada co-purchase untuk {parts[1]}. Jalankan DEMO_SIMULASI dulu.")
            else:
                print(f"\n  ── Rekomendasi untuk {parts[1]} (BFS <= 2 hop) ───────")
                print(f"  {'Produk':<10} {'Frekuensi':>10}  Nama")
                print(f"  {'─'*9} {'─'*10}  {'─'*25}")
                for kd, fr in rek[:8]:
                    p = bst.search(kd)
                    nama = p.nama if p else "?"
                    print(f"  {kd:<10} {fr:>8}x  {nama}")
                print(f"  Kompleksitas BFS: O(V + E)\n")

        # ── RIWAYAT ──
        elif cmd == 'RIWAYAT':
            if len(parts) < 2: print("  [!] Format: RIWAYAT <cust>"); continue
            cust = parts[1]
            if cust not in cust_stacks or cust_stacks[cust].is_empty():
                print(f"  [!] Belum ada riwayat untuk {cust}.")
            else:
                items = cust_stacks[cust].to_list()
                print(f"\n  ── Riwayat {cust} (Stack, terbaru di atas) ───────")
                for i, o in enumerate(items, 1):
                    print(f"  [{i:2d}] Order#{o.order_id:<5} {o.produk_kode}  {o.tier:<10}"
                          f"  Rp{o.total_harga:>10,.0f}")
                print(f"  Kompleksitas: O(n)\n")

        # ── UNDO_ORDER ──
        elif cmd == 'UNDO_ORDER':
            if len(parts) < 2: print("  [!] Format: UNDO_ORDER <cust>"); continue
            cust = parts[1]
            if cust not in cust_stacks or cust_stacks[cust].is_empty():
                print(f"  [!] Tidak ada riwayat untuk {cust}.")
            else:
                last = cust_stacks[cust].pop()
                bst.update_stok(last.produk_kode, last.qty)
                print(f"  [OK] UNDO: Order #{last.order_id} ({last.produk_kode}) dihapus dari riwayat.")
                print(f"       Stok {last.produk_kode} dikembalikan +{last.qty}  | pop O(1)")

        # ── LAPORAN_HARIAN ──
        elif cmd == 'LAPORAN_HARIAN':
            if len(order_ll) == 0:
                print("  [!] Belum ada order selesai. Gunakan SERVE atau DEMO_SIMULASI."); continue
            all_orders = order_ll.to_list()
            n = len(all_orders)
            print(f"\n  ══════════════════════════════════════════════")
            print(f"  LAPORAN HARIAN — {n} order selesai")
            print(f"  ══════════════════════════════════════════════")

            ll_b = OrderLL()
            ll_i = OrderLL()
            for o in all_orders: ll_b.append(o); ll_i.append(o)
            tb = ll_b.bubble_sort_harga_desc()
            ti = ll_i.insertion_sort_waktu_asc()

            print(f"\n  Bubble Sort   (harga DESC) : {tb:.3f} ms")
            print(f"  Insertion Sort (waktu ASC) : {ti:.3f} ms")
            print(f"  Rasio Bubble/Insertion     : {tb/ti:.1f}x lebih lambat\n")

            # Benchmark 3 ukuran
            sim = generate_orders(produk_list, 300)
            print(f"  {'N':>6}  {'Bubble Sort':>13}  {'Insertion Sort':>15}")
            print(f"  {'─'*6}  {'─'*13}  {'─'*15}")
            for size in [50, 100, 300]:
                sub = sim[:size]
                lb = OrderLL(); li = OrderLL()
                for o in sub: lb.append(o); li.append(o)
                print(f"  {size:>6}  {lb.bubble_sort_harga_desc():>11.3f} ms"
                      f"  {li.insertion_sort_waktu_asc():>13.3f} ms")
            print(f"\n  Kompleksitas: O(n²)  — Insertion Sort lebih baik untuk data hampir terurut")

            print(f"\n  Top-5 Order (harga tertinggi setelah Bubble Sort):")
            for i, o in enumerate(ll_b.to_list()[:5], 1):
                print(f"  {i}. Order#{o.order_id:<5} {o.pelanggan} {o.produk_kode}"
                      f" [{o.tier}]  Rp{o.total_harga:,.0f}")
            print(f"  ══════════════════════════════════════════════\n")

        # ── DEMO_SIMULASI ──
        elif cmd == 'DEMO_SIMULASI':
            print("  Menjalankan 300 order simulasi (seed=99)...")
            sim = generate_orders(produk_list, 300)
            for o in sim: queues[o.tier].enqueue(o); cancel_stack.push(o)
            count = 0
            for tier in ['PREMIUM','REGULAR','ECONOMY']:
                while not queues[tier].is_empty():
                    sv = queues[tier].dequeue()
                    cust = sv.pelanggan
                    if cust not in cust_stacks: cust_stacks[cust] = Stack(10)
                    cust_stacks[cust].push(sv)
                    order_ll.append(sv)
                    count += 1
            build_graph(sim, graf)
            counter += 300
            print(f"  [OK] {count} order dilayani. Graf co-purchase dibangun.")
            print(f"  Coba: RIWAYAT C001 | REKOMENDASI P015 | LAPORAN_HARIAN\n")

        # ── BANTUAN ──
        elif cmd == 'BANTUAN':
            print("""
  ── PERINTAH TERSEDIA ──────────────────────────────────
  ORDER <cust> <prod> <tier>   Buat order baru
  SERVE                        Layani order prioritas
  CANCEL_LAST                  Batalkan order terakhir
  LAPORAN_ANTRIAN              Status semua antrian
  CARI_PRODUK <kode>           Cari produk (BST)
  UPDATE_STOK <kode> <qty>     Update stok produk
  KATALOG [n]                  Tampilkan katalog (inorder)
  REKOMENDASI <kode>           Rekomendasi co-purchase
  RIWAYAT <cust>               Riwayat transaksi (Stack)
  UNDO_ORDER <cust>            Batalkan transaksi terakhir
  LAPORAN_HARIAN               Sorting & laporan harian
  DEMO_SIMULASI                Jalankan 300 order simulasi
  KELUAR                       Keluar dari sistem
  ──────────────────────────────────────────────────────""")

        elif cmd == 'KELUAR':
            print("\n  Terima kasih! Sistem ditutup.\n"); break
        else:
            print(f"  [!] Perintah tidak dikenal. Ketik BANTUAN.")

if __name__ == '__main__':
    main()
