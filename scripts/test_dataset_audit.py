"""A small synthetic-data test for the dataset-audit workflow."""
import tempfile
import unittest
from pathlib import Path
from vision.audit_dataset import audit


class TestAudit(unittest.TestCase):
    def test_counts_and_no_leakage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for split in ("train", "valid", "test"):
                (root / split / "images").mkdir(parents=True)
                (root / split / "labels").mkdir()
                (root / split / "images" / f"{split}.jpg").write_bytes(b"placeholder")
                (root / split / "labels" / f"{split}.txt").write_text(
                    "0 0.5 0.5 0.2 0.2\n", encoding="utf-8")
            result = audit(root)
            self.assertFalse(result["errors"])
            self.assertTrue(all(v["count"] == 0
                                for v in result["cross_split_source_overlap"].values()))
            self.assertEqual(result["splits"]["train"]["objects"], 1)


if __name__ == "__main__":
    unittest.main()
