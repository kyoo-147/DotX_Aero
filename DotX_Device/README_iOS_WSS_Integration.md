# ESP32 MQTT WebSocket Secure (WSS) for iOS Integration

## 🎯 **MỤC TIÊU**
Đảm bảo ESP32 kết nối MQTT qua WSS (WebSocket Secure) để tương thích với iOS App Transport Security (ATS).

## 📱 **iOS APP TRANSPORT SECURITY (ATS)**

### Yêu cầu của iOS:
- **Chặn HTTP:** iOS chặn tất cả kết nối HTTP không mã hóa
- **Bắt buộc HTTPS/WSS:** Chỉ cho phép kết nối bảo mật
- **Certificate Validation:** Yêu cầu chứng chỉ SSL/TLS hợp lệ

## 🔧 **CẤU HÌNH ESP32**

### 1. **MQTT Configuration (`sdkconfig`)**
```
CONFIG_BROKER_URI="wss://broker.emqx.io:8084/mqtt"
CONFIG_MQTT_TRANSPORT_SSL=y
CONFIG_MQTT_TRANSPORT_WEBSOCKET=y
CONFIG_MQTT_TRANSPORT_WEBSOCKET_SECURE=y
CONFIG_MBEDTLS_CERTIFICATE_BUNDLE=y
CONFIG_MBEDTLS_CERTIFICATE_BUNDLE_DEFAULT_FULL=y
```

### 2. **Certificate Integration**
- **File:** `main/certs/isrgrootx1.pem` (ISRG Root X1 Certificate)
- **Embedded:** Via `CMakeLists.txt` EMBED_TXTFILES
- **Purpose:** Xác thực chứng chỉ Let's Encrypt của broker

### 3. **Code Implementation**
```c
// Embedded certificate reference
extern const uint8_t isrgrootx1_pem_start[] asm("_binary_isrgrootx1_pem_start");
extern const uint8_t isrgrootx1_pem_end[]   asm("_binary_isrgrootx1_pem_end");

// MQTT SSL Configuration
const esp_mqtt_client_config_t mqtt_cfg = {
    .broker.address.uri = CONFIG_BROKER_URI,
    .broker.verification.certificate = (const char *)isrgrootx1_pem_start,
    .broker.verification.skip_cert_common_name_check = false,
};
```

## 📱 **iOS MQTT APP CONFIGURATION**

### Connection Settings:
```
Protocol: WebSocket Secure (WSS)
Host: broker.emqx.io
Port: 8084
Path: /mqtt
TLS/SSL: Enabled
Full URL: wss://broker.emqx.io:8084/mqtt
```

### Topics for Control:
| Topic | Description | Commands |
|-------|-------------|----------|
| `/topic/qos0` | Light 1 Control | "ON", "OFF" |
| `/topic/qos1` | Light 2 Control | "ON", "OFF" |
| `/topic/qos2` | Light 3 Control | "ON", "OFF" |
| `/topic/qos3` | Light 4 Control | "ON", "OFF" |

### Response Messages:
| Action | Response |
|--------|----------|
| Light 1 ON | `light1_turn_on` |
| Light 1 OFF | `light1_turn_off` |
| Light 2 ON | `light2_turn_on` |
| Light 2 OFF | `light2_turn_off` |
| Light 3 ON | `light3_turn_on` |
| Light 3 OFF | `light3_turn_off` |
| Light 4 ON | `light4_turn_on` |
| Light 4 OFF | `light4_turn_off` |

## 🔌 **HARDWARE MAPPING**
```
GPIO 22 -> LED/Relay 1 (Light 1)
GPIO 23 -> LED/Relay 2 (Light 2)  
GPIO 18 -> LED/Relay 3 (Light 3)
GPIO 19 -> LED/Relay 4 (Light 4)
```

## 🛠️ **BUILD & DEPLOY**

### Build Commands:
```bash
# Clean previous build
rm -rf build

# Build project
idf.py build

# Flash and monitor
idf.py flash monitor
```

### Expected Output (Success):
```
I (xxxx) MQTTWS_EXAMPLE: Connecting to MQTT broker: wss://broker.emqx.io:8084/mqtt
I (xxxx) MQTTWS_EXAMPLE: Using embedded certificate for SSL verification
I (xxxx) MQTTWS_EXAMPLE: MQTT_EVENT_CONNECTED
I (xxxx) MQTTWS_EXAMPLE: sent subscribe successful, msg_id=xxxx
```

## 🧪 **TESTING TRÊN iOS**

### 1. **Download MQTT Client App:**
- **MQTT Panel** - IoT client app
- **MQTTool**  
- **MyMQTT**

### 2. **Connection Test:**
```
1. Mở app MQTT trên iOS
2. Tạo connection mới:
   - Host: broker.emqx.io
   - Port: 8084
   - Protocol: WSS
   - Path: /mqtt
3. Connect
4. Subscribe to topics: /topic/qos0, /topic/qos1, /topic/qos2, /topic/qos3
5. Publish "ON"/"OFF" để test
```

### 3. **Verification:**
- ✅ iOS app kết nối thành công
- ✅ ESP32 nhận được commands
- ✅ LEDs/Relays hoạt động đúng
- ✅ Response messages được gửi về

## 🔍 **TROUBLESHOOTING**

### Lỗi thường gặp:

#### 1. **`No server verification option set`**
```
Nguyên nhân: Thiếu cấu hình SSL certificate
Giải pháp: Đảm bảo certificate được embed và config đúng
```

#### 2. **`ESP_ERR_MBEDTLS_SSL_SETUP_FAILED`**
```
Nguyên nhân: SSL handshake failed
Giải pháp: Kiểm tra certificate và broker URL
```

#### 3. **iOS không kết nối được**
```
Nguyên nhân: ATS chặn HTTP connection  
Giải pháp: Phải dùng WSS (wss://), không dùng WS (ws://)
```

### Debug Commands:
```bash
# Check certificate content
cat main/certs/isrgrootx1.pem

# Monitor SSL handshake
idf.py monitor | grep -i "ssl\|tls\|cert"

# Check MQTT events
idf.py monitor | grep -i "mqtt"
```

## 🎉 **KẾT QUẢ MONG ĐỢI**
- ✅ ESP32 kết nối WSS thành công  
- ✅ iOS app hoạt động không bị ATS chặn
- ✅ Điều khiển 4 LED/relay từ iOS
- ✅ Real-time response feedback
- ✅ Bảo mật SSL/TLS đầy đủ

## 📝 **GHI CHÚ QUAN TRỌNG**

1. **Certificate:** ISRG Root X1 là root CA của Let's Encrypt, tương thích với hầu hết brokers
2. **Security:** CN check được enable để tăng bảo mật
3. **Performance:** Embedded certificate tối ưu memory usage
4. **Compatibility:** WSS đảm bảo tương thích 100% với iOS ATS
