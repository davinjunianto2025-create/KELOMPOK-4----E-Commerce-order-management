import sys
import os
import unittest
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'data_structures'))
from stack import StackRiwayat, ECommerceHistoryManager


class TestStackPush(unittest.TestCase):
    """Test untuk operasi PUSH pada StackRiwayat."""

    def setUp(self):
        self.stack = StackRiwayat(limit=10)

    def test_push_pertama_jadi_top(self):
        """Elemen pertama yang di-push harus jadi top."""
        self.stack.push("Order P001")
        self.assertEqual(self.stack.top.data, "Order P001")

    def test_push_top_selalu_terbaru(self):
        """Top harus selalu menunjuk elemen yang paling baru di-push."""
        self.stack.push("Order P001")
        self.stack.push("Order P002")
        self.assertEqual(self.stack.top.data, "Order P002")

    def test_push_size_bertambah(self):
        """Size harus bertambah setiap push."""
        self.stack.push("Order P001")
        self.assertEqual(self.stack.size, 1)
        self.stack.push("Order P002")
        self.assertEqual(self.stack.size, 2)

    def test_push_melebihi_limit_size_tetap_10(self):
        """Push lebih dari limit (10), size tidak boleh melebihi limit."""
        for i in range(12):
            self.stack.push(f"Order P{i:03d}")
        self.assertEqual(self.stack.size, 10)

    def test_push_melebihi_limit_elemen_lama_hilang(self):
        """Setelah push ke-11, elemen pertama (terbawah) harus hilang."""
        for i in range(1, 12):
            self.stack.push(f"Order P{i:03d}")

        # Cek dari top ke bottom
        curr = self.stack.top
        data_list = []
        while curr:
            data_list.append(curr.data)
            curr = curr.next

        # P001 (push pertama) harus sudah tidak ada
        self.assertNotIn("Order P001", data_list)
        # P011 (push terakhir) harus ada di top
        self.assertIn("Order P011", data_list)

    def test_push_top_dan_bottom_sama_saat_satu_elemen(self):
        """Saat hanya ada 1 elemen, top dan bottom harus menunjuk node yang sama."""
        self.stack.push("Order P001")
        self.assertEqual(self.stack.top, self.stack.bottom)


class TestStackPop(unittest.TestCase):
    """Test untuk operasi POP pada StackRiwayat."""

    def setUp(self):
        self.stack = StackRiwayat(limit=10)
        self.stack.push("Order P001")
        self.stack.push("Order P002")
        self.stack.push("Order P003")

    def test_pop_ambil_dari_top(self):
        """Pop harus mengambil elemen paling atas (LIFO)."""
        result = self.stack.pop()
        self.assertEqual(result, "Order P003")

    def test_pop_size_berkurang(self):
        """Size harus berkurang setelah pop."""
        self.stack.pop()
        self.assertEqual(self.stack.size, 2)

    def test_pop_urutan_lifo(self):
        """Pop berturut-turut harus mengembalikan urutan LIFO."""
        o3 = self.stack.pop()
        o2 = self.stack.pop()
        o1 = self.stack.pop()
        self.assertEqual(o3, "Order P003")
        self.assertEqual(o2, "Order P002")
        self.assertEqual(o1, "Order P001")

    def test_pop_stack_kosong_return_none(self):
        """Pop pada stack kosong harus return None."""
        s = StackRiwayat()
        result = s.pop()
        self.assertIsNone(result)

    def test_pop_hingga_kosong_top_none(self):
        """Setelah semua elemen di-pop, top dan bottom harus None."""
        s = StackRiwayat()
        s.push("A")
        s.pop()
        self.assertIsNone(s.top)
        self.assertIsNone(s.bottom)

    def test_pop_update_top(self):
        """Setelah pop, top harus bergeser ke elemen berikutnya."""
        self.stack.pop()
        self.assertEqual(self.stack.top.data, "Order P002")


