import hashlib
import tempfile
import unittest
from pathlib import Path

from khoade_toolkit.cli import main
from khoade_toolkit.hashing import hash_file
from khoade_toolkit.organizer import category_for, organize
from khoade_toolkit.passwords import SYMBOLS, generate_password
from khoade_toolkit.renamer import apply_plan, plan_rename


class HashTests(unittest.TestCase):
    def test_sha256_matches_hashlib(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.bin"
            path.write_bytes(b"khoade")
            self.assertEqual(hash_file(path), hashlib.sha256(b"khoade").hexdigest())

    def test_unknown_algorithm(self):
        with self.assertRaises(ValueError):
            hash_file(__file__, "crc32")


class PasswordTests(unittest.TestCase):
    def test_length_and_groups(self):
        for _ in range(50):
            password = generate_password(20)
            self.assertEqual(len(password), 20)
            self.assertTrue(any(c.islower() for c in password))
            self.assertTrue(any(c.isupper() for c in password))
            self.assertTrue(any(c.isdigit() for c in password))
            self.assertTrue(any(c in SYMBOLS for c in password))

    def test_without_symbols(self):
        self.assertTrue(generate_password(30, symbols=False).isalnum())

    def test_too_short(self):
        with self.assertRaises(ValueError):
            generate_password(4)


class OrganizerTests(unittest.TestCase):
    def test_category(self):
        self.assertEqual(category_for("foto.JPG"), "Imagens")
        self.assertEqual(category_for("x.desconhecido"), "Outros")

    def test_dry_run_does_not_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "foto.png").write_bytes(b"x")
            moves = organize(root)
            self.assertEqual(len(moves), 1)
            self.assertTrue((root / "foto.png").exists())

    def test_apply_moves_and_avoids_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Imagens").mkdir()
            (root / "Imagens" / "foto.png").write_bytes(b"antiga")
            (root / "foto.png").write_bytes(b"nova")
            organize(root, apply=True)
            self.assertEqual((root / "Imagens" / "foto.png").read_bytes(), b"antiga")
            self.assertEqual((root / "Imagens" / "foto (1).png").read_bytes(), b"nova")

    def test_not_a_directory(self):
        with self.assertRaises(NotADirectoryError):
            organize("/caminho/que/nao/existe")


class RenamerTests(unittest.TestCase):
    def test_rename_sequence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("b.JPG", "a.jpg", "c.txt"):
                (root / name).write_bytes(b"x")
            apply_plan(plan_rename(root, "img_", start=1, width=2))
            self.assertEqual(
                sorted(p.name for p in root.iterdir()),
                ["img_01.jpg", "img_02.jpg", "img_03.txt"],
            )

    def test_rename_when_names_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "f_001.txt").write_text("um")
            (root / "f_002.txt").write_text("dois")
            apply_plan(plan_rename(root, "f_", start=2, width=3))
            self.assertEqual((root / "f_002.txt").read_text(), "um")
            self.assertEqual((root / "f_003.txt").read_text(), "dois")


class CliTests(unittest.TestCase):
    def test_senha_command(self):
        self.assertEqual(main(["senha", "-t", "12"]), 0)

    def test_hash_missing_file(self):
        self.assertEqual(main(["hash", "/nao/existe"]), 1)


if __name__ == "__main__":
    unittest.main()
