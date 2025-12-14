"""
Main State Machine - TN Skills Robotics Competition
Implements the complete robot control flow
"""
import time
import RPi.GPIO as GPIO
from motor_controller import MotorController
from line_sensor import LineSensor
from camera_handler import CameraHandler
from buzzer import Buzzer
import config

# State definitions
STATE_LINE_FOLLOW = "LINE_FOLLOW"
STATE_ZONE_A_COMPLETE = "ZONE_A_COMPLETE"
STATE_QR_SCAN = "QR_SCAN"
STATE_COLOR_LOCATE = "COLOR_LOCATE"
STATE_MOVE_TO_OBJECT = "MOVE_TO_OBJECT"
STATE_OBJECT_PUSH = "OBJECT_PUSH"
STATE_FINAL = "FINAL"
STATE_STOP = "STOP"


class RobotController:
    def __init__(self):
        """Initialize all robot components"""
        print("Initializing robot components...")

        self.motors = MotorController()
        self.line_sensor = LineSensor()
        self.camera = None  # Lazy initialization - only needed in Zone B
        self.buzzer = Buzzer()

        self.state = STATE_LINE_FOLLOW
        self.detected_colors = []  # Track detected QR colors
        self.current_target_color = None

        print("Robot initialized. Starting state machine...")

    def _ensure_camera(self):
        """Lazy camera initialization - only when entering Zone B"""
        if self.camera is None:
            print("Initializing camera for Zone B...")
            self.camera = CameraHandler()

    def run_line_follow(self):
        """
        Zone A: Line following using TCRT5000L sensors
        Returns: True if Zone A complete (end square detected)
        """
        if self.line_sensor.is_end_square():
            return True

        # Get line position (-2 to +2)
        line_pos = self.line_sensor.get_line_position()

        # Calculate correction
        base_speed = config.BASE_SPEED
        correction = line_pos * config.CORRECTION_GAIN * base_speed

        # Apply correction to motors
        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # Clamp speeds
        left_speed = max(0, min(config.MAX_SPEED, left_speed))
        right_speed = max(0, min(config.MAX_SPEED, right_speed))

        self.motors.set_speeds(left_speed, right_speed)

        return False

    def run_qr_scan(self):
        """
        Zone B: Scan for QR code
        Returns: Detected color name ('red', 'green', 'blue') or None
        """
        self._ensure_camera()  # Initialize camera if not already done
        print("Scanning for QR code...")
        self.motors.stop()
        time.sleep(0.5)  # Brief pause for stability

        qr_text = self.camera.detect_qr_code()

        if qr_text:
            color = self.camera.qr_to_color(qr_text)
            print(f"QR Code detected: {qr_text} -> Color: {color}")
            self.buzzer.beep(0.2)  # Short beep
            return color

        return None

    def run_color_locate(self):
        """
        Zone B: Rotate and detect wall color matching QR code
        Returns: True when matching color found
        """
        self._ensure_camera()  # Initialize camera if not already done
        print(f"Locating {self.current_target_color} wall...")

        # Rotate slowly while scanning
        for _ in range(20):  # Scan for ~2 seconds
            self.motors.turn_right(config.TURN_SPEED)
            time.sleep(0.1)

            wall_color = self.camera.detect_wall_color()

            if wall_color == self.current_target_color:
                print(f"Found {wall_color} wall!")
                self.motors.stop()
                return True

        # If not found, stop anyway
        self.motors.stop()
        return False

    def run_move_to_object(self):
        """
        Zone B: Move toward detected object/wall
        """
        print("Moving toward object...")
        self.motors.forward(config.BASE_SPEED)
        time.sleep(1.0)  # Move forward for 1 second
        self.motors.stop()

    def run_object_push(self):
        """
        Zone B: Push object toward drop box
        """
        print("Pushing object...")
        self.motors.forward(config.BASE_SPEED // 2)  # Slow speed
        time.sleep(2.0)  # Push for 2 seconds
        self.motors.stop()

        # Beep for successful placement attempt
        self.buzzer.placement_success()

    def state_machine_step(self):
        """Execute one step of the state machine"""
        if self.state == STATE_LINE_FOLLOW:
            if self.run_line_follow():
                self.state = STATE_ZONE_A_COMPLETE

        elif self.state == STATE_ZONE_A_COMPLETE:
            print("Zone A complete!")
            self.motors.stop()
            self.buzzer.zone_a_complete()
            time.sleep(0.5)
            self.state = STATE_QR_SCAN

        elif self.state == STATE_QR_SCAN:
            color = self.run_qr_scan()
            if color:
                self.current_target_color = color
                self.detected_colors.append(color)
                self.state = STATE_COLOR_LOCATE
            time.sleep(0.1)  # Small delay before next scan

        elif self.state == STATE_COLOR_LOCATE:
            if self.run_color_locate():
                self.state = STATE_MOVE_TO_OBJECT
            else:
                # Color not found, try next QR or continue
                self.state = STATE_QR_SCAN

        elif self.state == STATE_MOVE_TO_OBJECT:
            self.run_move_to_object()
            self.state = STATE_OBJECT_PUSH

        elif self.state == STATE_OBJECT_PUSH:
            self.run_object_push()

            # Check if we've processed all colors (assuming 3 colors)
            if len(self.detected_colors) >= 3:
                self.state = STATE_FINAL
            else:
                # Go back to QR scanning for next color
                self.state = STATE_QR_SCAN

        elif self.state == STATE_FINAL:
            print("Mission complete!")
            self.motors.stop()
            self.buzzer.final_completion()
            self.state = STATE_STOP

        elif self.state == STATE_STOP:
            return False  # Signal to stop main loop

        return True  # Continue running

    def run(self):
        """Main execution loop"""
        try:
            print("Starting robot...")
            while self.state_machine_step():
                time.sleep(0.01)  # Small delay to prevent CPU overload

        except KeyboardInterrupt:
            print("\nInterrupted by user")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup all resources"""
        print("Cleaning up...")
        self.motors.stop()
        self.motors.cleanup()
        if self.camera is not None:
            self.camera.cleanup()
        self.buzzer.cleanup()
        GPIO.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    robot = RobotController()
    robot.run()
