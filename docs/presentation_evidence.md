# EcoRecycle — Original project presentation

**Origin:** Team QUARTZ, student hackathon group at **École Nationale Polytechnique d'Oran (ENPO), Oran, Algeria**, June 2025.

The 44-slide presentation titled *« Vous jetez, elle pense : la poubelle du futur »* describes a broader **EcoRecycle** system concept than the source code preserved in the repository. The deck contains two embedded short clips.

| Slides | Evidence in the slides | What it establishes |
|---|---|---|
| 5–12 | Vision workflow, dataset and live-looking detection screens / 9.6-second demo | Bottle detection experiment, including success and failure cases |
| 13–19 | CAD views and 12.6-second mechanical animation of paired rollers | Proposed mechanical bottle-compaction design, **not validated crushing tests** |
| 20–22 | Solar/battery sizing and consumption estimates | Preliminary power budget, not field measurements |
| 23–31 | Electronics diagrams, ultrasonic sensors, Arduino, servo, motor and LCD | Embedded-control architecture consistent with saved sketch |
| 32–41 | EcoRecycle Oran mobile-app screens: locations, QR codes, points and status | App **interface concept**, not proven deployed mobile backend |
| 42–44 | Cost estimate, conclusions, team credit | Pitch material; numerical financial claims not independently verified |

**Data from archived code:** 984 images split as 861 training / 82 validation / 41 test; single `plastic-bottles` YOLO class. [See audit evidence](../notes/dataset_audit_verified.json).

**Important evidence distinction:** The presentation discusses **YOLO11n**, but the preserved notebook runs **YOLOv8m** training. We cannot identify the exact checkpoint powering the presentation's demo, or establish quantitative mAP or precision/recall, from the supplied materials alone.

**Credit:** This was a collaborative student project of **Team QUARTZ at ENPO Oran**. The repository is maintained by Ayoub ANANI, but not all subproject contributions can be assigned to an individual without teammate confirmation.
