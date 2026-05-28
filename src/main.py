"""
E-Commerce Order Management & Recommendation Engine
Topik 3 | Kelompok 4 | ELT60213 Algoritma dan Struktur Data

Menggabungkan:
  - data_structures/bst.py          -> BSTKatalogProduk
  - data_structures/stack.py        -> TransactionStackManager
  - data_structures/queue_ll.py     -> QueueLinkedList
  - data_structures/linked_list.py  -> LinkedListLaporan
  - data_structures/graph.py        -> RecommendationGraph
  - modules/modul_1.py              -> MultiPriorityOrderQueue
  - modules/modul_3.py              -> GraphRekomendasi (BFS co-purchase)
  - modules/modul_5.py              -> bubble_sort, insertion_sort
"""

import sys
import os
import random
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Data Structures
from data_structures.bst          import BSTKatalogProduk
from data_structures.stack        import TransactionStackManager
from data_structures.linked_list  import LinkedListLaporan
from data_structures.graph        import RecommendationGraph

# Modules
from modules.modul_1 import MultiPriorityOrderQueue, generate_random_orders
from modules.modul_3 import GraphRekomendasi, simulasi_copurchase
from modules.modul_5 import (
    LinkedList as LLSort,
    bubble_sort_harga_desc,
    insertion_sort_waktu_asc,
)

random.seed(99)


# ══════════════════════════════════════════════════════════
# SEED DATA PRODUK
# ══════════════════════════════════════════════════════════

PRODUK_DATA = [
    ("P001", "Keyboard Mekanikal",   850_000,  30),
    ("P010", "Mouse Wireless",       250_000,  50),
    ("P020", "Mousepad XL",           75_000, 100),
    ("P025", "Webcam HD",            450_000,  15),
    ("P030", "USB Hub 7-Port",       180_000,  40),
    ("P040", "Kabel HDMI 2m",         55_000,  80),
    ("P050", "Laptop Gaming",     15_000_000,  10),
    ("P060", "Monitor 27 inch",    4_500_000,   8),
    ("P075", "Headset Bluetooth",    600_000,  20),
    ("P080", "Speaker Portable",     350_000,  25),
    ("P090", "Charger GaN 65W",      275_000,  35),
    ("P100", "SSD External 1TB",   1_200_000,  12),
]


# ══════════════════════════════════════════════════════════
# INISIALISASI SISTEM
# ══════════════════════════════════════════════════════════

def init_sistem():
    bst = BSTKatalogProduk()
    for kode, nama, harga, stok in PRODUK_DATA:
        bst.insert(kode, nama, harga, stok)

    mpq       = MultiPriorityOrderQueue()
    stack_mgr = TransactionStackManager()
    graf      = GraphRekomendasi()
    laporan   = LinkedListLaporan()
    rec_graph = RecommendationGraph()

    kode_list = [k for k, *_ in PRODUK_DATA]
    for k in kode_list:
        graf.inisialisasi_produk(k)

    return bst, mpq, stack_mgr, graf, laporan, rec_graph


# ══════════════════════════════════════════════════════════
# HELPER
# ══════════════════════════════════════════════════════════

