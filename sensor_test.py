"""
HC-SR04 bench test (no servo).
Wiring: VCC->pin 2, GND->pin 6, TRIG->pin 16 (GPIO23),
ECHO->10k->row18->pin 18 (GPIO24), row18->10k->10k->GND
Run: python3 sensor_test.py   (Ctrl+C to stop)
"""
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=24, trigger=23, max_distance=3.0)

while True:
    print(f"{sensor.distance * 100:6.1f} cm")
    sleep(0.2)
