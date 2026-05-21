"""
benchmark.py - Performance Benchmarking
E-Commerce Order Management & Recommendation Engine
Topik 3 | experiments/

Mengukur runtime semua struktur data:
  - BST Katalog Produk     : insert, search, delete
  - Stack Riwayat          : push, pop
  - Queue Multi-Priority   : enqueue, dequeue
  - Sorting Laporan Harian : Bubble Sort vs Insertion Sort
  - Linked List            : append, search

N yang diuji: 50, 100, 300 (sesuai spesifikasi modul 5)
"""

import time
import random
import string
import sys
import os

# ── Path setup ────────────────────────────────────────────────────────
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# Coba import modul project; fallback ke implementasi inline jika belum ada
try:
    from data_structures.bst   import BSTKatalogProduk
    from data_structures.stack import TransactionStack
    BST_AVAILABLE   = True
    STACK_AVAILABLE = True
except ImportError:
    BST_AVAILABLE   = False
    STACK_AVAILABLE = False


# ======================================================================
# HELPER UTILITIES
# ======================================================================

def timer(fn, *args, **kwargs):
    """Jalankan fn(*args) dan kembalikan (result, elapsed_ms)."""
    start  = time.perf_counter()
    result = fn(*args, **kwargs)
    end    = time.perf_counter()
    return result, (end - start) * 1_000   # ms


def random_kode(prefix="P", n=3) -> str:
    return prefix + str(random.randint(1, 10**n)).zfill(n)


def print_header(title: str):
    bar = "=" * 60
    print(f"\n{bar}")
    print(f"  {title}")
    print(bar)


def print_row(label: str, n: int, ms: float):
    print(f"  {label:<30} N={n:<5}  {ms:>10.4f} ms")


# ======================================================================
# 1. BST BENCHMARK
# ======================================================================

def _inline_bst_benchmark(N: int) -> dict:
    """BST minimal inline (fallback jika modul belum ada)."""

    class Node:
        def __init__(self, k, v):
            self.k, self.v, self.left, self.right = k, v, None, None

    class BST:
        def __init__(self): self.root = None
        def insert(self, k, v):
            n = Node(k, v)
            if not self.root: self.root = n; return
            c = self.root
            while True:
                if k < c.k:
                    if not c.left: c.left = n; return
                    c = c.left
                else:
                    if not c.right: c.right = n; return
                    c = c.right
        def search(self, k):
            c = self.root
            while c:
                if k == c.k: return c
                c = c.left if k < c.k else c.right
            return None

    bst  = BST()
    keys = [f"P{i:03d}" for i in range(1, N + 1)]
    random.shuffle(keys)

    _, t_insert = timer(lambda: [bst.insert(k, i) for i, k in enumerate(keys)])
    _, t_search = timer(lambda: [bst.search(k)    for k in keys])
    return {"insert": t_insert, "search": t_search}


def benchmark_bst(sizes: list[int]):
    print_header("BST KATALOG PRODUK")
    print(f"  {'Operasi':<30} {'N':<8} {'Waktu':>12}")
    print(f"  {'-'*52}")

    for N in sizes:
        if BST_AVAILABLE:
            bst   = BSTKatalogProduk()
            keys  = [f"P{i:03d}" for i in range(1, N + 1)]
            names = [f"Produk-{i}" for i in range(N)]
            random.shuffle(keys)

            _, t_ins = timer(lambda: [
                bst.insert(k, names[i], random.randint(10_000, 5_000_000), random.randint(1, 100))
                for i, k in enumerate(keys)
            ])
            _, t_srch = timer(lambda: [bst.search(k) for k in keys])
            _, t_del  = timer(lambda: bst.delete(keys[0]))

            print_row("insert", N, t_ins)
            print_row("search", N, t_srch)
            print_row("delete", N, t_del)
        else:
            res = _inline_bst_benchmark(N)
            print_row("insert (inline)", N, res["insert"])
            print_row("search (inline)", N, res["search"])

        print()


# ======================================================================
# 2. STACK BENCHMARK
# ======================================================================

def benchmark_stack(sizes: list[int]):
    print_header("STACK RIWAYAT TRANSAKSI")
    print(f"  {'Operasi':<30} {'N':<8} {'Waktu':>12}")
    print(f"  {'-'*52}")

    for N in sizes:
        if STACK_AVAILABLE:
            stack = TransactionStack("C001")
            from data_structures.stack import OrderRecord

            orders = [
                OrderRecord(f"ORD-{i:04d}", f"P{i%100:03d}", random.randint(1, 5),
                            random.choice(["PREMIUM", "REGULAR", "ECONOMY"]),
                            random.randint(50_000, 10_000_000))
                for i in range(N)
            ]
            _, t_push = timer(lambda: [stack.push(o) for o in orders])
            _, t_pop  = timer(lambda: [stack.pop()   for _ in range(min(N, stack.MAX_SIZE))])
        else:
            # Inline stack
            class _Stack:
                def __init__(self): self._d = []
                def push(self, v):
                    if len(self._d) >= 10: self._d.pop(0)
                    self._d.append(v)
                def pop(self): return self._d.pop() if self._d else None

            st = _Stack()
            _, t_push = timer(lambda: [st.push(i) for i in range(N)])
            _, t_pop  = timer(lambda: [st.pop()   for _ in range(10)])

        print_row("push", N, t_push)
        print_row("pop",  N, t_pop)
        print()


