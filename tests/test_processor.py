import unittest
import cv2
import numpy as np
from tracking_system.processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()

    def test_process_no_frame(self):
        error, processed_frame = self.processor.process(None)
        self.assertIsNone(error)
        self.assertIsNone(processed_frame)

    def test_process_blank_white_image(self):
        # White image (255) - no black tape
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 255
        error, processed_frame = self.processor.process(frame)
        self.assertIsNone(error)
        self.assertIsNotNone(processed_frame)

    def test_process_black_line_center(self):
        # White image with black vertical line in center
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 255
        # Draw black line in center (width 100, center is 50)
        cv2.line(frame, (50, 0), (50, 100), (0, 0, 0), 10)
        
        error, processed_frame = self.processor.process(frame)
        self.assertIsNotNone(error)
        # Error should be close to 0
        self.assertAlmostEqual(error, 0.0, delta=0.1)

    def test_process_black_line_left(self):
        # White image with black vertical line on left
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 255
        # Draw black line at x=25 (left of center 50)
        cv2.line(frame, (25, 0), (25, 100), (0, 0, 0), 10)
        
        error, processed_frame = self.processor.process(frame)
        self.assertIsNotNone(error)
        # Center is 50. x is 25. Error = (25 - 50) / 50 = -0.5
        self.assertAlmostEqual(error, -0.5, delta=0.1)

    def test_process_black_line_right(self):
        # White image with black vertical line on right
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 255
        # Draw black line at x=75 (right of center 50)
        cv2.line(frame, (75, 0), (75, 100), (0, 0, 0), 10)
        
        error, processed_frame = self.processor.process(frame)
        self.assertIsNotNone(error)
        # Center is 50. x is 75. Error = (75 - 50) / 50 = 0.5
        self.assertAlmostEqual(error, 0.5, delta=0.1)

if __name__ == '__main__':
    unittest.main()
