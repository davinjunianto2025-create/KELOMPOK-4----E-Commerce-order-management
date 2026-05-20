"""
=======================================================
TOPIK 3 - E-Commerce Order Management System
Modul 1: Multi-Priority Order Queue
=======================================================
Implementasi 3 Queue berbasis Linked List (PREMIUM, REGULAR, ECONOMY)
dengan Stack-based undo (CANCEL_LAST) dan laporan antrian.

Struktur Data: Queue (Linked List), Stack
Big-O: enqueue O(1), serve O(1)
=======================================================
"""

import random
from datetime import datetime


# ──────────────────────────────────────────────
#  NODE & LINKED LIST QUEUE
# ──────────────────────────────────────────────

class OrderNode:
    """Satu node di dalam Linked List Queue."""

    def __init__(self, customer_id: str, product_id: str, tier: str):
        self.customer_id = customer_id
        self.product_id  = product_id
        self.tier        = tier
        self.timestamp   = datetime.now().strftime("%H:%M:%S")
        self.next        = None  # pointer ke node berikutnya

    def __str__(self):
        return f"[{self.tier}] {self.customer_id} - {self.product_id} ({self.timestamp})"


class LinkedQueue:
    """
    Queue berbasis Linked List.
    - enqueue  → tambah di tail → O(1)
    - dequeue  → ambil dari head → O(1)
    """

    def __init__(self, tier: str):
        self.tier   = tier
        self.head   = None   # front of queue
        self.tail   = None   # rear of queue
        self._size  = 0

    # ── enqueue O(1) ──
    def enqueue(self, customer_id: str, product_id: str) -> OrderNode:
        node = OrderNode(customer_id, product_id, self.tier)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail      = node
        self._size += 1
        return node

    # ── dequeue O(1) ──
    def dequeue(self) -> OrderNode | None:
        if self.head is None:
            return None
        node       = self.head
        self.head  = self.head.next
        if self.head is None:
            self.tail = None
        node.next  = None
        self._size -= 1
        return node

    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return self._size

    def peek(self) -> OrderNode | None:
        return self.head

    def to_list(self) -> list:
        """Kembalikan semua order di queue ini sebagai list (buat laporan)."""
        result = []
        curr   = self.head
        while curr:
            result.append(curr)
            curr = curr.next
        return result


# ──────────────────────────────────────────────
#  STACK – untuk CANCEL_LAST (undo)
# ──────────────────────────────────────────────

class UndoStack:
    """
    Stack sederhana berbasis list Python.
    Menyimpan order yang sudah di-SERVE,
    sehingga bisa di-undo dengan CANCEL_LAST.
    """

    def __init__(self):
        self._data: list[OrderNode] = []

    def push(self, node: OrderNode):
        self._data.append(node)

    def pop(self) -> OrderNode | None:
        return self._data.pop() if self._data else None

    def peek(self) -> OrderNode | None:
        return self._data[-1] if self._data else None

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)


# ──────────────────────────────────────────────
#  MULTI-PRIORITY ORDER QUEUE  (core system)
# ──────────────────────────────────────────────

TIERS = ["PREMIUM", "REGULAR", "ECONOMY"]