# ======================================================================
# 3. QUEUE BENCHMARK (inline, multi-priority)
# ======================================================================

def benchmark_queue(sizes: list[int]):
    print_header("QUEUE MULTI-PRIORITY")
    print(f"  {'Operasi':<30} {'N':<8} {'Waktu':>12}")
    print(f"  {'-'*52}")

    class PriorityQueue:
        """3 antrian: PREMIUM > REGULAR > ECONOMY."""
        def __init__(self):
            self.premium  = []
            self.regular  = []
            self.economy  = []

        def enqueue(self, item, tier: str):
            tier = tier.upper()
            if   tier == "PREMIUM":  self.premium.append(item)
            elif tier == "REGULAR":  self.regular.append(item)
            else:                    self.economy.append(item)

        def dequeue(self):
            if self.premium: return self.premium.pop(0), "PREMIUM"
            if self.regular: return self.regular.pop(0), "REGULAR"
            if self.economy: return self.economy.pop(0), "ECONOMY"
            return None, None

    tiers = ["PREMIUM", "REGULAR", "ECONOMY"]

    for N in sizes:
        pq     = PriorityQueue()
        orders = [(f"ORD-{i:04d}", random.choice(tiers)) for i in range(N)]

        _, t_enq = timer(lambda: [pq.enqueue(o, t) for o, t in orders])
        _, t_deq = timer(lambda: [pq.dequeue()     for _ in range(N)])

        print_row("enqueue", N, t_enq)
        print_row("dequeue (serve)", N, t_deq)
        print()


# ======================================================================
# 4. SORTING BENCHMARK — Bubble vs Insertion (sesuai Modul 5 Spek)
# ======================================================================

def bubble_sort(arr: list) -> list:
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def insertion_sort(arr: list) -> list:
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j   = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j        -= 1
        a[j + 1] = key
    return a


def benchmark_sorting(sizes: list[int]):
    print_header("SORTING LAPORAN HARIAN (Bubble vs Insertion)")
    print(f"  {'Algoritma':<30} {'N':<8} {'Waktu':>12}  {'Winner'}")
    print(f"  {'-'*58}")

    for N in sizes:
        # Data: simulasi total_harga acak (descending sort by harga)
        data = [random.randint(10_000, 50_000_000) for _ in range(N)]

        _, t_bubble    = timer(bubble_sort,    data)
        _, t_insertion = timer(insertion_sort, data)

        winner_b = "✓" if t_bubble    < t_insertion else ""
        winner_i = "✓" if t_insertion < t_bubble    else ""

        print_row("Bubble Sort",    N, t_bubble)
        print(f"  {'':30} {'':8} {'':>12}  {winner_b}")
        print_row("Insertion Sort", N, t_insertion)
        print(f"  {'':30} {'':8} {'':>12}  {winner_i}")
        diff = abs(t_bubble - t_insertion)
        faster = "Insertion" if t_insertion < t_bubble else "Bubble"
        print(f"  → {faster} Sort lebih cepat {diff:.4f} ms untuk N={N}")
        print()


# ======================================================================
# 5. LINKED LIST BENCHMARK
# ======================================================================

def benchmark_linked_list(sizes: list[int]):
    print_header("LINKED LIST (Laporan Harian)")
    print(f"  {'Operasi':<30} {'N':<8} {'Waktu':>12}")
    print(f"  {'-'*52}")

    class _Node:
        def __init__(self, v): self.v = v; self.next = None

    class LinkedList:
        def __init__(self): self.head = None; self._size = 0
        def append(self, v):
            n = _Node(v)
            if not self.head: self.head = n; self._size += 1; return
            c = self.head
            while c.next: c = c.next
            c.next = n; self._size += 1
        def search(self, v):
            c = self.head
            while c:
                if c.v == v: return c
                c = c.next
            return None

    for N in sizes:
        ll   = LinkedList()
        vals = list(range(N))
        random.shuffle(vals)

        _, t_app  = timer(lambda: [ll.append(v) for v in vals])
        _, t_srch = timer(lambda: [ll.search(v) for v in vals])

        print_row("append", N, t_app)
        print_row("search (linear)", N, t_srch)
        print()


# ======================================================================
# MAIN — jalankan semua benchmark
# ======================================================================

def main():
    SIZES = [50, 100, 300]   # sesuai spesifikasi Modul 5

    print("\n" + "█" * 60)
    print("  BENCHMARK — E-Commerce Order Management")
    print("  Topik 3 | Data Structures Performance Test")
    print("  N yang diuji:", SIZES)
    print("█" * 60)

    random.seed(99)   # reproducible (np.random.seed = 99 dari spek)

    benchmark_bst(SIZES)
    benchmark_stack(SIZES)
    benchmark_queue(SIZES)
    benchmark_sorting(SIZES)
    benchmark_linked_list(SIZES)

    print("\n" + "=" * 60)
    print("  ✅ Benchmark selesai.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
