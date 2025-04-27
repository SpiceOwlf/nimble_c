import asyncio
import cv2
import numpy as np
from datetime import datetime
from aiortc import VideoStreamTrack
from av import VideoFrame
import fractions

class BallVideoStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.frame_count = 0
        self.ball_x = 320
        self.ball_y = 240
        self.ball_radius = 20
        self.ball_speed_x = 5
        self.ball_speed_y = 5
        self.width = 640
        self.height = 480

    async def recv(self):
        self.frame_count += 1
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y
        
        if self.ball_x - self.ball_radius < 0 or self.ball_x + self.ball_radius > self.width:
            self.ball_speed_x *= -1
        if self.ball_y - self.ball_radius < 0 or self.ball_y + self.ball_radius > self.height:
            self.ball_speed_y *= -1
            
        cv2.circle(frame, (int(self.ball_x), int(self.ball_y)), self.ball_radius, (0, 255, 0), -1)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        video_frame.pts = self.frame_count
        video_frame.time_base = fractions.Fraction(1, 30)
        return video_frame

    def get_ball_position(self):
        return (self.ball_x, self.ball_y)

async def main():
    ball = BallVideoStreamTrack()
    
    while True:
        frame = await ball.recv()
        cv2.imshow('Bouncing Ball', frame.to_ndarray(format="bgr24")) 
        pos = ball.get_ball_position()
        print(f"Ball position: {pos}")
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main()) 