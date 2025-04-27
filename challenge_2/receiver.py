import asyncio
import base64
from aiortc import RTCPeerConnection
from aiortc.contrib.signaling import TcpSocketSignaling
from ballManager import BallManager
from gracefulShutDown import handle_shutdown

async def run(pc, signaling, ball_manager):
    await signaling.connect()

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
                encoded_frame = ball_manager.encode_frame(frame)
                encoded_frame = base64.b64encode(encoded_frame).decode('utf-8')
                channel.send(encoded_frame)
        except Exception as e:
            print(f"Error sending frame: {e}")
            await handle_shutdown(pc, [channel], None, None)

    @pc.on("datachannel")
    def on_datachannel(channel):
        print(f"Data channel established: {channel.label}")
        
        if channel.label == "chat":
            @channel.on("message")
            async def on_message(message):
                print(f"Received chat message: {message}")
                try:
                    parts = message.split(',')
                    if len(parts) == 3:
                        ball_id = parts[0]
                        ball_x = float(parts[1])
                        ball_y = float(parts[2])
                        cur_x, cur_y = ball_manager.get_ball_position()
                        print("current ball position:", cur_x, cur_y)
                        error_x = ball_x - cur_x
                        error_y = ball_y - cur_y
                        message = f"ball_error,{error_x},{error_y}"
                        channel.send(message)
                except Exception as e:
                    print(f"Error processing chat message: {e}")
                    await handle_shutdown(pc, channel, ball_manager, signaling)
        elif channel.label == "video":
            @channel.on("message")
            async def on_message(message):
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
    

async def main():
    signaling = TcpSocketSignaling("0.0.0.0", 8080)
    pc = RTCPeerConnection()
    
    ball_manager = BallManager()
    ball_manager.start()
    while True:
        try:
            await run(pc, signaling, ball_manager)
        except Exception as e:
            print(f"Error in main: {str(e)}")
            await handle_shutdown(pc, None, ball_manager, signaling)
        finally:
            print("Closing peer connection")
            await handle_shutdown(pc, None, ball_manager, signaling)

if __name__ == "__main__":
    asyncio.run(main())