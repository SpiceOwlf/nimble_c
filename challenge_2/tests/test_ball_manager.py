import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ballManager import BallManager

class TestBallManager(unittest.TestCase):
    def setUp(self):
        self.manager = BallManager()

    def test_initialization(self):
        self.assertIsNotNone(self.manager.ball)
        self.assertFalse(self.manager.running)
        self.assertIsNone(self.manager.thread)

    def test_start_stop(self):
        self.manager.start()
        self.assertTrue(self.manager.running)
        self.assertIsNotNone(self.manager.thread)
        
        self.manager.stop()
        self.assertFalse(self.manager.running)

    def test_frame_queue(self):
        self.manager.start()
        frame = self.manager.get_current_frame()
        self.assertIsNotNone(frame)
        self.manager.stop()

if __name__ == '__main__':
    unittest.main() 