"""
TCRT5000L 5-Channel IR Line Sensor
Used ONLY in Zone A for line following
"""
import RPi.GPIO as GPIO
import config

class LineSensor:
    def __init__(self):
        """Initialize line sensor GPIO pins"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup sensor pins as inputs with pull-up resistors
        self.sensors = [
            config.LINE_SENSOR_S1,  # Leftmost
            config.LINE_SENSOR_S2,
            config.LINE_SENSOR_S3,  # Center (PRIMARY)
            config.LINE_SENSOR_S4,
            config.LINE_SENSOR_S5   # Rightmost
        ]
        
        for sensor_pin in self.sensors:
            GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def read_all(self):
        """
        Read all 5 sensors
        Returns: List of 5 values [S1, S2, S3, S4, S5]
        0 = Black line detected
        1 = White surface
        """
        return [GPIO.input(pin) for pin in self.sensors]
    
    def read_center(self):
        """
        Read center sensor (S3) - PRIMARY reference
        Returns: 0 (black) or 1 (white)
        """
        return GPIO.input(config.LINE_SENSOR_S3)
    
    def get_line_position(self):
        """
        Calculate line position from sensor readings
        Returns: Position value (-2 to +2)
        -2 = Far left
        -1 = Left
         0 = Center
        +1 = Right
        +2 = Far right
        """
        readings = self.read_all()
        
        # Weighted position calculation
        # S1=-2, S2=-1, S3=0, S4=+1, S5=+2
        weights = [-2, -1, 0, 1, 2]
        
        # Count sensors on line (black = 0)
        on_line = [1 - reading for reading in readings]
        
        if sum(on_line) == 0:
            # No line detected - return last known position or 0
            return 0
        
        # Calculate weighted average
        position = sum(weight * on_line[i] for i, weight in enumerate(weights))
        position = position / sum(on_line)
        
        return position
    
    def is_end_square(self):
        """
        Detect black end square (all sensors on black)
        Returns: True if all sensors detect black
        """
        readings = self.read_all()
        return all(reading == 0 for reading in readings)
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        # GPIO cleanup handled by main program
        pass

