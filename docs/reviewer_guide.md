# Smart Bin: a quick guide for reviewers

**Project:** EcoRecycle Smart Bin — Team QUARTZ, engineering students at **ENPO Oran**, June 2025.

**Why it matters:** Combines image annotations/model experimentation and Arduino-based sensing/actuation. The hackathon presentation includes a real-looking detection demo, plus valuable examples of **false positives**.

## Two-minute review

1. [Project README](../README.md) — goal and honest scope.
2. [Historic experiment notebook](../notebooks/original_experiment.ipynb) — training configuration, with caveats about generic-vs-fine-tuned checkpoints.
3. [Dataset audit](../notes/dataset_audit_verified.json) and [auditing script](../vision/audit_dataset.py) — how splits and annotations are checked.
4. [Vision demonstration analysis](vision_demo_analysis.md) — both successes and failures from the original presentation.
5. [Arduino sketch](../firmware/SmartBin_Controller/SmartBin_Controller.ino) — sensors, servo, motor and LCD.
6. [System maturity notes](system_scope.md) — implemented, experimented and proposed features kept distinct.

**Most important technical takeaway:** The false-positive on adhesive tape shows why test data, dataset quality, representative negative samples and honest measurement matter more than a cherry-picked detection screenshot.

**Evidence still sought:** original trained model weights, comparable held-out test metrics, confirmed team contributions, permission to release presentation media, and verified end-to-end camera/Arduino communication.
