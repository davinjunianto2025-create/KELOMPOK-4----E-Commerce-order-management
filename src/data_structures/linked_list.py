class OrderNode:
    def __init__(self, id_pelanggan, kode_produk, total_harga, waktu_pesan):
        self.id_pelanggan = id_pelanggan
        self.kode_produk = kode_produk
        self.total_harga = total_harga
        self.waktu_pesan = waktu_pesan
        self.next = None


class LinkedListLaporan:
    def __init__(self):
        self.head = None

    # nambahin data baru ke paling belakang
    def append(self, id_pelanggan, kode_produk, total_harga, waktu_pesan):
        baru = OrderNode(id_pelanggan, kode_produk, total_harga, waktu_pesan)
        if self.head is None:
            self.head = baru
            return

        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = baru

    # bubble sort descending berdasarkan harga
    # kompleksitas O(n^2)
    def bubble_sort_by_harga_desc(self):
        if self.head is None or self.head.next is None:
            return

        batas = None
        while batas != self.head.next:
            curr = self.head
            while curr.next != batas:
                nxt = curr.next
                if curr.total_harga < nxt.total_harga:
                    # tukar semua datanya
                    curr.id_pelanggan, nxt.id_pelanggan = nxt.id_pelanggan, curr.id_pelanggan
                    curr.kode_produk, nxt.kode_produk = nxt.kode_produk, curr.kode_produk
                    curr.total_harga, nxt.total_harga = nxt.total_harga, curr.total_harga
                    curr.waktu_pesan, nxt.waktu_pesan = nxt.waktu_pesan, curr.waktu_pesan
                curr = curr.next
            batas = curr

    # insertion sort ascending berdasarkan waktu pesan
    # kompleksitas O(n^2)
    def insertion_sort_by_waktu_asc(self):
        if self.head is None or self.head.next is None:
            return

        hasil = None
        curr = self.head

        while curr:
            berikut = curr.next
            hasil = self._insert_terurut(hasil, curr)
            curr = berikut

        self.head = hasil

    def _insert_terurut(self, head_sorted, node_baru):
        if head_sorted is None or head_sorted.waktu_pesan >= node_baru.waktu_pesan:
            node_baru.next = head_sorted
            return node_baru

        curr = head_sorted
        while curr.next is not None and curr.next.waktu_pesan < node_baru.waktu_pesan:
            curr = curr.next

        node_baru.next = curr.next
        curr.next = node_baru
        return head_sorted

    def display(self):
        if self.head is None:
            print("  list kosong.")
            return

        print(f"{'PELANGGAN':<12} | {'PRODUK':<8} | {'TOTAL HARGA':<15} | {'WAKTU PESAN'}")
        print("-" * 55)
        curr = self.head
        while curr:
            print(f"{curr.id_pelanggan:<12} | {curr.kode_produk:<8} | Rp{curr.total_harga:<13} | {curr.waktu_pesan} Telah Selesai")
            curr = curr.next


if __name__ == "__main__":
    laporan = LinkedListLaporan()

    laporan.append("C001", "P050", 1500000, 10)
    laporan.append("C002", "P010", 75000, 5)
    laporan.append("C003", "P075", 300000, 15)
    laporan.append("C004", "P025", 250000, 2)

    print(">>> LAPORAN HARIAN SEBELUM DI-SORTING:")
    laporan.display()

    print("\n>>> (a) BUBBLE SORT - Harga Termahal ke Termurah:")
    laporan.bubble_sort_by_harga_desc()
    laporan.display()

    print("\n>>> (b) INSERTION SORT - Waktu Terlama ke Terbaru:")
    laporan.insertion_sort_by_waktu_asc()
    laporan.display()