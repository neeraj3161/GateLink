# GateLink

GateLink is a real-time IoT gate automation system built using ESP8266, FastAPI, and WebSockets. It enables remote gate control via HTTP requests or voice commands (such as Siri Shortcuts), with instant relay activation through a persistent WebSocket connection.

This project demonstrates full-stack IoT integration between embedded hardware and a cloud-hosted backend.

---

## Overview

GateLink maintains a persistent WebSocket connection between an ESP8266 device and a FastAPI backend server. When an API endpoint is triggered, the server sends a real-time command to the connected device, which activates a relay to power the gate trigger.

The system avoids polling and ensures low-latency communication.

System flow:

Siri / API Call  
→ FastAPI Server  
→ WebSocket Push  
→ ESP8266  
→ Relay  
→ Gate Trigger  

---

## Architecture

### Backend

- FastAPI
- Uvicorn
- WebSocket communication
- Hosted on Render (or similar cloud provider)

### Hardware

- ESP8266 (NodeMCU)
- 5V single-channel relay module
- 5V 2A power supply
- USB cable (5V line switched through relay)
- Gate USB trigger dongle

---

## Project Structure

```
GateLink/
│
├── main.py
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## API Endpoints

### POST /open-gate

Triggers all connected ESP devices to activate the relay.

Response:

```json
{
  "status": "sent"
}
```

---

### POST /gate-open-log

Receives log messages from connected devices.

Example request body:

```json
"Gate opened successfully"
```

---

## Backend Setup (Local Development)

### 1. Install Dependencies

```
pip install -r requirements.txt
```

### 2. Run Server

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

WebSocket endpoint (local):

```
ws://<your-local-ip>:8000/ws
```

---

## Deployment (Render)

1. Push the repository to GitHub.
2. Create a new Web Service on Render.
3. Configure:

Build Command:
```
pip install -r requirements.txt
```

Start Command:
```
uvicorn main:app --host 0.0.0.0 --port 10000
```

After deployment:

WebSocket endpoint:
```
wss://your-app-name.onrender.com/ws
```

When connecting from ESP8266, use SSL (`beginSSL`) and port 443.

---

## ESP8266 Firmware Setup

### Required Libraries

- ESP8266WiFi
- WebSocketsClient (by Markus Sattler)

### Board Selection

Arduino IDE →  
Board: NodeMCU 1.0 (ESP-12E Module)

### Relay Wiring

ESP D1  → Relay IN1  
ESP 5V  → Relay VCC  
ESP GND → Relay GND  

The relay switches only the 5V (red) wire of the USB cable powering the gate trigger.  
Ground remains directly connected.

---

## WebSocket Connection (ESP)

For local development:

```cpp
webSocket.begin("192.168.x.x", 8000, "/ws");
```

For production (Render):

```cpp
webSocket.beginSSL("your-app-name.onrender.com", 443, "/ws");
```

---

## Security Considerations

This project currently assumes a trusted environment. For production deployment, consider:

- API authentication tokens
- Device ID validation
- Rate limiting
- Logging and audit trails
- HTTPS-only communication
- IP filtering
- Replay protection

---

## Reliability Handling

The backend:

- Tracks connected clients
- Cleans up disconnected WebSockets
- Prevents server crashes from dead connections
- Handles reconnection gracefully

The ESP8266:

- Automatically reconnects to WiFi
- Automatically reconnects to WebSocket
- Activates relay for fixed duration
- Avoids polling-based communication

---

## Possible Improvements

- Telegram or email notifications
- Mobile dashboard interface
- OTA firmware updates
- MQTT integration
- Access control (multiple users)
- Gate open audit logs stored in database
- Encrypted device authentication

---

## Technical Highlights

- Asynchronous WebSocket handling with FastAPI
- Persistent real-time connection model
- Embedded system and cloud backend integration
- Low-latency push-based architecture
- Production-ready disconnect handling

---

## Author

Neeraj Tripathi  
Software Engineer
