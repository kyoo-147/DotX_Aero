import asyncio
import websockets
from ollama import chat

# Hàm xử lý yêu cầu từ client và gửi phản hồi LLM
async def handle_client(websocket, path):
    try:
        # Gửi tín hiệu ping đến client để duy trì kết nối
        while True:
            # Nhận tin nhắn từ client
            message = await websocket.recv()
            print(f"Received message: {message}")
            
            # Gọi mô hình AI (LLM) để xử lý yêu cầu của client
            stream = chat(
                model='llama3.2',
                messages=[{'role': 'user', 'content': message}],
                stream=True,
            )
            
            # Tạo phản hồi từ LLM và gửi lại cho client
            full_response = ""
            for chunk in stream:
                full_response += chunk['message']['content']
            
            # Gửi phản hồi lại client
            await websocket.send(full_response)

            # Gửi tín hiệu ping cho client để kiểm tra kết nối
            await websocket.ping()

            await asyncio.sleep(5)  # Delay để tránh ping quá nhanh

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Tạo server WebSocket
async def start_server():
    server = await websockets.serve(handle_client, '0.0.0.0', 8765, ping_interval=10, ping_timeout=5)
    print("Server started at ws://0.0.0.0:8765")
    await server.wait_closed()

# Chạy server
if __name__ == "__main__":
    asyncio.run(start_server())