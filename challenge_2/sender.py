import asyncio
import cv2
import numpy as np
import base64
import ffmpeg
from datetime import datetime
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import TcpSocketSignaling
from av import VideoFrame
from findCircleCenter import detect_ball_position
from gracefulShutDown import handle_shutdown

async def setup_webrtc_and_run(ip_address, port):
    global chat_channel, video_channel
    signaling = TcpSocketSignaling(ip_address, port)
    pc = RTCPeerConnection()
    chat_channel = pc.createDataChannel("chat")
    video_channel = pc.createDataChannel("video")
    
    @chat_channel.on("open")
    def on_open():
        print("Data channel opened")
        
    @chat_channel.on("message")
    def on_message(message):
        print(f"Received message: {message}")
    
    width = 640
    height = 480
    fps = 30
    try:
        stream = ffmpeg.input('pipe:', format='h264')
        stream = ffmpeg.output(stream, 'pipe:', format='rawvideo', pix_fmt='bgr24')
        process = ffmpeg.run_async(stream, pipe_stdin=True, pipe_stdout=True)
        print("FFmpeg decoder setup successful")
    except Exception as e:
        print(f"Error setting up FFmpeg decoder: {e}")
        await handle_shutdown(pc, [chat_channel, video_channel], None, [process])
        process = None

    def decode_frame(encoded_frame):
        if process is None:
            return None
        try:
            decoded_frame = process.communicate(input=encoded_frame)[0]
            frame = np.frombuffer(decoded_frame, dtype=np.uint8)
            frame = frame.reshape((height, width, 3))
            return frame
        except Exception as e:
            print(f"Error decoding frame: {e}")
            return None

    @pc.on("datachannel")
    def on_datachannel(channel):
        global ball_position_x, ball_position_y
        print(f"Data channel established: {channel.label}")
        
        if channel.label == "video":
            @channel.on("message")
            def on_message(message):
                try:
                    encoded_frame = base64.b64decode(message)
                    frame = decode_frame(encoded_frame)
                    ball_position_x, ball_position_y = detect_ball_position(frame)
                    message = f"from sender ball position: ,{ball_position_x}, {ball_position_y}"
                    
                    chat_channel.send(message)
                    if frame is not None:
                        cv2.imshow('Received Frame', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cv2.destroyAllWindows()

                except Exception as e:
                    print(f"Error processing video frame: {e}")

    try:
        await signaling.connect()

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)
        await signaling.send(pc.localDescription)

        while True:
            obj = await signaling.receive()
            if isinstance(obj, RTCSessionDescription):
                await pc.setRemoteDescription(obj)
                print("Remote description set")
            elif obj is None:
                print("Signaling ended")
                break
        print("Closing connection")
    finally:
        cv2.destroyAllWindows()
        await handle_shutdown(pc, [chat_channel, video_channel], None, [process])

async def main():
    ip_address = "0.0.0.0"
    port = 8080
    await setup_webrtc_and_run(ip_address, port)

if __name__ == "__main__":
    asyncio.run(main())