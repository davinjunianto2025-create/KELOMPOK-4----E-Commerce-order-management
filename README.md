# 🛒 E-Commerce Order Management & Recommendation Engine

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Course](https://img.shields.io/badge/Mata%20Kuliah-Algoritma%20%26%20Struktur%20Data-success.svg)]()
[![Status](https://img.shields.io/badge/Status-In%20Progress-yellow.svg)]()

Proyek **E-Commerce Order Management & Recommendation Engine** ini dikembangkan sebagai pemenuhan tugas *Team Based Project* (TA 2025/2026) untuk mata kuliah **ELT60213 Algoritma dan Struktur Data**, Teknik Elektro, Universitas Negeri Yogyakarta.

Sistem ini mensimulasikan platform belanja online yang melayani **50 pelanggan** (C001–C050) dengan **100 produk** (P001–P100) dan **300 order acak**, mencakup manajemen antrian multi-prioritas, katalog produk terindeks, sistem rekomendasi berbasis ko-pembelian, serta riwayat transaksi per pelanggan. Seluruh struktur data dibangun secara murni (*from scratch*) tanpa menggunakan pustaka koleksi bawaan Python.

---

## 👥 Tim Pengembang (Kelompok)

| NIM | Nama Lengkap |
| :--- | :--- |
| **25051030101** | Davin Junianto |
| **25051030088** | Reino Mifta Suputra |
| **25051030109** | Fransisca Laurency |
| **25051030091** | Fikri Octaviansyah |

---

## ✨ Fitur & Modul Utama

Sistem ini dipecah menjadi 6 modul fungsional yang saling terintegrasi:

1. **Modul 1: Multi-Priority Order Queue**
   - Tiga *Queue* berbasis *Custom Linked List* (PREMIUM, REGULAR, ECONOMY).
   - `SERVE` selalu mengutamakan PREMIUM → REGULAR → ECONOMY.
   - Mendukung `CANCEL_LAST` berbasis Stack (undo order terakhir) dan `LAPORAN_ANTRIAN`.
   - Kompleksitas: `enqueue` $O(1)$, `serve` $O(1)$.

2. **Modul 2: BST Katalog Produk**
   - *Binary Search Tree* dengan kunci `kode_produk` (string).
   - Setiap node menyimpan: kode, nama, harga, stok.
   - Mendukung: `insert`, `search`, `update_stok`, `inorder` (katalog terurut), `delete`.
   - Kompleksitas: rata-rata $O(\log n)$.

3. **Modul 3: Graph Rekomendasi (Co-purchase)**
   - Graf produk berbobot: *edge* $(P_i, P_j, w)$ merepresentasikan frekuensi ko-pembelian.
   - Rekomendasi via **BFS** dari produk yang baru dibeli (batas hop ≤ 2).
   - Kompleksitas BFS: $O(V + E)$.

4. **Modul 4: Stack Riwayat Transaksi**
   - *Stack* berbasis *Linked List* per-pelanggan (kapasitas maks 10 transaksi teratas).
   - Mendukung `RIWAYAT <pelanggan>` dan `UNDO_ORDER <pelanggan>`.
   - Kompleksitas: `push`/`pop` $O(1)$.

5. **Modul 5: Sorting Laporan Harian**
   - **Bubble Sort** berdasarkan `total_harga` (descending).
   - **Insertion Sort** berdasarkan `waktu_pesan` (ascending).
   - Keduanya diimplementasikan langsung pada *Linked List*.
   - Eksperimen perbandingan runtime untuk $N = 50, 100, 300$.
   - Kompleksitas: $O(n^2)$.

6. **Modul 6: Command Line Interface (CLI)**
   - Perintah yang didukung: `ORDER <cust> <prod> <tier>`, `SERVE`, `CANCEL_LAST`, `CARI_PRODUK <kode>`, `UPDATE_STOK <kode> <qty>`, `REKOMENDASI <kode_produk>`, `RIWAYAT <cust>`, `LAPORAN_HARIAN`, `KELUAR`.
   - Menampilkan kompleksitas Big-O setiap operasi secara langsung di terminal.

---

## ⚙️ Parameter Sistem

| Parameter | Nilai |
| :--- | :--- |
| Jumlah produk | 100 (kode P001–P100) |
| Jumlah pelanggan | 50 (kode C001–C050) |
| Tingkat prioritas order | 3 (PREMIUM, REGULAR, ECONOMY) |
| Order simulasi | 300 order acak |
| `np.random.seed` | 99 (wajib, untuk reproducibility) |
| Koneksi rekomendasi | Graf produk-produk (co-purchase) |

---

## 📂 Struktur Direktori

```text
📁 PROJECT3/
├── 📁 AI_log/                   # Log Penggunaan AI Assistant
│   └── 📄 log_promt.txt
├── 📁 docs/                     # Berkas Laporan & Presentasi
│   ├── 📄 laporan_final.pdf
│   └── 📄 slide_presentasi.pdf
├── 📁 experiment/               # Skrip Eksperimen Runtime
│   └── 📄 benchmark.py
├── 📁 src/                      # Source Code Utama
│   ├── 📁 data_structures/      # Struktur Data Murni (From Scratch)
│   │   ├── 📄 bst.py            # Binary Search Tree Katalog
│   │   ├── 📄 graph.py          # Graph Rekomendasi (Adjacency List)
│   │   ├── 📄 linked_list.py    # Node & Linked List Dasar
│   │   ├── 📄 queue.py          # Queue berbasis Linked List
│   │   └── 📄 stack.py          # Stack berbasis Linked List
│   ├── 📁 modules/              # Implementasi Modul Aplikasi
│   │   ├── 📄 modules_1.py      # Multi-Priority Order Queue
│   │   ├── 📄 modules_2.py      # BST Katalog Produk
│   │   ├── 📄 modules_3.py      # Graph Rekomendasi & BFS
│   │   ├── 📄 modules_4.py      # Stack Riwayat Transaksi
│   │   ├── 📄 modules_5.py      # Sorting Laporan Harian
│   │   └── 📄 modules_6.py      # CLI E-Commerce
│   └── 📄 main.py               # Entry Point Aplikasi
├── 📁 tests/                    # Unit Testing
│   ├── 📄 test_bst.py
│   ├── 📄 test_graph.py
│   ├── 📄 test_linked_list.py
│   ├── 📄 test_queue.py
│   └── 📄 test_stack.py
├── 📄 .gitignore
└── 📄 README.md
```

---

## 🚀 Cara Menjalankan

### Prasyarat
```bash
pip install numpy
```

### Menjalankan Aplikasi
```bash
cd src
python main.py
```

### Contoh Penggunaan CLI
```
E-Commerce Order Management — Ketik BANTUAN untuk daftar perintah

> ORDER C001 P010 PREMIUM
[✓] Order #1 | C001 → P010 | Tier: PREMIUM | Total: Rp 750.000 | Big-O: O(1)

> SERVE
[✓] Memproses order PREMIUM: #1 | C001 → P010

> CARI_PRODUK P010
[✓] Ditemukan: Laptop Model-10 | Harga: Rp 750.000 | Stok: 45 | Big-O: O(log n)

> REKOMENDASI P010
[✓] Rekomendasi (BFS ≤2 hop): P023, P047, P081 | Big-O: O(V+E)

> RIWAYAT C001
[✓] 10 Transaksi Terakhir C001: ... | Big-O: O(k)

> LAPORAN_HARIAN
> KELUAR
```

### Menjalankan Eksperimen Runtime
```bash
cd experiment
python benchmark.py
```

---

## 📊 Ringkasan Analisis Big-O

| Operasi | Struktur Data | Kompleksitas |
| :--- | :--- | :--- |
| `enqueue` / `serve` | Multi-Priority Queue | $O(1)$ |
| `insert` / `search` BST | BST Katalog | $O(\log n)$ rata-rata |
| Rekomendasi BFS | Graph Co-purchase | $O(V + E)$ |
| `push` / `pop` riwayat | Stack Transaksi | $O(1)$ |
| Sorting laporan | Linked List (Bubble/Insertion) | $O(n^2)$ |

---

## 🔬 Pertanyaan Analisis yang Dijawab di Laporan

1. Trade-off antara 3 Queue terpisah vs 1 Priority Queue (enqueue vs serve) untuk 300 order/hari.
2. Estimasi node yang dijelajahi BFS dalam 2 hop pada graf 100 produk (rata-rata 5 tetangga).
3. Circular buffer array vs Stack Linked List untuk riwayat kapasitas tetap: memori & akses ke-$k$.
4. Perbandingan Bubble Sort vs Insertion Sort pada data hampir terurut — bukti eksperimen runtime.
5. Strategi skalabilitas adjacency list untuk graf produk berjumlah 1 juta node.

---

## 📋 Deliverable

- [x] Kode sumber Python terstruktur per modul
- [ ] Laporan PDF (8–12 halaman)
- [ ] Slide presentasi (10–12 lembar)
- [x] README lengkap
- [x] Folder `AI_Log/` dengan log prompt
-isi dari komputer kamu
