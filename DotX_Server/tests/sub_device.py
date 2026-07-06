# #import context  # Ensures paho is in PYTHONPATH

# import paho.mqtt.client as mqtt


# def on_connect(mqttc, obj, flags, reason_code, properties):
#     print("reason_code: "+str(reason_code))

# def on_message(mqttc, obj, msg):
#     print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

# def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
#     print("Subscribed: "+str(mid)+" "+str(reason_code_list))

# def on_log(mqttc, obj, level, string):
#     print(string)

# mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")
# mqttc.on_message = on_message
# mqttc.on_connect = on_connect
# mqttc.on_subscribe = on_subscribe
# # Uncomment to enable debug messages
# mqttc.on_log = on_log
# mqttc.connect("mqtt.eclipseprojects.io", 80, 60)
# mqttc.subscribe("/topic/qos0", 0)
# mqttc.subscribe("/topic/qos1", 0)
# # mqttc.publish("/topic/qos0", "this_is_sample_test", 0)

# mqttc.loop_forever()


import paho.mqtt.client as mqtt

# Hàm xử lý khi kết nối MQTT thành công
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Đăng ký lắng nghe 2 topic
    client.subscribe("/topic/qos0")
    client.subscribe("/topic/qos1")

# Hàm xử lý khi nhận dữ liệu từ MQTT
def on_message(client, userdata, msg):
    # Lấy nội dung text từ payload
    text_data = msg.payload.decode("utf-8")  # Giải mã payload thành chuỗi
    print(f"Received on topic {msg.topic}: {text_data}")

    # Xử lý logic tùy theo topic
    if msg.topic == "/topic/qos0":
        print(f"Data from qos0: {text_data}")
    elif msg.topic == "/topic/qos1":
        print(f"Data from qos1: {text_data}")

# Khởi tạo MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Kết nối tới MQTT Broker
client.connect("mqtt.eclipseprojects.io", 1883, 60)

# Chạy vòng lặp để lắng nghe dữ liệu từ MQTT
client.loop_forever()
