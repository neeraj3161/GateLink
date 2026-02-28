# GateLink

GateLink is a real-time IoT gate automation system built using ESP8266, FastAPI, and WebSockets.  
It enables remote gate control through HTTP triggers or voice commands (via Siri Shortcuts), with instant relay activation over a persistent WebSocket connection.

The project demonstrates integration between embedded hardware and a cloud-hosted backend service.

---

## Overview

GateLink establishes a persistent WebSocket connection between an ESP8266 device and a FastAPI server.  
When an API endpoint is triggered, the server pushes a real-time message to the connected device, which activates a relay to power the gate trigger.

This design avoids polling and ensures low-latency communication.

System flow:

Siri / API Call  
→ FastAPI Server  
→ WebSocket Push  
→ ESP8266  
→ Relay  
→ Gate Trigger  

---

## Architecture

The system consists of:

- ESP8266 (NodeMCU) microcontroller  
- 5V relay module  
- FastAPI backend  
- WebSocket communication layer  
- Cloud deployment (Render or similar)  

The ESP8266 maintains a persistent WebSocket connection to the backend.  
When the `/open-gate` endpoint is called, the server broadcasts an `OPEN` command to all connected clients.

The device then activates the relay for a predefined duration.

---

## Features

- Real-time WebSocket-based device control  
- Automatic WebSocket reconnection handling  
- Safe client disconnect handling on the server  
- HTTP-triggered gate activation  
- Deployable to cloud platforms  
- Voice integration through iOS Shortcuts  

---

## API Endpoints

### POST /open-gate

Triggers all connected ESP devices to activate the relay.

Response:

```json
{
  "status": "sent"
}
