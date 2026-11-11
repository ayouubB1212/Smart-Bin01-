"""Reconstructed, reproducible training entry point, not original hackathon code."""
from __future__ import annotations
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
import yaml


def main():
    p = argparse.ArgumentParser(description="Train Smart Bin bottle detector")
    p.add_argument("--dataset-root", required=True, type=Path)
    p.add_argument("--weights", default="yolov8m.pt")
    p.add_argument("--epochs", type=int, default=50)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--batch", type=int, default=16)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    root = args.dataset_root.expanduser().resolve()
    for relative in ("train/images", "train/labels", "valid/images", "valid/labels",
                     "test/images", "test/labels"):
        if not (root / relative).is_dir():
            p.error(f"Missing dataset folder: {root / relative}")
    from ultralytics import YOLO
    with TemporaryDirectory() as temp:
        config = Path(temp) / "data.yaml"
        config.write_text(yaml.safe_dump({
            "path": str(root), "train": "train/images", "val": "valid/images",
            "test": "test/images", "nc": 1, "names": ["plastic-bottles"]
        }), encoding="utf-8")
        model = YOLO(args.weights)
        model.train(data=str(config), epochs=args.epochs, imgsz=args.imgsz,
                    batch=args.batch, seed=args.seed, project="runs/detect",
                    name="smartbin", exist_ok=False)
    print("Check resulting runs/detect/smartbin*/weights/best.pt")


if __name__ == "__main__":
    main()