def cetak_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║  E-Commerce Order Management & Recommendation Engine    ║
║  Kelompok 4 | ELT60213 Algoritma & Struktur Data        ║
╚══════════════════════════════════════════════════════════╝
Ketik BANTUAN untuk daftar perintah.
""")


def cetak_bantuan():
    print("""
  ── PERINTAH TERSEDIA ────────────────────────────────────
  ORDER <cust> <prod> <tier>    Tambah order ke antrian
  SERVE                         Layani order prioritas tertinggi
  CANCEL_LAST                   Batalkan order terakhir (undo)
  LAPORAN_ANTRIAN               Status semua antrian
  ──
  CARI_PRODUK <kode>            Cari produk di BST katalog
  KATALOG [n]                   Tampilkan katalog (inorder BST)
  UPDATE_STOK <kode> <delta>    Update stok (+/-)
  ──
  RIWAYAT <cust>                Riwayat transaksi pelanggan (Stack)
  UNDO_ORDER <cust>             Batalkan transaksi terakhir pelanggan
  ──
  REKOMENDASI <kode>            Rekomendasi produk (BFS co-purchase)
  LAPORAN_HARIAN                Sorting laporan harian
  DEMO                          Isi 10 order acak & serve 3
  DEMO_SIMULASI                 Simulasi 300 order (seed=99)
  BANTUAN                       Tampilkan bantuan ini
  KELUAR                        Keluar dari sistem
  ─────────────────────────────────────────────────────────""")


# ══════════════════════════════════════════════════════════
# MAIN CLI
# ══════════════════════════════════════════════════════════

def main():
    cetak_banner()
    bst, mpq, stack_mgr, graf, laporan, rec_graph = init_sistem()
    waktu_counter = [0]

    print(f"  {len(PRODUK_DATA)} produk dimuat ke BST Katalog.\n")

    while True:
        try:
            raw = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Keluar. Sampai jumpa!")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd   = parts[0].upper()
        args  = parts[1:]

        # ORDER
        if cmd == "ORDER":
            if len(args) < 3:
                print("  [!] Format: ORDER <cust> <prod> <tier>"); continue
            cust, kode, tier = args[0].upper(), args[1].upper(), args[2].upper()
            if tier not in ("PREMIUM", "REGULAR", "ECONOMY"):
                print("  [!] Tier harus: PREMIUM | REGULAR | ECONOMY"); continue
            produk = bst.search(kode)
            if not produk:
                print(f"  [!] Produk {kode} tidak ditemukan."); continue
            if produk.stok <= 0:
                print(f"  [!] Stok {kode} habis!"); continue
            print(" ", mpq.order(cust, kode, tier))
            bst.update_stok(kode, -1)

        # SERVE
        elif cmd == "SERVE":
            hasil = mpq.serve()
            print(" ", hasil)
            if "SERVE" in hasil:
                node = mpq.undo_stack.peek()
                if node:
                    p     = bst.search(node.product_id)
                    harga = p.harga if p else 0
                    stack_mgr.catat_order(
                        node.customer_id, node.product_id,
                        1, node.tier, harga
                    )
                    waktu_counter[0] += 1
                    laporan.append(
                        node.customer_id, node.product_id,
                        harga, waktu_counter[0]
                    )
                    riwayat_cust = stack_mgr.get_stack(node.customer_id).riwayat(5)
                    for prev in riwayat_cust[1:]:
                        graf.add_copurchase(node.product_id, prev.kode_produk)
                        rec_graph.add_edge(node.product_id, prev.kode_produk)

        # CANCEL_LAST
        elif cmd == "CANCEL_LAST":
            print(" ", mpq.cancel_last())

        # LAPORAN_ANTRIAN
        elif cmd == "LAPORAN_ANTRIAN":
            print(mpq.laporan_antrian())

        # CARI_PRODUK
        elif cmd == "CARI_PRODUK":
            if not args:
                print("  [!] Format: CARI_PRODUK <kode>"); continue
            p = bst.search(args[0].upper())
            if not p:
                print(f"  [!] Produk {args[0].upper()} tidak ditemukan.")
            else:
                print(f"\n  Kode  : {p.kode}")
                print(f"  Nama  : {p.nama}")
                print(f"  Harga : Rp{p.harga:,.0f}")
                print(f"  Stok  : {p.stok} unit  | O(log n)\n")

        # KATALOG
        elif cmd == "KATALOG":
            n_show = int(args[0]) if args and args[0].isdigit() else len(PRODUK_DATA)
            items  = bst.inorder()[:n_show]
            print(f"\n  {'Kode':<8} {'Nama':<25} {'Harga':>13} {'Stok':>6}")
            print(f"  {'─'*60}")
            for p in items:
                print(f"  {p.kode:<8} {p.nama:<25} Rp{p.harga:>10,.0f} {p.stok:>5}")
            print(f"  Total: {len(items)} produk | O(n)\n")

        # UPDATE_STOK
        elif cmd == "UPDATE_STOK":
            if len(args) < 2:
                print("  [!] Format: UPDATE_STOK <kode> <delta>"); continue
            try:
                delta = int(args[1])
            except ValueError:
                print("  [!] delta harus angka."); continue
            ok = bst.update_stok(args[0].upper(), delta)
            if ok:
                p = bst.search(args[0].upper())
                print(f"  [OK] Stok {args[0].upper()} -> {p.stok} unit | O(log n)")

        # RIWAYAT
        elif cmd == "RIWAYAT":
            if not args:
                print("  [!] Format: RIWAYAT <cust>"); continue
            stack_mgr.tampilkan_riwayat(args[0].upper())

        # UNDO_ORDER
        elif cmd == "UNDO_ORDER":
            if not args:
                print("  [!] Format: UNDO_ORDER <cust>"); continue
            rec = stack_mgr.undo_order(args[0].upper())
            if rec:
                bst.update_stok(rec.kode_produk, rec.qty)
                print(f"  [OK] Stok {rec.kode_produk} +{rec.qty} dikembalikan.")

        # REKOMENDASI
        elif cmd == "REKOMENDASI":
            if not args:
                print("  [!] Format: REKOMENDASI <kode>"); continue
            kode     = args[0].upper()
            hasil_rek = graf.rekomendasikan(kode, max_hop=2)
            if not hasil_rek:
                print(f"  [!] Belum ada co-purchase untuk {kode}. Coba DEMO_SIMULASI.")
            else:
                print(f"\n  ── Rekomendasi untuk {kode} (BFS ≤ 2 hop) ──")
                print(f"  {'Produk':<10} {'Frek':>6}  Nama")
                print(f"  {'─'*45}")
                for kd, frek, hop in hasil_rek[:8]:
                    p = bst.search(kd)
                    nama = p.nama if p else "-"
                    print(f"  {kd:<10} {frek:>5}x  {nama}  (hop={hop})")
                print(f"  Kompleksitas BFS: O(V+E)\n")

        # LAPORAN_HARIAN
        elif cmd == "LAPORAN_HARIAN":
            if laporan.head is None:
                print("  [!] Belum ada order selesai."); continue
            base = datetime(2024, 1, 1, 8, 0, 0)
            ll_b = LLSort(); ll_i = LLSort()
            curr = laporan.head
            i = 0
            while curr:
                wkt = base + timedelta(minutes=curr.waktu_pesan * 5)
                ll_b.append(f"ORD{i+1:04d}", curr.total_harga, wkt)
                ll_i.append(f"ORD{i+1:04d}", curr.total_harga, wkt)
                curr = curr.next; i += 1

            n = ll_b.size()
            print(f"\n  LAPORAN HARIAN — {n} order selesai")
            print(f"  {'═'*52}")

            t0 = time.perf_counter(); bubble_sort_harga_desc(ll_b)
            tb = (time.perf_counter() - t0) * 1000
            t0 = time.perf_counter(); insertion_sort_waktu_asc(ll_i)
            ti = (time.perf_counter() - t0) * 1000

            print(f"  Bubble Sort   (harga DESC) : {tb:.3f} ms | O(n²)")
            print(f"  Insertion Sort (waktu ASC) : {ti:.3f} ms | O(n²)")
            print(f"\n  Top-5 Harga Tertinggi:")
            ll_b.print_table(5)
            print(f"\n  Top-5 Order Terlama:")
            ll_i.print_table(5)
            print(f"  {'═'*52}\n")

        # DEMO
        elif cmd == "DEMO":
            print("\n  [DEMO] 10 order acak masuk...\n")
            for cust, prod, tier in generate_random_orders(10, seed=42):
                p = bst.search(prod)
                if p and p.stok > 0:
                    print(" ", mpq.order(cust, prod, tier))
                    bst.update_stok(prod, -1)
            print("\n  [DEMO] Serve 3x...\n")
            for _ in range(3):
                print(" ", mpq.serve())
            print(); print(mpq.laporan_antrian())

        # DEMO_SIMULASI
        elif cmd == "DEMO_SIMULASI":
            print("  Menjalankan 300 order simulasi (seed=99)...")
            kode_list = [k for k, *_ in PRODUK_DATA]
            simulasi_copurchase(graf, kode_list, n_order=300)

            sim_orders = generate_random_orders(300, seed=99)
            for cust, prod, tier in sim_orders:
                mpq.order(cust, prod, tier)

            count = 0
            for _ in range(150):
                hasil = mpq.serve()
                if "SERVE" in hasil:
                    node = mpq.undo_stack.peek()
                    if node:
                        p     = bst.search(node.product_id)
                        harga = p.harga if p else 0
                        stack_mgr.catat_order(
                            node.customer_id, node.product_id,
                            1, node.tier, harga
                        )
                        waktu_counter[0] += 1
                        laporan.append(
                            node.customer_id, node.product_id,
                            harga, waktu_counter[0]
                        )
                        count += 1

            print(f"  [OK] 300 order masuk, {count} dilayani.")
            print(f"  Graf: {graf.jumlah_node()} node, {graf.jumlah_edge()} edge.")
            print("  Coba: RIWAYAT C001 | REKOMENDASI P050 | LAPORAN_HARIAN\n")

        # BANTUAN
        elif cmd == "BANTUAN":
            cetak_bantuan()

        # KELUAR
        elif cmd == "KELUAR":
            print("\n  Terima kasih! Sistem ditutup.\n"); sys.exit(0)

        else:
            print(f"  [!] Perintah tidak dikenal. Ketik BANTUAN.")


if __name__ == "__main__":
    main()
    
