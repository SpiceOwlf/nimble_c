import numpy as np
import cv2
import asyncio
import fractions
from aiortc import MediaStreamTrack
from av import VideoFrame

class BallVideoStreamTrack(MediaStreamTrack):
    kind = "video"
    
    def __init__(self, fps=30):
        super().__init__()
        self.frame_count = 0
        self.width = 640
        self.height = 480
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.dx = 5
        self.dy = 5
        self.ball_radius = 20
        self.fps = fps
        
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
        
        # Convert to VideoFrame
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        video_frame.pts = self.frame_count
        video_frame.time_base = fractions.Fraction(1, self.fps)
        
        return video_frame

    def get_ball_position(self):
        return [int(self.ball_x), int(self.ball_y)]

    def set_fps(self, new_fps):
        self.fps = new_fps 

async def main():
    ball = BallVideoStreamTrack()
    
    while True:
        frame = await ball.recv()
        cv2.imshow('Bouncing Ball', frame.to_ndarray(format="bgr24"))  # Convert VideoFrame back to numpy array
        pos = ball.get_ball_position()
        print(f"Ball position: {pos}")
        
        # Break loop on 'q' press
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main()) 