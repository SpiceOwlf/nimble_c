import unittest
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ballAnimation import BallVideoStreamTrack

class TestBallAnimation(unittest.TestCase):
    def setUp(self):
        self.ball = BallVideoStreamTrack()

    def test_initial_position(self):
        x, y = self.ball.get_ball_position()
        self.assertEqual(x, 320)
        self.assertEqual(y, 240)

    def test_ball_movement(self):
        initial_x, initial_y = self.ball.get_ball_position()
        asyncio.run(self.ball.recv())
        new_x, new_y = self.ball.get_ball_position()
        self.assertNotEqual(initial_x, new_x)
        self.assertNotEqual(initial_y, new_y)

    def test_ball_bounds(self):
        for _ in range(100):
            asyncio.run(self.ball.recv())
            x, y = self.ball.get_ball_position()
            self.assertTrue(0 <= x <= 640)
            self.assertTrue(0 <= y <= 480)

if __name__ == '__main__':
    unittest.main() 