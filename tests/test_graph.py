from collections import deque


class RecommendationGraph:
    def __init__(self):
        # adjacency list, format -> { 'kode_produk': { 'produk_lain': frekuensi } }
        self.adj_list = {}

    def add_edge(self, produk1, produk2, weight=1):
        if produk1 not in self.adj_list:
            self.adj_list[produk1] = {}
        if produk2 not in self.adj_list:
            self.adj_list[produk2] = {}

        # undirected jadi dua arah, kalo udah ada tinggal ditambah bobotnya
        self.adj_list[produk1][produk2] = self.adj_list[produk1].get(produk2, 0) + weight
        self.adj_list[produk2][produk1] = self.adj_list[produk2].get(produk1, 0) + weight

    # BFS buat cari rekomendasi, dibatasi sampe max_hop
    # O(V + E)
    def get_recommendations(self, start_produk, max_hop=2):
        if start_produk not in self.adj_list:
            return []

        visited = set([start_produk])
        queue = deque([(start_produk, 0)])  # (node, hop sekarang)
        hasil = []

        while queue:
            node, hop = queue.popleft()

            if hop >= max_hop:
                continue

            for tetangga, bobot in self.adj_list[node].items():
                if tetangga not in visited:
                    visited.add(tetangga)
                    queue.append((tetangga, hop + 1))
                    hasil.append({
                        'produk': tetangga,
                        'hop': hop + 1,
                        'weight': bobot
                    })

        # urutkan dari yang paling sering dibeli bareng
        hasil.sort(key=lambda x: x['weight'], reverse=True)

        return hasil  # kembalikan list dict supaya info hop & weight bisa ditampilkan

    def display_graph(self):
        print("\n--- Relasi Antar Produk ---")
        for node, edges in self.adj_list.items():
            print(f"  {node} -> {edges}")
        print("-" * 35)


# ──────────────────────────────────────────────────────────────
# TEST DRIVE
# ──────────────────────────────────────────────────────────────
def test_drive():
    print("=" * 45)
    print("  TEST DRIVE - Graph Rekomendasi Co-Purchase")
    print("=" * 45)

    graf = RecommendationGraph()

    # Tambah edge / relasi antar produk
    graf.add_edge("P010", "P075", weight=5)  # Kaos Polos & Chino Cream
    graf.add_edge("P010", "P025", weight=2)  # Kaos Polos & Kemeja Coklat
    graf.add_edge("P075", "P050", weight=4)  # Chino Cream & Sepatu Novablast
    graf.add_edge("P025", "P050", weight=1)  # Kemeja Coklat & Sepatu Novablast

    # Tampilkan graph
    graf.display_graph()

    # ── Test 1: Rekomendasi dari P010 ──────────────────────
    print("\n[TEST 1] Rekomendasi dari P010 (maks 2 hop)")
    hasil = graf.get_recommendations("P010", max_hop=2)
    if hasil:
        for item in hasil:
            print(f"  produk={item['produk']}  hop={item['hop']}  frekuensi={item['weight']}")
    else:
        print("  Tidak ada rekomendasi.")

    # ── Test 2: Rekomendasi dari P075 ──────────────────────
    print("\n[TEST 2] Rekomendasi dari P075 (maks 2 hop)")
    hasil2 = graf.get_recommendations("P075", max_hop=2)
    if hasil2:
        for item in hasil2:
            print(f"  produk={item['produk']}  hop={item['hop']}  frekuensi={item['weight']}")
    else:
        print("  Tidak ada rekomendasi.")

    # ── Test 3: Produk tidak ada di graph ──────────────────
    print("\n[TEST 3] Rekomendasi dari produk tidak ada (P999)")
    hasil3 = graf.get_recommendations("P999", max_hop=2)
    print(f"  Hasil: {hasil3}  ← seharusnya list kosong []")

    # ── Test 4: max_hop=1 ──────────────────────────────────
    print("\n[TEST 4] Rekomendasi dari P010 (maks 1 hop)")
    hasil4 = graf.get_recommendations("P010", max_hop=1)
    if hasil4:
        for item in hasil4:
            print(f"  produk={item['produk']}  hop={item['hop']}  frekuensi={item['weight']}")
    else:
        print("  Tidak ada rekomendasi.")

    print("\n" + "=" * 45)
    print("  Semua test selesai.")
    print("=" * 45)


if __name__ == "__main__":
    test_drive()
    