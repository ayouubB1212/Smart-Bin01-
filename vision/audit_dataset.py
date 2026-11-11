"""Check one-class YOLO dataset labels, split sizes and augmented-source overlap."""
import argparse
import json
from pathlib import Path


def source_stem(filename):
    return filename.split("_jpg.rf.", 1)[0].split("_png.rf.", 1)[0]


def audit(root):
    report = {"splits": {}, "cross_split_source_overlap": {}, "errors": [], "warnings": []}
    sources = {}
    for split in ("train", "valid", "test"):
        images_dir = root / split / "images"
        labels_dir = root / split / "labels"
        if not images_dir.is_dir() or not labels_dir.is_dir():
            report["errors"].append(f"{split}: missing images or labels directory")
            continue
        images = sorted(p for p in images_dir.iterdir()
                        if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
        labels = sorted(labels_dir.glob("*.txt"))
        img_stems = {p.stem for p in images}
        label_stems = {p.stem for p in labels}
        if img_stems != label_stems:
            report["warnings"].append(
                f"{split}: {len(img_stems - label_stems)} missing labels; "
                f"{len(label_stems - img_stems)} orphan labels")
        objects, empty, invalid = 0, 0, 0
        for label in labels:
            content = label.read_text(encoding="utf-8").strip()
            if not content:
                empty += 1
            for index, line in enumerate(content.splitlines(), 1):
                parts = line.split()
                try:
                    if len(parts) != 5 or parts[0] != "0":
                        raise ValueError("expected class 0 and 4 coordinates")
                    x, y, width, height = map(float, parts[1:])
                    if not all(0 <= v <= 1 for v in (x, y, width, height)):
                        raise ValueError("non-normalized coordinate")
                    if width <= 0 or height <= 0:
                        raise ValueError("empty bounding box")
                    if x - width / 2 < 0 or x + width / 2 > 1:
                        raise ValueError("horizontal box outside image")
                    if y - height / 2 < 0 or y + height / 2 > 1:
                        raise ValueError("vertical box outside image")
                    objects += 1
                except ValueError as exc:
                    invalid += 1
                    report["errors"].append(f"{split}/{label.name}:{index}: {exc}")
        sources[split] = {source_stem(p.name) for p in images}
        report["splits"][split] = {
            "images": len(images), "labels": len(labels), "objects": objects,
            "empty_label_files": empty, "unique_source_stems": len(sources[split]),
            "invalid_boxes": invalid,
        }
    for left, right in (("train", "valid"), ("train", "test"), ("valid", "test")):
        if left not in sources or right not in sources:
            continue
        overlap = sorted(sources[left] & sources[right])
        report["cross_split_source_overlap"][f"{left}/{right}"] = {
            "count": len(overlap), "examples": overlap[:5]
        }
        if overlap:
            report["warnings"].append(f"Possible source overlap: {left}/{right}")
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset-root", type=Path, required=True)
    p.add_argument("--json-output", type=Path)
    args = p.parse_args()
    results = audit(args.dataset_root)
    print(json.dumps(results, indent=2))
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(results, indent=2) + "\n",
                                    encoding="utf-8")
    if results["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
