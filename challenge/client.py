import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
import aiohttp


class VideoClient:
    def __init__(self):
        self.pc = RTCPeerConnection()
        self.channel = self.pc.createDataChannel("chat")
        self.message_count = 0

    async def send_periodic_messages(self):
        while True:
            self.channel.send(f"Hello from client! Message {self.message_count}")
            self.message_count += 1
            await asyncio.sleep(2)  # Send every 2 seconds

    async def connect(self):
        @self.channel.on("open")
        def on_open():
            print("Channel opened!")
            # Start sending periodic messages
            asyncio.create_task(self.send_periodic_messages())

        @self.channel.on("message")
        def on_message(message):
            print(f"Server says: {message}")

    async def start(self):
        await self.connect()
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8080/offer",
                json={"sdp": self.pc.localDescription.sdp, "type": self.pc.localDescription.type}
            ) as response:
                answer_data = await response.json()
                answer = RTCSessionDescription(sdp=answer_data["sdp"], type=answer_data["type"])
                await self.pc.setRemoteDescription(answer)

async def main():
    client = VideoClient()
    await client.start()
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
