import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from ballAnimation import BallVideoStreamTrack

class VideoServer:
    def __init__(self):
        self.pcs = set()
        self.ball_track = BallVideoStreamTrack()
        # Start ball animation
        asyncio.create_task(self.animate_ball())

    async def animate_ball(self):
        while True:
            await self.ball_track.recv()  # This updates the ball position
            await asyncio.sleep(1/30)  # 30 FPS

    async def handle_offer(self, request):
        offer_data = await request.json()
        offer = RTCSessionDescription(sdp=offer_data['sdp'], type=offer_data['type'])
        pc = RTCPeerConnection()
        self.pcs.add(pc)
        
        @pc.on('datachannel')
        def on_datachannel(channel):
            cnt = [0]
            
            async def send_periodic_messages():
                while True:
                    try:
                        ball_pos = self.ball_track.get_ball_position()
                        message = f"Hello from server! Count: {cnt[0]}, ball position: ({ball_pos[0]}, {ball_pos[1]})"
                        channel.send(message)
                        print(message)
                        cnt[0] += 1
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"Error sending message: {e}")
                        break

            @channel.on('message')
            def on_message(message):
                print(f"Client says: {message}")
                if cnt[0] == 0:
                    asyncio.create_task(send_periodic_messages())

        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        return web.json_response({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })

async def main():
    server = VideoServer()
    app = web.Application()
    app.router.add_post("/offer", server.handle_offer)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "localhost", 8080).start()
    print("Server is running at http://localhost:8080")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
