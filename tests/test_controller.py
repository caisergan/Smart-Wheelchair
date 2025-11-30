import unittest
from tracking_system.controller import PIDController

class TestPIDController(unittest.TestCase):
    def test_compute_proportional(self):
        # kp=1, ki=0, kd=0
        controller = PIDController(kp=1.0, ki=0.0, kd=0.0)
        output = controller.compute(0.5)
        self.assertEqual(output, 0.5)

    def test_compute_integral(self):
        # kp=0, ki=1, kd=0
        controller = PIDController(kp=0.0, ki=1.0, kd=0.0)
        controller.compute(0.5) # Integral becomes 0.5
        output = controller.compute(0.5) # Integral becomes 1.0
        self.assertEqual(output, 1.0)

    def test_compute_derivative(self):
        # kp=0, ki=0, kd=1
        controller = PIDController(kp=0.0, ki=0.0, kd=1.0)
        controller.compute(0.5) # Prev error 0.5
        output = controller.compute(1.0) # Error 1.0. Derivative = 1.0 - 0.5 = 0.5
        self.assertEqual(output, 0.5)

    def test_compute_none(self):
        controller = PIDController()
        output = controller.compute(None)
        self.assertEqual(output, 0.0)

if __name__ == '__main__':
    unittest.main()
