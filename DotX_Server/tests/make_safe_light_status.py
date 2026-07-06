import asyncio
from threading import Event

# Khởi tạo event để theo dõi phản hồi từ MQTT
response_event = Event()

# Hàm callback khi nhận được tin nhắn từ các topic đã đăng ký
def on_message(client, userdata, msg):
    global light_status
    text_data = msg.payload.decode("utf-8")
    
    # Cập nhật trạng thái đèn dựa trên topic và tin nhắn nhận được
    if msg.topic == "/topic/qos0":  # light1
        light_status["light1"] = text_data.lower() == "on"
        print(f"Received on topic {msg.topic}: {text_data}")
    elif msg.topic == "/topic/qos1":  # light2
        light_status["light2"] = text_data.lower() == "on"
        print(f"Received on topic {msg.topic}: {text_data}")
    
    # Đặt event khi nhận được phản hồi
    response_event.set()

# Hàm chờ nhận phản hồi sau khi gửi tin nhắn
async def wait_for_response():
    # Đảm bảo vòng lặp MQTT client sẽ xử lý tin nhắn đến
    mqtt_client.loop_start()
    # Chờ đến khi có phản hồi
    await asyncio.wait_for(response_event.wait(), timeout=5)  # Thêm thời gian chờ 5s
    # Dừng vòng lặp khi đã nhận được phản hồi
    mqtt_client.loop_stop()

# Cập nhật logic điều khiển đèn
async def control_light(light_id, action):
    # Gửi tin nhắn và chờ phản hồi cho light1
    if light_id == "light1":
        await send_mqtt_message("/topic/qos0", action.upper())
        await wait_for_response()  # Chờ phản hồi sau khi gửi tin nhắn
        if light_status["light1"] == (action == "on"):
            return f"{light_id} has been {action} successfully."
        else:
            return f"Failed to change {light_id} status."
    # Gửi tin nhắn và chờ phản hồi cho light2
    elif light_id == "light2":
        await send_mqtt_message("/topic/qos1", action.upper())
        await wait_for_response()  # Chờ phản hồi sau khi gửi tin nhắn
        if light_status["light2"] == (action == "on"):
            return f"{light_id} has been {action} successfully."
        else:
            return f"Failed to change {light_id} status."

# Hàm chính để xử lý lệnh của người dùng
async def generate_response(user_input):
    print(f"AI received: {user_input}")
    # Đảm bảo các từ khóa dễ nhận diện cho lệnh bật tắt đèn
    light_actions = {
        "light1": ["light one", "white light"],
        "light2": ["light two", "yellow light"],
        "light1andlight2": ["light one and light two", "white light and yellow light", "both", "lights", "both lights"]
    }
    action_keywords = {
        "turn on": "on",
        "turn off": "off"
    }
    
    # Lặp qua các hành động bật/tắt đèn
    for light_id, keywords in light_actions.items():
        for keyword in keywords:
            for action, api_action in action_keywords.items():
                if action in user_input.lower() and keyword in user_input.lower():
                    # Gọi hàm điều khiển đèn và nhận phản hồi
                    result = await control_light(light_id, api_action)
                    return result  # Trả về kết quả cho người dùng

    return "Sorry, I couldn't process your request."
