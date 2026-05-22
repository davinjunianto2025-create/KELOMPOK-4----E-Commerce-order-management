"""
Stack Riwayat Transaksi - E-Commerce Order Management & Recommendation Engine
Topik 3 | Domain: Platform Belanja Online

Struktur Data: Stack (berbasis Linked List)
Per-pelanggan: menyimpan maks 10 order terakhir

Operasi:
  - push (catat order)    -> O(1)
  - pop  (undo order)     -> O(1)
  - peek / riwayat        -> O(1) / O(n)

CLI:
  RIWAYAT   <pelanggan>            -> tampilkan 10 order terakhir
  UNDO_ORDER <pelanggan>           -> batalkan order terakhir
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


# ======================================================================
# NODE & ORDER RECORD
# ======================================================================

@dataclass
class OrderRecord:
    """Satu record transaksi yang disimpan dalam stack."""
    order_id   : str
    kode_produk: str
    qty        : int
    tier       : str          # PREMIUM | REGULAR | ECONOMY
    total_harga: float
    waktu      : str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status     : str = "AKTIF"   # AKTIF | DIBATALKAN

    def __str__(self) -> str:
        return (
            f"  [{self.waktu}] {self.order_id} | "
            f"Produk: {self.kode_produk} x{self.qty} | "
            f"Tier: {self.tier} | "
            f"Total: Rp{self.total_harga:,.0f} | "
            f"Status: {self.status}"
        )


class _StackNode:
    """Node internal linked-list untuk stack."""

    def __init__(self, data: OrderRecord):
        self.data: OrderRecord = data
        self.next: _StackNode | None = None


# ======================================================================
# STACK PER PELANGGAN
# ======================================================================

class TransactionStack:
    """
    Stack riwayat transaksi untuk SATU pelanggan.
    Kapasitas maksimum: MAX_SIZE order (default 10).
    Implementasi menggunakan Singly Linked List (top di head).
    """

    MAX_SIZE = 10

    def __init__(self, kode_pelanggan: str):
        self.kode_pelanggan = kode_pelanggan
        self._top: _StackNode | None = None
        self._size: int = 0

    # ------------------------------------------------------------------
    # PUSH  ->  O(1)
    # ------------------------------------------------------------------
    def push(self, order: OrderRecord) -> bool:
        """
        Tambahkan order ke atas stack.
        Jika sudah penuh (10 order), order terlama dibuang (FIFO eviction).
        Return True jika berhasil.
        """
        if self._size == self.MAX_SIZE:
            # Buang elemen terbawah (terlama)
            self._remove_bottom()

        new_node = _StackNode(order)
        new_node.next = self._top
        self._top = new_node
        self._size += 1
        return True

    def _remove_bottom(self):
        """Hapus node paling bawah stack (order terlama). O(n)."""
        if self._top is None:
            return
        if self._top.next is None:
            self._top = None
            self._size -= 1
            return
        current = self._top
        while current.next.next:
            current = current.next
        current.next = None
        self._size -= 1

    # ------------------------------------------------------------------
    # POP / UNDO  ->  O(1)
    # ------------------------------------------------------------------
    def pop(self) -> OrderRecord | None:
        """
        Ambil (hapus) order teratas dari stack.
        Return OrderRecord jika ada, None jika kosong.
        """
        if self._top is None:
            return None
        data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return data

    def undo_order(self) -> OrderRecord | None:
        """
        Batalkan order terakhir pelanggan.
        Menandai status = 'DIBATALKAN' dan mengembalikan record-nya.
        """
        order = self.pop()
        if order is None:
            print(f"[STACK] Tidak ada riwayat order untuk pelanggan {self.kode_pelanggan}.")
            return None
        order.status = "DIBATALKAN"
        print(f"[STACK] Order dibatalkan: {order.order_id} ({order.kode_produk})")
        return order

    # ------------------------------------------------------------------
    # PEEK  ->  O(1)
    # ------------------------------------------------------------------
    def peek(self) -> OrderRecord | None:
        """Lihat order teratas tanpa menghapusnya."""
        return self._top.data if self._top else None

    # ------------------------------------------------------------------
    # RIWAYAT  ->  O(n)
    # ------------------------------------------------------------------
    def riwayat(self, n: int = MAX_SIZE) -> list[OrderRecord]:
        """
        Kembalikan daftar n order terakhir (dari teratas ke terbawah).
        Default n = 10.
        """
        result = []
        current = self._top
        count = 0
        while current and count < n:
            result.append(current.data)
            current = current.next
            count += 1
        return result

    def print_riwayat(self):
        """Tampilkan riwayat transaksi pelanggan ke stdout."""
        orders = self.riwayat()
        header = f"RIWAYAT TRANSAKSI - Pelanggan {self.kode_pelanggan}"
        print(f"\n{'='*65}")
        print(f"{header:^65}")
        print(f"{'='*65}")
        if not orders:
            print("  (Belum ada transaksi)")
        else:
            for i, order in enumerate(orders, 1):
                print(f"  {i:>2}. {order}")
        print(f"{'='*65}")
        print(f"  Total order tercatat: {self._size} / {self.MAX_SIZE}")

    # ------------------------------------------------------------------
    # UTILITY
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0


# ======================================================================
# MANAGER — mengelola stack untuk SEMUA pelanggan (C001–C050)
# ======================================================================

class TransactionStackManager:
    """
    Manager yang menyimpan TransactionStack per pelanggan.
    Diakses via kode_pelanggan (C001–C050).
    """

    def __init__(self):
        self._stacks: dict[str, TransactionStack] = {}

    def _get_or_create(self, kode_pelanggan: str) -> TransactionStack:
        if kode_pelanggan not in self._stacks:
            self._stacks[kode_pelanggan] = TransactionStack(kode_pelanggan)
        return self._stacks[kode_pelanggan]

    # CLI: ORDER <cust> <prod> <tier> <qty>
    def catat_order(
        self,
        kode_pelanggan: str,
        kode_produk   : str,
        qty           : int,
        tier          : str,
        harga_satuan  : float,
        order_id      : str | None = None,
    ) -> OrderRecord:
        """Catat order baru ke stack pelanggan."""
        if order_id is None:
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            order_id = f"ORD-{kode_pelanggan}-{ts}"

        record = OrderRecord(
            order_id    = order_id,
            kode_produk = kode_produk,
            qty         = qty,
            tier        = tier.upper(),
            total_harga = harga_satuan * qty,
        )
        stack = self._get_or_create(kode_pelanggan)
        stack.push(record)
        print(f"[STACK] Order dicatat: {record.order_id} untuk {kode_pelanggan}")
        return record

    # CLI: UNDO_ORDER <cust>
    def undo_order(self, kode_pelanggan: str) -> OrderRecord | None:
        """Batalkan order terakhir pelanggan."""
        stack = self._get_or_create(kode_pelanggan)
        return stack.undo_order()

    # CLI: RIWAYAT <cust>
    def tampilkan_riwayat(self, kode_pelanggan: str):
        """Tampilkan riwayat transaksi pelanggan."""
        stack = self._get_or_create(kode_pelanggan)
        stack.print_riwayat()

    def get_stack(self, kode_pelanggan: str) -> TransactionStack:
        return self._get_or_create(kode_pelanggan)


# ======================================================================
# DEMO / QUICK TEST
# ======================================================================
if __name__ == "__main__":
    manager = TransactionStackManager()

    PELANGGAN = "C007"

    # Simulasi beberapa order
    orders_data = [
        ("P010", 2, "REGULAR",  250_000),
        ("P050", 1, "PREMIUM",  15_000_000),
        ("P001", 3, "ECONOMY",  850_000),
        ("P030", 1, "REGULAR",  450_000),
        ("P090", 2, "PREMIUM",  600_000),
    ]
    for kode_prod, qty, tier, harga in orders_data:
        manager.catat_order(PELANGGAN, kode_prod, qty, tier, harga)

    # Tampilkan riwayat
    manager.tampilkan_riwayat(PELANGGAN)

    # Undo order terakhir
    print("\n[UNDO ORDER TERAKHIR]")
    manager.undo_order(PELANGGAN)

    # Tampilkan riwayat setelah undo
    manager.tampilkan_riwayat(PELANGGAN)

    # Test batas kapasitas: tambah lebih dari 10 order
    print("\n[TEST BATAS KAPASITAS — tambah 7 order lagi]")
    for i in range(7):
        manager.catat_order(PELANGGAN, f"P{i+20:03d}", 1, "ECONOMY", 100_000 * (i + 1))

    manager.tampilkan_riwayat(PELANGGAN)
