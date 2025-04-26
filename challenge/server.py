import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from ballAnimation import BallVideoStreamTrack


async def handle_offer(request):
    offer_data = await request.json()
    offer = RTCSessionDescription(sdp=offer_data['sdp'], type=offer_data['type'])
    pc = RTCPeerConnection()
    
    @pc.on('datachannel')
    def on_datachannel(channel):
        print(f"Channel {channel.label} established")
        cnt = [0]
        
        async def send_periodic_messages():
            while True:
                try:
                    message = f"Hello from server! Count: {cnt[0]}, ball position: {ball_position()}"
                    print(f"Server sending: {message}")
                    channel.send(message)
                    cnt[0] += 1
                    await asyncio.sleep(2)
                except Exception as e:
                    print(f"Error sending message: {e}")
                    break

        @channel.on('message')
        def on_message(message):
            print(f"Client says: {message}")
            asyncio.create_task(send_periodic_messages())

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })

def ball_position():
    ball_position = BallVideoStreamTrack()
    ball_position.set_fps(new_fps=45)
    print(ball_position.get_ball_position())
    return ball_position.get_ball_position()


async def main():
    app = web.Application()
    app.router.add_post("/offer", handle_offer)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "localhost", 8080).start()
    print("Server is running at http://localhost:8080")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
