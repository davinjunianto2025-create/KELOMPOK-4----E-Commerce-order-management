class QueueNode:
    def __init__(self, id_pelanggan, kode_produk, tier):
        self.id_pelanggan = id_pelanggan
        self.kode_produk = kode_produk
        self.tier = tier  # PREMIUM, REGULAR, ECONOMY
        self.next = None


class QueueLinkedList:
    def __init__(self):
        self.head = None  # paling depan
        self.tail = None  # paling belakang
        self.size = 0

    def is_empty(self):
        return self.head is None

    # masukin order baru ke belakang, O(1)
    def enqueue(self, id_pelanggan, kode_produk, tier):
        node = QueueNode(id_pelanggan, kode_produk, tier)

        if self.is_empty():
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

        self.size += 1

    # ambil order dari depan, O(1)
    def dequeue(self):
        if self.is_empty():
            return None

        keluar = self.head
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        self.size -= 1
        return keluar

    def display_queue(self):
        if self.is_empty():
            print("  antrean kosong.")
            return

        curr = self.head
        i = 1
        while curr:
            print(f"  {i}. [{curr.tier}] {curr.id_pelanggan} -> {curr.kode_produk}")
            curr = curr.next
            i += 1

    def to_list(self):
        """Bantu: kembalikan data sebagai list untuk pengecekan."""
        hasil = []
        curr = self.head
        while curr:
            hasil.append((curr.id_pelanggan, curr.kode_produk, curr.tier))
            curr = curr.next
        return hasil


# ──────────────────────────────────────────────────────────────
# TEST DRIVE
# ──────────────────────────────────────────────────────────────
def test_drive():
    print("=" * 50)
    print("  TEST DRIVE - Queue Linked List Order")
    print("=" * 50)

    # ── Test 1: Enqueue normal ─────────────────────────────
    print("\n[TEST 1] Enqueue 3 order:")
    antrean = QueueLinkedList()
    antrean.enqueue("C001", "P050", "PREMIUM")
    antrean.enqueue("C002", "P010", "REGULAR")
    antrean.enqueue("C003", "P075", "ECONOMY")
    antrean.display_queue()
    assert antrean.size == 3, "GAGAL: size harus 3"
    print(f"  ✓ Size antrean = {antrean.size} (benar)")

    # ── Test 2: Dequeue - FIFO ─────────────────────────────
    print("\n[TEST 2] Dequeue - harus keluar C001 duluan (FIFO):")
    order = antrean.dequeue()
    print(f"  Dilayani: {order.id_pelanggan} | [{order.tier}] Produk: {order.kode_produk}")
    assert order.id_pelanggan == "C001", "GAGAL: harus C001 yang keluar duluan"
    assert antrean.size == 2, "GAGAL: size harus 2 setelah dequeue"
    print(f"  ✓ FIFO benar - C001 keluar duluan")
    print(f"  ✓ Size antrean = {antrean.size}")

    print("\n  Antrean setelah dequeue:")
    antrean.display_queue()

    # ── Test 3: Dequeue sampai kosong ─────────────────────
    print("\n[TEST 3] Dequeue sampai kosong:")
    o1 = antrean.dequeue()
    o2 = antrean.dequeue()
    print(f"  Dilayani: {o1.id_pelanggan} [{o1.tier}]")
    print(f"  Dilayani: {o2.id_pelanggan} [{o2.tier}]")
    assert antrean.is_empty(), "GAGAL: antrean harusnya kosong"
    assert antrean.size == 0, "GAGAL: size harus 0"
    print(f"  ✓ Antrean kosong setelah semua di-dequeue")

    # ── Test 4: Dequeue saat kosong ────────────────────────
    print("\n[TEST 4] Dequeue saat antrean kosong:")
    hasil = antrean.dequeue()
    assert hasil is None, "GAGAL: harusnya return None"
    print(f"  ✓ Return None saat kosong - tidak error")

    # ── Test 5: Display saat kosong ────────────────────────
    print("\n[TEST 5] Display saat antrean kosong:")
    antrean.display_queue()
    print("  ✓ Tidak error saat display kosong")

    # ── Test 6: Enqueue banyak tier ────────────────────────
    print("\n[TEST 6] Enqueue berbagai tier:")
    antrean2 = QueueLinkedList()
    antrean2.enqueue("C010", "P001", "ECONOMY")
    antrean2.enqueue("C011", "P002", "PREMIUM")
    antrean2.enqueue("C012", "P003", "REGULAR")
    antrean2.enqueue("C013", "P004", "PREMIUM")
    antrean2.display_queue()
    assert antrean2.size == 4, "GAGAL: size harus 4"
    print(f"  ✓ Size antrean = {antrean2.size} (benar)")

    print("\n" + "=" * 50)
    print("  Semua test selesai.")
    print("=" * 50)


if __name__ == "__main__":
    test_drive()
    