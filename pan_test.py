from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, min_angle=0, max_angle=180,
                     min_pulse_width=0.0006, max_pulse_width=0.0023)
CENTER = 84

def set_angle(t):
    cmd = t * CENTER / 90 if t <= 90 else CENTER + (t - 90) * (180 - CENTER) / 90
    servo.angle = cmd

try:
    for a in (90, 60, 90, 120, 90):
        print(f"Going to {a}")
        set_angle(a)
        sleep(2)
finally:
    servo.detach()
