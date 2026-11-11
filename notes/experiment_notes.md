# Experiment notes and evidence boundaries

The source archive contains a YOLO-format **plastic-bottles** dataset with 984 images (861 train, 82 validation, 41 test) and 1 object class.

### Evidence retained
- The Roboflow export records EXIF correction, 256 × 256 resizing, horizontal flips, changes in exposure, blur and noise.
- An archived notebook calls Ultralytics \`YOLO("yolov8m.pt")\` and \`train(... epochs=50, imgsz=640, batch=16)\`.
- A \`yolo11n.pt\` checkpoint was in the source archive, but no matching completed fine-tuning log is available.
- Some notebook cells reload **generic YOLOv8m COCO weights**, so downstream predictions cannot prove custom bottle-detection performance.
- The archive does not contain a clearly paired trained \`best.pt\` with test metrics.

### Dataset integrity audit
An earlier audit of the original data reported 984 images and no malformed YOLO labels under its initial format/range checks; no overlap was detected between source-identifiers across the three data splits. This does **not** prove full absence of near-duplicates or image/content leakage. More stringent auditing can uncover extra issues.

### Not established
A validated precision, recall, mAP or latency for a final bottle model; on-device inference or end-to-end automatic camera→Arduino interface; individually attributable team contributions.

### Reproducible future evaluation
Record weights, hardware, software versions, seed, data source/version and class mapping. Use held-out test images and a checkpoint trained on the **plastic-bottles** class. Report precision, recall, mAP@0.5, mAP@0.5:0.95, runtime and failure examples. Do not confuse generic COCO predictions with custom model evaluation.
