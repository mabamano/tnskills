"""
Raspberry Pi Camera Handler
Used ONLY in Zone B for QR code and color detection
"""
import cv2
import numpy as np
from pyzbar import pyzbar
import config

class CameraHandler:
    def __init__(self):
        """Initialize camera"""
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_RESOLUTION[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_RESOLUTION[1])
        
        if not self.camera.isOpened():
            raise Exception("Failed to open camera")
    
    def capture_frame(self):
        """Capture a single frame from camera"""
        ret, frame = self.camera.read()
        if not ret:
            raise Exception("Failed to capture frame")
        return frame
    
    def detect_qr_code(self):
        """
        Detect and decode QR code from camera
        Returns: QR code text (e.g., 'tn-red', 'tn-green', 'tn-blue') or None
        """
        frame = self.capture_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Decode QR codes
        qr_codes = pyzbar.decode(gray)
        
        if qr_codes:
            # Return first QR code text
            qr_text = qr_codes[0].data.decode('utf-8')
            if qr_text in config.QR_CODES:
                return qr_text
        
        return None
    
    def detect_wall_color(self):
        """
        Detect wall color using HSV color space
        Returns: 'red', 'green', or 'blue' or None
        """
        frame = self.capture_frame()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define HSV ranges for red, green, blue
        # Red (wrapping around 180)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        # Green
        lower_green = np.array([40, 50, 50])
        upper_green = np.array([80, 255, 255])
        
        # Blue
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])
        
        # Create masks
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Count pixels in each color range
        red_pixels = cv2.countNonZero(mask_red)
        green_pixels = cv2.countNonZero(mask_green)
        blue_pixels = cv2.countNonZero(mask_blue)
        
        # Find dominant color
        max_pixels = max(red_pixels, green_pixels, blue_pixels)
        
        if max_pixels < 1000:  # Threshold to avoid noise
            return None
        
        if max_pixels == red_pixels:
            return 'red'
        elif max_pixels == green_pixels:
            return 'green'
        elif max_pixels == blue_pixels:
            return 'blue'
        
        return None
    
    def qr_to_color(self, qr_text):
        """
        Convert QR code text to color name
        'tn-red' -> 'red', 'tn-green' -> 'green', 'tn-blue' -> 'blue'
        """
        if qr_text:
            return qr_text.replace('tn-', '')
        return None
    
    def cleanup(self):
        """Release camera resources"""
        if self.camera.isOpened():
            self.camera.release()
        cv2.destroyAllWindows()

