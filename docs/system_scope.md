# EcoRecycle system architecture and evidence boundaries

The original ENPO Oran Team QUARTZ presentation brings several disciplines together. They are at **different levels of implementation maturity**.

## Computer vision — archived experiments and demo

Single-class plastic-bottle detection, an annotated dataset and a short video of predictions. The historical notebook uses Ultralytics `YOLO("yolov8m.pt")`. The slideshow refers to YOLO11n, but the final video model remains unverified. No aggregate held-out metric has been established.

## Embedded electronics — code available

The Arduino sketch uses two ultrasonic sensors, a door servo, a motor-control output, a potentiometer as a **simulated weight** and a 16×2 I²C LCD. The provided firmware does not read model predictions from Python and therefore does not prove a deployed camera-to-Arduino link.

## Mechanical system — CAD concept

Presentation sketches/animations show a proposed motorized twin-roller bottle-compression mechanism. CAD animation demonstrates design intent; measured power, throughput and volume-reduction performance were not supplied.

## Power and connected features — proposal

Solar/battery sizing and EcoRecycle Oran app mockups (QR, collection rewards, location, status) are **design concepts**. They are not presented here as a tested commercial battery system or working app/backend.

## What a meaningful next iteration would test

- Re-run vision training with a versioned dataset and saved `best.pt` checkpoint.
- Report precision/recall/mAP and false positives from a genuinely held-out test set.
- Build a bounded, acknowledged serial communication link from camera inference to Arduino.
- Test physical actuation and failure modes on actual wiring and hardware.
- Attribute responsibilities to teammates and clear permissions for public media release.
