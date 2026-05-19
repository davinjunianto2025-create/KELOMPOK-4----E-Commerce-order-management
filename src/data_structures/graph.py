from collections import deque

class RecommendationGraph:
    """Implementasi Graph untuk Mesin Rekomendasi Produk (Co-purchase)"""
    def _init_(self):
        # Menggunakan Adjacency List
        # Format: { 'kode_produk': { 'kode_produk_lain': bobot_frekuensi } }
        self.adj_list = {}

    def add_edge(self, produk1, produk2, weight=1):
        """Menambahkan koneksi bahwa produk1 dan produk2 sering dibeli bersama."""
        if produk1 not in self.adj_list:
            self.adj_list[produk1] = {}
        if produk2 not in self.adj_list:
            self.adj_list[produk2] = {}
        
        # Karena graf tak berarah (undirected), kita hubungkan kedua arah.
        # Jika sudah pernah dibeli bersama, bobotnya akan akumulatif (bertambah).
        self.adj_list[produk1][produk2] = self.adj_list[produk1].get(produk2, 0) + weight
        self.adj_list[produk2][produk1] = self.adj_list[produk2].get(produk1, 0) + weight

    def get_recommendations(self, start_produk, max_hop=2):
        """
        Mencari rekomendasi produk menggunakan algoritma BFS.
        Membatasi pencarian hingga hop tertentu (default <= 2).
        Big-O BFS: O(V + E)
        """
        if start_produk not in self.adj_list:
            return []

        visited = set([start_produk])
        # Queue menyimpan tuple: (node_sekarang, jumlah_hop)
        queue = deque([(start_produk, 0)])
        
        rekomendasi_detail = []

        while queue:
            current_node, current_hop = queue.popleft()

            # Jika sudah mencapai batas hop, jangan mengeksplor tetangganya lagi
            if current_hop >= max_hop:
                continue

            # Eksplorasi produk yang terhubung
            for neighbor, weight in self.adj_list[current_node].items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, current_hop + 1))
                    
                    # Simpan data produk untuk sorting berdasarkan bobot terbesar
                    rekomendasi_detail.append({
                        'produk': neighbor,
                        'hop': current_hop + 1,
                        'weight': weight
                    })
        
        # Urutkan hasil rekomendasi berdasarkan yang paling sering dibeli bersama (weight tertinggi)
        rekomendasi_detail.sort(key=lambda x: x['weight'], reverse=True)
        
        # Ambil list kode produknya saja untuk output akhir
        hasil_rekomendasi = [item['produk'] for item in rekomendasi_detail]
        return hasil_rekomendasi

    def display_graph(self):
        """Menampilkan adjacency list dari graph (untuk testing)"""
        print("\n--- Peta Relasi Produk (Graph Adjacency List) ---")
        for node, edges in self.adj_list.items():
            print(f"Produk {node} terhubung dengan: {edges}")
        print("-" * 50)


# ==========================================
# CONTOH PENGGUNAAN (SIMULASI MODUL 3)
# ==========================================
if _name_ == "_main_":
    graf_rekomendasi = RecommendationGraph()

    # Contoh simulasi produk dibeli bersamaan
    graf_rekomendasi.add_edge("P010", "P075", weight=5)  # Misal: Kaos Polos & Chino Cream
    graf_rekomendasi.add_edge("P010", "P025", weight=2)  # Kaos Polos & Kemeja Coklat
    graf_rekomendasi.add_edge("P075", "P050", weight=4)  # Chino Cream & Sepatu Novablast

    # Cetak struktur graf
    graf_rekomendasi.display_graph()

    # Test pencarian rekomendasi BFS dari produk P010
    produk_input = "P010"
    print(f"\n>>> Input Produk: {produk_input}")
    
    rekomendasi = graf_rekomendasi.get_recommendations(produk_input, max_hop=2)
    print(f"Hasil Rekomendasi BFS (hop <= 2): {rekomendasi}")