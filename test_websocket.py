import websockets
import asyncio

async def test_websocket():
    uri = "ws://localhost:8000/face/ws/video"
    async with websockets.connect(uri) as websocket:
        print("WebSocket подключён")
        await websocket.send("Test message")
        response = await websocket.recv()
        print(f"Ответ от сервера: {response}")

asyncio.run(test_websocket())