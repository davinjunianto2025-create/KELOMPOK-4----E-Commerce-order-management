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

        return [item['produk'] for item in hasil]

    def display_graph(self):
        print("\n--- Relasi Antar Produk ---")
        for node, edges in self.adj_list.items():
            print(f"  {node} -> {edges}")
        print("-" * 35)


if __name__ == "__main__":
    graf = RecommendationGraph()

    graf.add_edge("P010", "P075", weight=5)  # Kaos Polos & Chino Cream
    graf.add_edge("P010", "P025", weight=2)  # Kaos Polos & Kemeja Coklat
    graf.add_edge("P075", "P050", weight=4)  # Chino Cream & Sepatu Novablast

    graf.display_graph()

    produk_input = "P010"
    print(f"\n>>> Produk dipilih: {produk_input}")

    rekomendasi = graf.get_recommendations(produk_input, max_hop=2)
    print(f"Rekomendasi (maks 2 hop): {rekomendasi}")