"""
L298 Motor Driver Controller
Controls left and right motors via PWM
"""
import RPi.GPIO as GPIO
import config


class MotorController:
    def __init__(self):
        """Initialize motor controller with GPIO pins"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup motor direction pins
        GPIO.setup(config.MOTOR_LEFT_IN1, GPIO.OUT)
        GPIO.setup(config.MOTOR_LEFT_IN2, GPIO.OUT)
        GPIO.setup(config.MOTOR_RIGHT_IN3, GPIO.OUT)
        GPIO.setup(config.MOTOR_RIGHT_IN4, GPIO.OUT)

        # Setup PWM pins
        GPIO.setup(config.MOTOR_LEFT_PWM, GPIO.OUT)
        GPIO.setup(config.MOTOR_RIGHT_PWM, GPIO.OUT)

        # Create PWM objects
        self.left_pwm = GPIO.PWM(config.MOTOR_LEFT_PWM, 1000)  # 1kHz frequency
        self.right_pwm = GPIO.PWM(config.MOTOR_RIGHT_PWM, 1000)

        # Start PWM at 0%
        self.left_pwm.start(0)
        self.right_pwm.start(0)

    def forward(self, speed=None):
        """Move forward"""
        if speed is None:
            speed = config.BASE_SPEED

        GPIO.output(config.MOTOR_LEFT_IN1, GPIO.HIGH)
        GPIO.output(config.MOTOR_LEFT_IN2, GPIO.LOW)
        GPIO.output(config.MOTOR_RIGHT_IN3, GPIO.HIGH)
        GPIO.output(config.MOTOR_RIGHT_IN4, GPIO.LOW)

        self.left_pwm.ChangeDutyCycle(speed)
        self.right_pwm.ChangeDutyCycle(speed)

    def backward(self, speed=None):
        """Move backward"""
        if speed is None:
            speed = config.BASE_SPEED

        GPIO.output(config.MOTOR_LEFT_IN1, GPIO.LOW)
        GPIO.output(config.MOTOR_LEFT_IN2, GPIO.HIGH)
        GPIO.output(config.MOTOR_RIGHT_IN3, GPIO.LOW)
        GPIO.output(config.MOTOR_RIGHT_IN4, GPIO.HIGH)

        self.left_pwm.ChangeDutyCycle(speed)
        self.right_pwm.ChangeDutyCycle(speed)

    def turn_left(self, speed=None):
        """Turn left (left motor backward, right motor forward)"""
        if speed is None:
            speed = config.TURN_SPEED

        GPIO.output(config.MOTOR_LEFT_IN1, GPIO.LOW)
        GPIO.output(config.MOTOR_LEFT_IN2, GPIO.HIGH)
        GPIO.output(config.MOTOR_RIGHT_IN3, GPIO.HIGH)
        GPIO.output(config.MOTOR_RIGHT_IN4, GPIO.LOW)

        self.left_pwm.ChangeDutyCycle(speed)
        self.right_pwm.ChangeDutyCycle(speed)

    def turn_right(self, speed=None):
        """Turn right (left motor forward, right motor backward)"""
        if speed is None:
            speed = config.TURN_SPEED

        GPIO.output(config.MOTOR_LEFT_IN1, GPIO.HIGH)
        GPIO.output(config.MOTOR_LEFT_IN2, GPIO.LOW)
        GPIO.output(config.MOTOR_RIGHT_IN3, GPIO.LOW)
        GPIO.output(config.MOTOR_RIGHT_IN4, GPIO.HIGH)

        self.left_pwm.ChangeDutyCycle(speed)
        self.right_pwm.ChangeDutyCycle(speed)

    def stop(self):
        """Stop all motors"""
        self.left_pwm.ChangeDutyCycle(0)
        self.right_pwm.ChangeDutyCycle(0)

    def set_speeds(self, left_speed, right_speed):
        """Set individual motor speeds (for line following corrections)"""
        # Set directions based on speed sign
        if left_speed >= 0:
            GPIO.output(config.MOTOR_LEFT_IN1, GPIO.HIGH)
            GPIO.output(config.MOTOR_LEFT_IN2, GPIO.LOW)
        else:
            GPIO.output(config.MOTOR_LEFT_IN1, GPIO.LOW)
            GPIO.output(config.MOTOR_LEFT_IN2, GPIO.HIGH)
            left_speed = abs(left_speed)

        if right_speed >= 0:
            GPIO.output(config.MOTOR_RIGHT_IN3, GPIO.HIGH)
            GPIO.output(config.MOTOR_RIGHT_IN4, GPIO.LOW)
        else:
            GPIO.output(config.MOTOR_RIGHT_IN3, GPIO.LOW)
            GPIO.output(config.MOTOR_RIGHT_IN4, GPIO.HIGH)
            right_speed = abs(right_speed)

        # Clamp speeds
        left_speed = max(0, min(100, left_speed))
        right_speed = max(0, min(100, right_speed))

        self.left_pwm.ChangeDutyCycle(left_speed)
        self.right_pwm.ChangeDutyCycle(right_speed)

    def cleanup(self):
        """Cleanup GPIO resources"""
        self.stop()
        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()