class TestStackDisplayRiwayat(unittest.TestCase):
    """Test untuk DISPLAY_RIWAYAT pada StackRiwayat."""

    def test_display_stack_kosong(self):
        """Display pada stack kosong tidak boleh crash."""
        s = StackRiwayat()
        captured = StringIO()
        sys.stdout = captured
        try:
            s.display_riwayat()
        except Exception as e:
            self.fail(f"display_riwayat() crash pada stack kosong: {e}")
        finally:
            sys.stdout = sys.__stdout__

    def test_display_tampilkan_semua_elemen(self):
        """Display harus menampilkan semua elemen yang ada di stack."""
        s = StackRiwayat()
        s.push("Order P001")
        s.push("Order P002")

        captured = StringIO()
        sys.stdout = captured
        s.display_riwayat()
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        self.assertIn("Order P001", output)
        self.assertIn("Order P002", output)


class TestECommerceHistoryManager(unittest.TestCase):
    """Test untuk ECommerceHistoryManager."""

    def setUp(self):
        self.manager = ECommerceHistoryManager()

    def test_tambah_order_buat_stack_baru(self):
        """Pelanggan baru harus otomatis dibuatkan stack-nya."""
        self.manager.tambah_order("C001", "Order P001")
        self.assertIn("C001", self.manager.riwayat_pelanggan)

    def test_tambah_order_tersimpan_di_stack(self):
        """Order yang ditambah harus tersimpan di top stack pelanggan."""
        self.manager.tambah_order("C001", "Order P001")
        self.assertEqual(
            self.manager.riwayat_pelanggan["C001"].top.data,
            "Order P001"
        )

    def test_undo_order_hapus_top(self):
        """Undo harus menghapus order terakhir dari stack pelanggan."""
        self.manager.tambah_order("C001", "Order P001")
        self.manager.tambah_order("C001", "Order P002")
        self.manager.undo_order("C001")
        self.assertEqual(
            self.manager.riwayat_pelanggan["C001"].top.data,
            "Order P001"
        )

    def test_undo_pelanggan_tidak_ada(self):
        """Undo untuk pelanggan yang tidak ada tidak boleh crash."""
        try:
            self.manager.undo_order("C999")
        except Exception as e:
            self.fail(f"undo_order() crash untuk pelanggan tidak ada: {e}")

    def test_undo_stack_kosong_tidak_crash(self):
        """Undo saat stack pelanggan kosong tidak boleh crash."""
        self.manager.tambah_order("C001", "Order P001")
        self.manager.undo_order("C001")
        try:
            self.manager.undo_order("C001")  # Stack sudah kosong
        except Exception as e:
            self.fail(f"undo_order() crash saat stack kosong: {e}")

    def test_riwayat_pelanggan_tidak_ada(self):
        """Riwayat pelanggan yang tidak ada tidak boleh crash."""
        captured = StringIO()
        sys.stdout = captured
        try:
            self.manager.riwayat("C999")
        except Exception as e:
            self.fail(f"riwayat() crash untuk pelanggan tidak ada: {e}")
        finally:
            sys.stdout = sys.__stdout__

    def test_limit_10_order_per_pelanggan(self):
        """Setelah 12 order, riwayat pelanggan tetap max 10."""
        for i in range(1, 13):
            self.manager.tambah_order("C001", f"Order P{i:03d}")
        self.assertEqual(
            self.manager.riwayat_pelanggan["C001"].size,
            10
        )

    def test_dua_pelanggan_stack_terpisah(self):
        """Dua pelanggan berbeda harus punya stack yang independen."""
        self.manager.tambah_order("C001", "Order C001-P001")
        self.manager.tambah_order("C002", "Order C002-P099")

        self.assertEqual(
            self.manager.riwayat_pelanggan["C001"].top.data,
            "Order C001-P001"
        )
        self.assertEqual(
            self.manager.riwayat_pelanggan["C002"].top.data,
            "Order C002-P099"
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
