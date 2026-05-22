"""
Sorting Laporan Harian – Topik 3 No. 5
Struktur Data: Linked List
Algoritma  : Bubble Sort (total_harga DESC) & Insertion Sort (waktu_pesan ASC)
Big-O      : O(n²)
"""

import random
import time
from datetime import datetime, timedelta

random.seed(99)

# ─────────────────────────────────────────────
# NODE & LINKED LIST
# ─────────────────────────────────────────────
class Node:
    def __init__(self, order_id, total_harga, waktu_pesan):
        self.order_id    = order_id
        self.total_harga = total_harga
        self.waktu_pesan = waktu_pesan   # datetime object
        self.next        = None


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, order_id, total_harga, waktu_pesan):
        new_node = Node(order_id, total_harga, waktu_pesan)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self._size += 1

    def size(self):
        return self._size

    def to_list(self):
        result = []
        cur = self.head
        while cur:
            result.append((cur.order_id, cur.total_harga, cur.waktu_pesan))
            cur = cur.next
        return result

    def print_table(self, max_rows=10):
        print(f"  {'No':<4} {'Order ID':<10} {'Total Harga':>15} {'Waktu Pesan'}")
        print("  " + "-" * 52)
        cur = self.head
        i = 1
        while cur and i <= max_rows:
            print(f"  {i:<4} {cur.order_id:<10} Rp {cur.total_harga:>12,.0f}  {cur.waktu_pesan.strftime('%Y-%m-%d %H:%M')}")
            cur = cur.next
            i += 1
        if self._size > max_rows:
            print(f"  ... dan {self._size - max_rows} data lainnya.")


# ─────────────────────────────────────────────
# BUBBLE SORT – total_harga DESC  O(n²)
# ─────────────────────────────────────────────
def bubble_sort_harga_desc(ll: LinkedList):
    """
    Bubble Sort pada Linked List berdasarkan total_harga descending.
    Swap dilakukan dengan menukar DATA (bukan pointer) agar lebih sederhana.
    Big-O: O(n²) time | O(1) space
    """
    if ll.head is None:
        return

    swapped = True
    while swapped:
        swapped = False
        cur = ll.head
        while cur.next:
            if cur.total_harga < cur.next.total_harga:
                # tukar data
                cur.order_id,    cur.next.order_id    = cur.next.order_id,    cur.order_id
                cur.total_harga, cur.next.total_harga = cur.next.total_harga, cur.total_harga
                cur.waktu_pesan, cur.next.waktu_pesan = cur.next.waktu_pesan, cur.waktu_pesan
                swapped = True
            cur = cur.next


# ─────────────────────────────────────────────
# INSERTION SORT – waktu_pesan ASC  O(n²)
# ─────────────────────────────────────────────
def insertion_sort_waktu_asc(ll: LinkedList):
    """
    Insertion Sort pada Linked List berdasarkan waktu_pesan ascending.
    Membangun sub-list terurut dengan menyisipkan node satu per satu.
    Big-O: O(n²) time | O(1) space
    """
    if ll.head is None or ll.head.next is None:
        return

    sorted_head = None   # kepala linked list yang sudah terurut

    cur = ll.head
    while cur:
        next_node = cur.next

        # sisipkan cur ke posisi yang tepat di sorted list
        if sorted_head is None or cur.waktu_pesan <= sorted_head.waktu_pesan:
            cur.next    = sorted_head
            sorted_head = cur
        else:
            temp = sorted_head
            while temp.next and temp.next.waktu_pesan <= cur.waktu_pesan:
                temp = temp.next
            cur.next  = temp.next
            temp.next = cur

        cur = next_node

    ll.head = sorted_head


# ─────────────────────────────────────────────
# GENERATE DATA
# ─────────────────────────────────────────────
def generate_data(n: int) -> LinkedList:
    ll = LinkedList()
    base_time = datetime(2024, 1, 1, 8, 0, 0)
    times = [base_time + timedelta(minutes=random.randint(0, n * 10)) for _ in range(n)]

    for i in range(n):
        order_id    = f"ORD{i+1:04d}"
        total_harga = random.randint(50_000, 9_999_999)
        waktu_pesan = times[i]
        ll.append(order_id, total_harga, waktu_pesan)
    return ll


# ─────────────────────────────────────────────
# BENCHMARK
# ─────────────────────────────────────────────
SEPARATOR = "=" * 62

def header(title):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def benchmark(n: int):
    header(f"N = {n} ORDER")

    # ── Bubble Sort ──────────────────────────
    ll_bubble = generate_data(n)
    print(f"\n  [Bubble Sort] Data sebelum diurutkan (5 teratas):")
    ll_bubble.print_table(max_rows=5)

    start = time.perf_counter()
    bubble_sort_harga_desc(ll_bubble)
    elapsed_bubble = (time.perf_counter() - start) * 1000   # ms

    print(f"\n  [Bubble Sort] Hasil – total_harga DESCENDING (5 teratas):")
    ll_bubble.print_table(max_rows=5)
    print(f"  ⏱  Runtime Bubble Sort  : {elapsed_bubble:.4f} ms  |  Big-O: O(n²)")

    # ── Insertion Sort ───────────────────────
    ll_insert = generate_data(n)
    print(f"\n  [Insertion Sort] Data sebelum diurutkan (5 teratas):")
    ll_insert.print_table(max_rows=5)

    start = time.perf_counter()
    insertion_sort_waktu_asc(ll_insert)
    elapsed_insert = (time.perf_counter() - start) * 1000   # ms

    print(f"\n  [Insertion Sort] Hasil – waktu_pesan ASCENDING (5 teratas):")
    ll_insert.print_table(max_rows=5)
    print(f"  ⏱  Runtime Insertion Sort: {elapsed_insert:.4f} ms  |  Big-O: O(n²)")

    return elapsed_bubble, elapsed_insert


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print(SEPARATOR)
    print("  SORTING LAPORAN HARIAN – Topik 3 No. 5")
    print("  Bubble Sort (harga DESC) & Insertion Sort (waktu ASC)")
    print("  Implementasi: Linked List  |  Big-O: O(n²)")
    print(SEPARATOR)

    hasil = {}
    for n in [50, 100, 300]:
        hasil[n] = benchmark(n)

    # ── Tabel perbandingan runtime ────────────
    header("PERBANDINGAN RUNTIME")
    print(f"\n  {'N':<6} {'Bubble Sort (ms)':>18} {'Insertion Sort (ms)':>20}")
    print("  " + "-" * 46)
    for n, (b, i) in hasil.items():
        print(f"  {n:<6} {b:>18.4f} {i:>20.4f}")

    print(f"""
  Analisis:
  • Kedua algoritma berjalan dalam O(n²) — waktu naik ~4x
    setiap kali N digandakan (50→100, 100→200, dst).
  • Bubble Sort melakukan lebih banyak swap eksplisit
    sehingga cenderung lebih lambat dari Insertion Sort
    pada data yang hampir terurut.
  • Insertion Sort lebih efisien di kasus terbaik O(n)
    bila data sudah hampir terurut.
""")


if __name__ == "__main__":
    main()
    