from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, min_angle=0, max_angle=180,
                     min_pulse_width=0.0006, max_pulse_width=0.0023)

CENTER = 84  # commanded angle that looks like a true 90°

def set_angle(target):
    """Map a desired real angle (0-180) to the calibrated command."""
    if target <= 90:
        cmd = target * CENTER / 90
    else:
        cmd = CENTER + (target - 90) * (180 - CENTER) / 90
    servo.angle = cmd

try:
    while True:
        for a in (0, 90, 180, 90):
            set_angle(a)
            print(f"Target: {a}")
            sleep(1)
except KeyboardInterrupt:
    servo.detach()
    print("Stopped")

