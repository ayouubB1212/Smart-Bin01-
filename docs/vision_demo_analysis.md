# Computer-vision demo: strengths and failure cases

**Source:** Original Team QUARTZ / ENPO Oran presentation (slides 11–12 and embedded 9.6-second video).

## Observations

- A **plastic bottle** is recognized on screen with a confidence reading around **0.90–0.92**.
- A **roll of adhesive tape** is also labeled `plastic-bottles` with an on-screen confidence around **0.26–0.58**: a visible **false positive**.
- Other non-bottle items shown in the slides also receive detections.
- Camera scenes include varied object positioning, changing backgrounds and human hands.

These are **single-frame confidence values**, **not** the validation accuracy or mAP of the trained model. We have not verified which exact training checkpoint generated the displayed detections.

## What we learned

Computer vision prototypes need more than a compelling successful screenshot. The tape false-positive is an instructive case for:

1. Adding representative **hard negatives** to the dataset.
2. Keeping data splits independent, including near-duplicate or augmented variants.
3. Evaluating held-out precision, recall and **mAP**, not only confidence scores.
4. Recording inference latency and robustness across lighting/occlusion conditions.
5. Saving checkpoint provenance, dataset version and experiment configuration.

## How this relates to dataset benchmarking

The project illustrates the journey from **annotated images → model training → detection examples → failure analysis**. A proper academic/industrial benchmark would extend that approach with fixed splits, reproducible baseline scripts and documented evaluation metrics.

## Caveats

Do not describe the slide demo as proof of production deployment, a reliable end-to-end Arduino integration, or a completed YOLO11n fine-tuning experiment; the available artifacts do not establish those claims.
