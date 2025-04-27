import unittest
import numpy as np
import cv2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from findCircleCenter import detect_ball_position

class TestCircleDetection(unittest.TestCase):
    def setUp(self):
        self.width = 640
        self.height = 480
        self.radius = 20

    def create_test_frame(self, x, y):
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        cv2.circle(frame, (x, y), self.radius, (0, 255, 0), -1)
        return frame

    def test_detect_circle(self):
        test_x, test_y = 320, 240
        frame = self.create_test_frame(test_x, test_y)
        detected_x, detected_y = detect_ball_position(frame)
        
        self.assertIsNotNone(detected_x)
        self.assertIsNotNone(detected_y)
        self.assertAlmostEqual(detected_x, test_x, delta=5)
        self.assertAlmostEqual(detected_y, test_y, delta=5)

    def test_no_circle(self):
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        result = detect_ball_position(frame)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main() 