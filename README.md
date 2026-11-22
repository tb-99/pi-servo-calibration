# Raspberry Pi Pi-Servo Calibration

Pan servo + distance sensor on a Raspberry Pi 4, sweeping to build a radar-style scan.

- `servo.py` – basic servo sweep (Miuzei MS18, GPIO18, gpiozero)
- `servo_cal.py` – two-segment piecewise calibration correcting a measured 6° midpoint error
- `sensor_test.py` – distance sensor bring-up
- `pan_test.py` – pan motion test
- `radar_scan.py` – sweeps and records distance vs. angle
- `scans/` – example scan output

Next: hardware PWM vs. software PWM jitter comparison, encoder feedback (AS5600).
