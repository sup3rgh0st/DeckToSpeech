import asyncio
import websockets
import sys

async def hello(arg):
    async with websockets.connect("ws://localhost:3030") as websocket:
        await websocket.send(arg)

asyncio.run(hello(sys.argv[1]))