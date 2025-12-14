"""
Buzzer Controller
Provides audio feedback for state transitions
"""
import RPi.GPIO as GPIO
import time
import config

class Buzzer:
    def __init__(self):
        """Initialize buzzer GPIO pin"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(config.BUZZER_PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(config.BUZZER_PIN, config.BUZZER_FREQUENCY)
        self.pwm.start(0)  # Start with 0% duty cycle (silent)
    
    def beep(self, duration=1.0):
        """
        Play beep for specified duration
        Args:
            duration: Beep duration in seconds
        """
        self.pwm.ChangeDutyCycle(50)  # 50% duty cycle for sound
        time.sleep(duration)
        self.pwm.ChangeDutyCycle(0)   # Stop sound
    
    def zone_a_complete(self):
        """Beep for Zone A completion (1 second)"""
        self.beep(config.ZONE_A_BEEP_DURATION)
    
    def placement_success(self):
        """Beep for correct object placement (1 second)"""
        self.beep(config.PLACEMENT_BEEP_DURATION)
    
    def final_completion(self):
        """Beep for final completion (5 seconds)"""
        self.beep(config.FINAL_BEEP_DURATION)
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        self.pwm.stop()
        GPIO.cleanup([config.BUZZER_PIN])

