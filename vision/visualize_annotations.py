"""Render a few YOLO ground-truth bounding boxes (NOT model predictions)."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument("--split", choices=("train", "valid", "test"), default="valid")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/annotation_previews"))
    args = parser.parse_args()
    images_dir = args.dataset_root / args.split / "images"
    labels_dir = args.dataset_root / args.split / "labels"
    if not images_dir.is_dir() or not labels_dir.is_dir():
        parser.error("Dataset images/labels directories not found.")
    files = [p for p in sorted(images_dir.iterdir())
             if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path in files[:args.limit]:
        image = Image.open(path).convert("RGB")
        width, height = image.size
        draw = ImageDraw.Draw(image)
        label_path = labels_dir / (path.stem + ".txt")
        if label_path.is_file():
            for line in label_path.read_text(encoding="utf-8").splitlines():
                parts = line.split()
                if len(parts) != 5 or parts[0] != "0":
                    continue
                center_x, center_y, box_w, box_h = map(float, parts[1:])
                coords = ((center_x-box_w/2)*width,
                          (center_y-box_h/2)*height,
                          (center_x+box_w/2)*width,
                          (center_y+box_h/2)*height)
                draw.rectangle(coords, outline="red", width=3)
                draw.text((coords[0], max(0, coords[1]-12)),
                          "plastic-bottles", fill="red")
        image.save(args.output_dir / path.name)
    print(f"Saved up to {args.limit} labeled image(s) in {args.output_dir}")


if __name__ == "__main__":
    main()