class MultiPriorityOrderQueue:
    """
    Sistem antrian order 3 tingkat prioritas.

    Prioritas serve: PREMIUM → REGULAR → ECONOMY
    Setiap tier punya Linked List Queue sendiri.
    SERVE selalu ambil dari tier tertinggi yang tidak kosong.
    CANCEL_LAST membatalkan order SERVE terakhir via Stack undo.
    """

    def __init__(self):
        self.queues: dict[str, LinkedQueue] = {
            "PREMIUM"  : LinkedQueue("PREMIUM"),
            "REGULAR"  : LinkedQueue("REGULAR"),
            "ECONOMY"  : LinkedQueue("ECONOMY"),
        }
        self.undo_stack = UndoStack()

        self.total_enqueued  = 0
        self.total_served    = 0
        self.total_cancelled = 0

    # ── ORDER ──────────────────────────────────
    def order(self, customer_id: str, product_id: str, tier: str) -> str:
        """Tambahkan order ke antrian sesuai tier. Big-O: O(1)"""
        tier = tier.upper()
        if tier not in TIERS:
            return f"✗ Tier '{tier}' tidak valid. Pilih: PREMIUM / REGULAR / ECONOMY"

        node = self.queues[tier].enqueue(customer_id, product_id)
        self.total_enqueued += 1
        return (
            f"✓ Order masuk  | {node} "
            f"| Posisi antrian {self.queues[tier].size()}"
        )

    # ── SERVE ───────────────────────────────────
    def serve(self) -> str:
        """
        Layani order dari tier tertinggi yang tersedia.
        PREMIUM dulu, lalu REGULAR, lalu ECONOMY.
        Big-O: O(1)
        """
        for tier in TIERS:
            if not self.queues[tier].is_empty():
                node = self.queues[tier].dequeue()
                self.undo_stack.push(node)
                self.total_served += 1
                return f"✓ SERVE        | {node} | Selesai dilayani"

        return "✗ Semua antrian kosong. Tidak ada order untuk dilayani."

    # ── CANCEL_LAST ─────────────────────────────
    def cancel_last(self) -> str:
        """
        Batalkan / undo order yang paling terakhir di-SERVE.
        Order dikembalikan ke posisi HEAD queue tier-nya.
        Big-O: O(1)
        """
        if self.undo_stack.is_empty():
            return "✗ Tidak ada order yang bisa dibatalkan (undo stack kosong)."

        node = self.undo_stack.pop()

        q = self.queues[node.tier]
        node.next = q.head
        q.head    = node
        if q.tail is None:
            q.tail = node
        q._size += 1

        self.total_served    -= 1
        self.total_cancelled += 1
        return (
            f"↩ CANCEL_LAST  | {node} | "
            f"Order dikembalikan ke antrian {node.tier}"
        )

    # ── LAPORAN_ANTRIAN ─────────────────────────
    def laporan_antrian(self) -> str:
        """Tampilkan laporan lengkap semua antrian."""
        lines = []
        lines.append("=" * 60)
        lines.append("          LAPORAN ANTRIAN ORDER")
        lines.append(f"  Waktu   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)

        total_waiting = 0
        for tier in TIERS:
            q     = self.queues[tier]
            items = q.to_list()
            total_waiting += len(items)

            lines.append(f"  [{tier}]  {len(items)} order")
            lines.append("  " + "-" * 40)

            if items:
                for i, node in enumerate(items, 1):
                    lines.append(f"    {i:>3}. {node}")
            else:
                lines.append("    (kosong)")
            lines.append("")

        lines.append("-" * 60)
        lines.append(f"  Total menunggu  : {total_waiting} order")
        lines.append(f"  Total masuk     : {self.total_enqueued} order")
        lines.append(f"  Total dilayani  : {self.total_served} order")
        lines.append(f"  Total dibatalkan: {self.total_cancelled} order")
        lines.append(f"  Undo stack      : {self.undo_stack.size()} entry")
        lines.append("=" * 60)
        return "\n".join(lines)


# ──────────────────────────────────────────────
#  GENERATOR DATA – sesuai parameter sistem
# ──────────────────────────────────────────────

def generate_random_orders(n: int = 300, seed: int = 99) -> list[tuple]:
    """
    Buat n order acak sesuai parameter sistem:
    - 100 produk  : P001–P100
    - 50 pelanggan: C001–C050
    - 3 tier      : PREMIUM, REGULAR, ECONOMY
    - seed        : 99
    """
    random.seed(seed)

    customers = [f"C{str(i).zfill(3)}" for i in range(1, 51)]
    products  = [f"P{str(i).zfill(3)}" for i in range(1, 101)]

    orders = []
    for _ in range(n):
        c    = random.choice(customers)
        p    = random.choice(products)
        tier = random.choice(TIERS)
        orders.append((c, p, tier))
    return orders


# ──────────────────────────────────────────────
#  CLI INTERFACE
# ──────────────────────────────────────────────

def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║   TOPIK 3 - E-Commerce Order Management System      ║
║   Modul 1 : Multi-Priority Order Queue              ║
║   Data Struktur: Queue (Linked List) + Stack        ║
╚══════════════════════════════════════════════════════╝
Perintah yang tersedia:
  ORDER <customer> <produk> <tier>   → Tambah order baru
  SERVE                              → Layani order tertinggi
  CANCEL_LAST                        → Undo order terakhir
  LAPORAN_ANTRIAN                    → Tampilkan semua antrian
  DEMO                               → Isi 10 order random & serve 3
  DEMO_FULL                          → Jalankan 300 order simulasi
  HELP                               → Tampilkan bantuan
  EXIT                               → Keluar program
""")


def print_help():
    print("""
──────────────────────────────────────────────────────
  PANDUAN PENGGUNAAN
──────────────────────────────────────────────────────
  ORDER C001 P005 PREMIUM
      → Customer C001 memesan produk P005, tier PREMIUM

  SERVE
      → Layani 1 order (dari PREMIUM dulu, dst.)

  CANCEL_LAST
      → Batalkan order yang terakhir dilayani (undo)

  LAPORAN_ANTRIAN
      → Lihat seluruh isi antrian per tier + statistik

  DEMO
      → Simulasi kecil: 10 order random, serve 3x, laporan

  DEMO_FULL
      → Simulasi 300 order acak (seed=99), serve ~100x
──────────────────────────────────────────────────────
""")


def run_demo(mpq: MultiPriorityOrderQueue, n: int = 10, serve_count: int = 3):
    """Demo kecil: masukkan n order random, serve beberapa."""
    print(f"\n>>> DEMO: memasukkan {n} order acak...\n")
    orders = generate_random_orders(n, seed=42)
    for cust, prod, tier in orders:
        result = mpq.order(cust, prod, tier)
        print(" ", result)

    print(f"\n>>> DEMO: serve {serve_count}x...\n")
    for _ in range(serve_count):
        print(" ", mpq.serve())

    print()
    print(mpq.laporan_antrian())


def run_demo_full(mpq: MultiPriorityOrderQueue):
    """Simulasi penuh 300 order (seed=99) lalu serve 100."""
    print("\n>>> DEMO_FULL: membuat 300 order acak (seed=99)...\n")
    orders = generate_random_orders(300, seed=99)

    for cust, prod, tier in orders:
        mpq.order(cust, prod, tier)

    print(f"  ✓ 300 order berhasil masuk ke antrian.\n")
    print(">>> DEMO_FULL: melayani 100 order...\n")

    for _ in range(100):
        result = mpq.serve()
        print(f"  {result}")

    print()
    print(mpq.laporan_antrian())


def parse_and_run(cmd_line: str, mpq: MultiPriorityOrderQueue) -> bool:
    """
    Parse satu baris perintah dan jalankan.
    Return False kalau EXIT, True selainnya.
    """
    parts = cmd_line.strip().split()
    if not parts:
        return True

    cmd = parts[0].upper()

    if cmd == "EXIT":
        print("  Sampai jumpa!")
        return False

    elif cmd == "ORDER":
        if len(parts) < 4:
            print("  ✗ Format: ORDER <customer_id> <product_id> <tier>")
        else:
            print(" ", mpq.order(parts[1], parts[2], parts[3]))

    elif cmd == "SERVE":
        print(" ", mpq.serve())

    elif cmd == "CANCEL_LAST":
        print(" ", mpq.cancel_last())

    elif cmd in ("LAPORAN_ANTRIAN", "LAPORAN"):
        print(mpq.laporan_antrian())

    elif cmd == "DEMO":
        run_demo(mpq)

    elif cmd == "DEMO_FULL":
        run_demo_full(mpq)

    elif cmd == "HELP":
        print_help()

    else:
        print(f"  ✗ Perintah '{cmd}' tidak dikenal. Ketik HELP untuk bantuan.")

    return True


def main():
    print_banner()
    mpq = MultiPriorityOrderQueue()

    while True:
        try:
            cmd_line = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Program dihentikan.")
            break

        if not parse_and_run(cmd_line, mpq):
            break


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────

if __name__ == "__main__":
    main()