import websockets

async def send_to_ai(text):
    uri = "ws://192.168.1.15:8765"  # Thay địa chỉ server WebSocket
    try:
        async with websockets.connect(uri) as websocket:
            # Gửi dữ liệu text tới server
            await websocket.send(text)
            print(f"Sent: {text}")
            
            # Nhận phản hồi từ server
            response = await websocket.recv()
            print(f"AI Response: {response}")
            return response
    
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Error sending data to AI: {e}")
        return None
