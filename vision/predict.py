"""Run inference with a fine-tuned *plastic-bottles* checkpoint."""
import argparse
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--weights", type=Path, required=True)
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--confidence", type=float, default=0.25)
    args = p.parse_args()
    if not args.weights.is_file():
        p.error("Fine-tuned checkpoint not found. Train or recover best.pt.")
    if not args.source.exists():
        p.error("Input source not found.")
    from ultralytics import YOLO
    model = YOLO(str(args.weights))
    classes = list(model.names.values())
    if len(classes) != 1 or classes[0].lower() != "plastic-bottles":
        p.error("Not a fine-tuned plastic-bottles checkpoint; refusing generic COCO inference.")
    results = model.predict(source=str(args.source), save=True, conf=args.confidence)
    print(f"Predicted on {len(results)} image(s); saved visual results.")


if __name__ == "__main__":
    main()
