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


if __name__ == "__main__":
    antrean = QueueLinkedList()

    print(">>> Enqueue order masuk...")
    antrean.enqueue("C001", "P050", "PREMIUM")
    antrean.enqueue("C002", "P010", "REGULAR")
    antrean.enqueue("C003", "P075", "ECONOMY")

    print("\n--- Antrean Sekarang ---")
    antrean.display_queue()

    print("\n>>> Serve order (Dequeue)...")
    order = antrean.dequeue()
    if order:
        print(f"Dilayani: {order.id_pelanggan} | [{order.tier}] Produk: {order.kode_produk}")

    print("\n--- Antrean Setelah Serve ---")
    antrean.display_queue()