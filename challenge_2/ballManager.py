import asyncio
import threading
import queue
import ffmpeg
from av import VideoFrame
from ballAnimation import BallVideoStreamTrack


class BallManager:
    def __init__(self):
        self.ball = BallVideoStreamTrack()
        self.frame_queue = queue.Queue(maxsize=1)
        self.running = False
        self.thread = None
        
        self.width = 640
        self.height = 480
        self.fps = 30
        self.setup_encoder()

    def setup_encoder(self):
        try:
            stream = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='bgr24', s=f'{self.width}x{self.height}', r=self.fps)
            stream = ffmpeg.output(stream, 'pipe:', format='h264', preset='ultrafast', tune='zerolatency')
            self.process = ffmpeg.run_async(stream, pipe_stdin=True, pipe_stdout=True)
            print("FFmpeg encoder setup successful")
        except Exception as e:
            print(f"Error setting up FFmpeg encoder: {e}")
            self.process = None

    def encode_frame(self, frame):
        if self.process is None:
            return None
        try:
            if isinstance(frame, VideoFrame):
                frame = frame.to_ndarray(format="bgr24")
            encoded_frame = self.process.communicate(input=frame.tobytes())[0]
            return encoded_frame
        except Exception as e:
            print(f"Error encoding frame: {e}")
            return None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_ball_animation)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.process:
            self.process.terminate()
            self.process.wait()

    def _run_ball_animation(self):
        while self.running:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                frame = loop.run_until_complete(self.ball.recv())
                if not self.frame_queue.empty():
                    self.frame_queue.get()
                self.frame_queue.put(frame)
            except Exception as e:
                print(f"Error in ball animation: {e}")
                break

    def get_current_frame(self):
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None

    def get_ball_position(self):
        return self.ball.get_ball_position()