"""
GPIO Pin Configuration - DO NOT MODIFY
All pins are conflict-free and tested for Raspberry Pi 5
"""

# L298 Motor Driver Pins
MOTOR_LEFT_IN1 = 17    # GPIO 17 - Left motor direction 1
MOTOR_LEFT_IN2 = 18    # GPIO 18 - Left motor direction 2
MOTOR_RIGHT_IN3 = 22   # GPIO 22 - Right motor direction 1
MOTOR_RIGHT_IN4 = 23   # GPIO 23 - Right motor direction 2
MOTOR_LEFT_PWM = 12    # GPIO 12 - Left motor speed (PWM)
MOTOR_RIGHT_PWM = 13   # GPIO 13 - Right motor speed (PWM)

# TCRT5000L Line Sensor Pins (Zone A only)
LINE_SENSOR_S1 = 5     # GPIO 5  - Leftmost sensor
LINE_SENSOR_S2 = 6     # GPIO 6  - Sensor 2
LINE_SENSOR_S3 = 16    # GPIO 16 - Center sensor (PRIMARY)
LINE_SENSOR_S4 = 19    # GPIO 19 - Sensor 4
LINE_SENSOR_S5 = 26    # GPIO 26 - Rightmost sensor

# Buzzer Pin
BUZZER_PIN = 21        # GPIO 21 - Buzzer control

# Camera
# Connected via CSI ribbon - no GPIO pins needed
# Accessed via OpenCV

# Motor PWM Settings (Tune these only)
BASE_SPEED = 70        # Base speed (0-100)
TURN_SPEED = 50        # Turn speed (0-100)
MAX_SPEED = 90         # Maximum speed (0-100)

# Line Following Settings
LINE_SENSOR_THRESHOLD = 0.5  # Threshold for black/white detection
CORRECTION_GAIN = 0.3        # Correction strength for line following

# Camera Settings
CAMERA_RESOLUTION = (640, 480)
QR_CODES = ['tn-red', 'tn-green', 'tn-blue']

# Buzzer Settings
BUZZER_FREQUENCY = 1000  # Hz
ZONE_A_BEEP_DURATION = 1.0  # seconds
PLACEMENT_BEEP_DURATION = 1.0  # seconds
FINAL_BEEP_DURATION = 5.0  # seconds
