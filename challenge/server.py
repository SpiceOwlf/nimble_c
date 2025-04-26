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
        cnt = [0]
        
        async def send_periodic_messages():
            while True:
                print("111111", ball_position())
                channel.send(f"This is from server:Server message { cnt[0], ball_position()}")
                cnt[0] += 1
                await asyncio.sleep(2)  # Send every 2 seconds
        
        @channel.on('message')
        async def on_message(message):
            print(f"Client says: {message}")

        @channel.on("open")
        def on_open():
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
