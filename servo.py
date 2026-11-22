from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, min_angle=0, max_angle=180,
                     min_pulse_width=0.0006, max_pulse_width=0.0023)

try:
    while True:
        for angle in (0, 90, 180, 90):
            servo.angle = angle
            print(f"Angle: {angle}")
            sleep(1)
except KeyboardInterrupt:
    servo.detach()
    print("Stopped")
