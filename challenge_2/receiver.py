import asyncio
import cv2
import numpy as np
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.signaling import TcpSocketSignaling
from av import VideoFrame
from datetime import datetime, timedelta
from ballAnimation import BallVideoStreamTrack
import threading
import queue
import ffmpeg
import base64
from ballManager import BallManager


async def run(pc, signaling, ball_manager):
    await signaling.connect()

    # Create data channel for sending video frames
    channel = pc.createDataChannel("video")
    print("Data channel created for video")

    @channel.on("open")
    def on_open():
        print("Video data channel opened")
        asyncio.create_task(send_frames(channel, ball_manager))

    async def send_frames(channel, ball_manager):
        try:
            frame = ball_manager.get_current_frame()
            if frame is not None:
                # Encode the frame only when sending
                encoded_frame = ball_manager.encode_frame(frame)
                encoded_frame = base64.b64encode(encoded_frame).decode('utf-8')
                channel.send(encoded_frame)
        except Exception as e:
            print(f"Error sending frame: {e}")

    @pc.on("datachannel")
    def on_datachannel(channel):
        print(f"Data channel established: {channel.label}")
        
    #     @channel.on("message")
    #     def on_message(message):
    #         print(f"Received message from sender: {message}")
    #         try:
    #             channel.send(f"Received your message: {message}")
    #         except Exception as e:
    #             print(f"Error sending response: {e}")
        if channel.label == "chat":
            @channel.on("message")
            def on_message(message):
                print(f"Received chat message: {message}")
                try:
                    parts = message.split(',')
                    if len(parts) == 3:
                        ball_id = parts[0]
                        ball_x = float(parts[1])
                        ball_y = float(parts[2])
                        print(f"Ball position: x={ball_x}, y={ball_y}")
                    channel.send(f"Received ball position: {message}")
                except Exception as e:
                    print(f"Error processing chat message: {e}")
        elif channel.label == "video":
            @channel.on("message")
            def on_message(message):
                print(f"Received video message: {message}")

    offer = await signaling.receive()
    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    await signaling.send(pc.localDescription)

    while pc.connectionState != "connected":
        await asyncio.sleep(0.1)
    while True:
        await asyncio.sleep(1)
    print("Closing connection")

async def main():
    signaling = TcpSocketSignaling("0.0.0.0", 8080)
    pc = RTCPeerConnection()
    
    # Initialize ball manager
    ball_manager = BallManager()
    ball_manager.start()
    while True:
        try:
            await run(pc, signaling, ball_manager)
        except Exception as e:
            print(f"Error in main: {str(e)}")
        finally:
            print("Closing peer connection")
            ball_manager.stop()
            cv2.destroyAllWindows()
            await pc.close()

if __name__ == "__main__":
    asyncio.run(main())
