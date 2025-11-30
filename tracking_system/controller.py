class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0):
        """
        Initialize the PID controller.
        
        Args:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.prev_error = 0.0
        self.integral = 0.0

    def compute(self, error):
        """
        Compute the control output.
        
        Args:
            error (float): The current error value.
            
        Returns:
            float: The control output.
        """
        if error is None:
            return 0.0
            
        self.integral += error
        derivative = error - self.prev_error
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.prev_error = error
        
        return output
