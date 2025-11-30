class MotorInterface:
    def __init__(self):
        """Initialize the motor interface."""
        print("Motor Interface Initialized (MOCK)")

    def set_speed(self, left_speed, right_speed):
        """
        Set the speed of the left and right motors.
        
        Args:
            left_speed (float): Speed for left motor (-1.0 to 1.0).
            right_speed (float): Speed for right motor (-1.0 to 1.0).
        """
        # Clamp values
        left_speed = max(-1.0, min(1.0, left_speed))
        right_speed = max(-1.0, min(1.0, right_speed))
        
        print(f"MOTORS -> Left: {left_speed:.2f}, Right: {right_speed:.2f}")

    def stop(self):
        """Stop the motors."""
        self.set_speed(0, 0)
