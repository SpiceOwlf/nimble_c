import numpy as np
import cv2
import asyncio
from aiortc import MediaStreamTrack
from av import VideoFrame

class BallVideoStreamTrack(MediaStreamTrack):
    kind = "video"
    
    def __init__(self):
        super().__init__()
        self.frame_count = 0
        self.width = 640
        self.height = 480
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.dx = 5
        self.dy = 5
        self.ball_radius = 20
        
    async def recv(self):
        self.frame_count += 1
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Update ball position
        self.ball_x += self.dx
        self.ball_y += self.dy
        
        # Bounce off walls
        if self.ball_x <= self.ball_radius or self.ball_x >= self.width - self.ball_radius:
            self.dx *= -1
        if self.ball_y <= self.ball_radius or self.ball_y >= self.height - self.ball_radius:
            self.dy *= -1
            
        # Draw ball
        cv2.circle(frame, (int(self.ball_x), int(self.ball_y)), self.ball_radius, (0, 255, 0), -1)
        return frame

    def get_ball_position(self):
        return {"x": self.ball_x, "y": self.ball_y}

async def main():
    ball = BallVideoStreamTrack()
    
    while True:
        frame = await ball.recv()
        cv2.imshow('Bouncing Ball', frame)
        
        # Break loop on 'q' press
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main()) 