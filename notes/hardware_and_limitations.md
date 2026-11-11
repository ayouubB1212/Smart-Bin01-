# Arduino hardware: documented behavior and limitations

The archived \`SmartBin_Controller.ino\` sketches a prototype with:

| Arduino connection | Purpose |
|---|---|
| A0 | Potentiometer representing a *simulated* weight signal |
| 9 / 10 | Fill-level ultrasonic sensor TRIG / ECHO |
| 7 / 6 | Bottle-entry ultrasonic sensor TRIG / ECHO |
| 8 | Door servomotor |
| 5 | DC motor-control output |
| I²C | 16×2 status LCD, default address 0x27 |

It estimates a fill percentage from distance thresholds (70 cm empty, 12.5 cm full), reacts to an approaching object at the inlet, drives the motor output for a timed interval, opens/closes the servo at a threshold and shows status on the LCD.

### Safety and implementation caveats

- **Never drive a DC motor directly from an Arduino GPIO pin.** Use a suitable driver and power supply, with protection appropriate to the motor.
- The displayed \`W:%dg\` number is the raw potentiometer ADC reading, **not grams** from a calibrated weight sensor.
- \`pulseIn\` timeout is interpreted as a large distance. Proper fault handling and filtering are future work.
- There are blocking delays in setup and loop; this is an educational prototype, not real-time safety-certified control.
- \`stopDoorServo()\` writes 0° before detaching. Hardware movement and final closure must be verified on the physical assembly.
- This file does not contain serial messages from a CV model. The camera→Arduino control integration was a proposed next step rather than demonstrated in the supplied source.

These limits are documented explicitly to distinguish prototype exploration from an industrialized system.
