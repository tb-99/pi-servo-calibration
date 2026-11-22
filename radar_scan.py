"""
Single-axis radar sweep using calibrated servo (from servo_cal.py).
Servo: signal->pin 12 (GPIO18), V+->5V, GND->breadboard - rail
Sensor: Trig->pin 16 (GPIO23), Echo->divider node->pin 18 (GPIO24)
Output: scans/scan_<timestamp>.csv and .png
Run: python3 radar_scan.py
"""
import csv
import os
import statistics
from time import sleep, strftime

from gpiozero import AngularServo, DistanceSensor
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---- Calibration (from servo_cal.py) ----
servo = AngularServo(18, min_angle=0, max_angle=180,
                     min_pulse_width=0.0006, max_pulse_width=0.0023)
CENTER = 84  # command that gives a true 90 degrees

# ---- Sweep settings (real angles, 90 = straight ahead) ----
SWEEP_MIN, SWEEP_MAX = 30, 150
STEP_DEG = 3
SETTLE_S = 0.15
PINGS_PER_ANGLE = 3
SCAN_DIR = "scans"

sensor = DistanceSensor(echo=24, trigger=23, max_distance=3.0)


def set_angle(target):
    """Map a real angle (0-180) to the calibrated servo command."""
    if target <= 90:
        cmd = target * CENTER / 90
    else:
        cmd = CENTER + (target - 90) * (180 - CENTER) / 90
    servo.angle = cmd


def read_cm():
    samples = []
    for _ in range(PINGS_PER_ANGLE):
        samples.append(sensor.distance * 100)
        sleep(0.06)
    return statistics.median(samples)


def sweep():
    results = []
    for angle in range(SWEEP_MIN, SWEEP_MAX + 1, STEP_DEG):
        set_angle(angle)
        sleep(SETTLE_S)
        d = read_cm()
        results.append((angle, d))
        print(f"{angle:4d} deg  {d:6.1f} cm")
    return results


def save(results):
    os.makedirs(SCAN_DIR, exist_ok=True)
    stamp = strftime("%Y%m%d_%H%M%S")
    base = os.path.join(SCAN_DIR, f"scan_{stamp}")

    with open(f"{base}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["angle_deg", "distance_cm"])
        w.writerows(results)

    angles = np.radians([a - 90 for a, _ in results])
    dists = [d for _, d in results]
    ax = plt.subplot(projection="polar")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_thetamin(SWEEP_MIN - 90)
    ax.set_thetamax(SWEEP_MAX - 90)
    ax.scatter(angles, dists, s=12)
    ax.set_title("Ultrasonic radar scan (cm)")
    plt.savefig(f"{base}.png", dpi=150, bbox_inches="tight")
    print(f"Saved {base}.csv and {base}.png")


try:
    data = sweep()
    set_angle(90)
    sleep(0.3)
    save(data)
except KeyboardInterrupt:
    print("Stopped")
finally:
    servo.detach()
