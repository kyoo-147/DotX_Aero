# ESP32 MQTT WebSocket - iOS ATS Compatible Configuration

## Overview
This project has been updated to support iOS App Transport Security (ATS) requirements.

## MQTT Broker Configuration

### Production (iOS Compatible):
- **Secure WebSocket:** `wss://broker.emqx.io:8084/mqtt`
- **Port:** 8084 (WSS)
- **TLS/SSL:** Enabled
- **iOS Compatibility:** ✅ Full ATS compliance

### Development/Testing (Non-iOS):
- **Plain WebSocket:** `ws://broker.emqx.io:8083/mqtt`  
- **Port:** 8083 (WS)
- **TLS/SSL:** Disabled
- **iOS Compatibility:** ❌ Blocked by ATS

## How to Switch Configuration

### Method 1: Using menuconfig
```bash
idf.py menuconfig
# Navigate to: Example Configuration -> Broker URL
# Change between ws:// and wss:// URLs
```

### Method 2: Direct sdkconfig edit
```bash
# For iOS compatibility (WSS):
CONFIG_BROKER_URI="wss://broker.emqx.io:8084/mqtt"

# For development only (WS):
CONFIG_BROKER_URI="ws://broker.emqx.io:8083/mqtt"
```

## iOS MQTT App Configuration

When using iOS MQTT apps like "MQTT Panel", use these settings:

### Connection Settings:
- **Protocol:** WebSocket Secure (WSS)
- **Host:** `broker.emqx.io`
- **Port:** `8084`
- **Path:** `/mqtt`
- **TLS/SSL:** Enabled
- **Full URL:** `wss://broker.emqx.io:8084/mqtt`

### Topics for Device Control:
- **Light 1:** `/topic/qos0` (Send "ON" or "OFF")
- **Light 2:** `/topic/qos1` (Send "ON" or "OFF")  
- **Light 3:** `/topic/qos2` (Send "ON" or "OFF")
- **Light 4:** `/topic/qos3` (Send "ON" or "OFF")

### Expected Responses:
- Light 1 ON: `light1_turn_on`
- Light 1 OFF: `light1_turn_off`
- Light 2 ON: `light2_turn_on`
- Light 2 OFF: `light2_turn_off`
- Light 3 ON: `light3_turn_on`
- Light 3 OFF: `light3_turn_off`
- Light 4 ON: `light4_turn_on`
- Light 4 OFF: `light4_turn_off`

## Hardware Connections
- **LED/Relay 1:** GPIO 22
- **LED/Relay 2:** GPIO 23
- **LED/Relay 3:** GPIO 18
- **LED/Relay 4:** GPIO 19

## Build and Flash
```bash
# Clean previous build
idf.py clean

# Build with new configuration
idf.py build

# Flash to ESP32
idf.py flash monitor
```

## Troubleshooting

### If iOS still can't connect:
1. Verify iOS app supports WSS protocol
2. Check if broker `broker.emqx.io:8084` is accessible
3. Try alternative public WSS brokers:
   - `wss://test.mosquitto.org:8081/mqtt`
   - `wss://mqtt.eclipseprojects.io:443/mqtt`

### If ESP32 can't connect to WSS:
1. Check certificate bundle is enabled in sdkconfig
2. Verify MQTT_TRANSPORT_WEBSOCKET_SECURE=y
3. Monitor logs for TLS handshake errors

### For development without iOS:
Use the WS configuration: `ws://broker.emqx.io:8083/mqtt`
