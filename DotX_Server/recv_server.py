import asyncio
import websockets
from ollama import chat  # Import module của Ollama LLM
from brain_tts import generate_response

async def handle_client(websocket):
    try:
        # Tiếp nhận tin nhắn từ client
        message_recv = await websocket.recv()
        print(f"Received message from client: {message_recv}")

        full_response = await generate_response(message_recv)
        print(f"AI Response: {full_response}")

        # Gửi phản hồi cho client
        await websocket.send(full_response)

        # Gửi tín hiệu ping cho client để kiểm tra kết nối
        await websocket.ping()

        await asyncio.sleep(4)  # Delay để tránh ping quá nhanh

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def start_server():
    server = await websockets.serve(handle_client, "0.0.0.0", 8765, ping_interval=20, ping_timeout=60)  # Lắng nghe trên tất cả các địa chỉ mạng (0.0.0.0)
    print("Server started at ws://0.0.0.0:8765")
    await server.wait_closed()

# Chạy server
asyncio.run(start_server())
