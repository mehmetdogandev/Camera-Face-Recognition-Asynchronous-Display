# OLED Screen Control System - Features & API Reference

This document provides comprehensive information about the OLED screen control features added to the ESP32-CAM camera project.

## 🎯 Features Overview

- **3-Column Display**: LEFT, RIGHT, BOTH counters
- **HTTP POST API**: Update screen via `/screen` endpoint
- **Real-time Updates**: Screen automatically refreshes on each POST request
- **Counter System**: Increment/decrement operations for each column
- **JSON Responses**: Structured data for easy integration
- **Non-blocking**: Camera and display work independently

## 📋 Requirements

### Arduino Libraries

You need to install the following libraries in Arduino IDE:

1. **Adafruit GFX Library**
   - Open Arduino IDE
   - Go to `Sketch -> Include Library -> Manage Libraries`
   - Search for "Adafruit GFX"
   - Click Install
   - Install all dependencies when prompted

2. **Adafruit SSD1306**
   - Same process: `Sketch -> Include Library -> Manage Libraries`
   - Search for "Adafruit SSD1306"
   - Click Install
   - Install all dependencies when prompted

3. **Wire**
   - Built-in with ESP32, no installation needed

### Python Requirements

```bash
pip install requests>=2.28.0
```

Or install from requirements.txt:
```bash
cd pythonscripts
pip install -r requirements.txt
```

## 🔌 Hardware Connection

Connect your OLED SSD1306 display to Deneyap Kart (ESP32-CAM):

```
OLED Pin    →    ESP32 Pin
────────────────────────────
VCC         →    3.3V
GND         →    GND
SDA         →    D10
SCL         →    D11
```

### Important Notes:

- **Voltage**: Most OLED modules work with 3.3V. Some require 5V - check your module's specifications
- **I2C Address**: Usually 0x3C, sometimes 0x3D
- **Cable Length**: Keep cables under 20cm for stable I2C communication

## ⚙️ Quick Installation

### 1. Install Libraries
Follow the requirements section above

### 2. Configure WiFi
Edit `KameraYuzTanima.ino`:
```cpp
const char* ssid = "Your_WiFi_Name";
const char* password = "Your_WiFi_Password";
```

### 3. Set Partition Scheme
- Arduino IDE: `Tools -> Partition Scheme -> Huge APP`
- **This is mandatory!** The project won't fit otherwise

### 4. Upload Code
- Select Board: `Tools -> Board -> Deneyap Kart 1A`
- Select Port: `Tools -> Port -> COMx`
- Click Upload button

### 5. Get IP Address
- Open Serial Monitor: `Tools -> Serial Monitor`
- Set baud rate to **115200**
- Note the IP address displayed:
  ```
  Wi-Fi agina baglanildi 
  OLED ekran başarıyla başlatıldı!
  Kamera hazir! Baglanmak icin 'http://192.168.1.100' adresini kullaniniz
  ```

## 🌐 API Reference

### HTTP Endpoint

```
POST http://<ESP32_IP>/screen
```

### Request Parameters

Send as form-data or URL-encoded:

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `data` | int | `0`, `1`, `2` | Column selector: 0=LEFT, 1=RIGHT, 2=BOTH |
| `status` | int | `0`, `1` | Operation: 0=INCREMENT, 1=DECREMENT |

### Response Format

**Success (200 OK):**
```json
{
  "status": "ok",
  "left": 10,
  "right": 5,
  "both": 3
}
```

**Error (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Invalid parameters"
}
```

### Column Selection Details

- `data=0` → **LEFT** column
  - Typically used for left-side person detection
  - Updates first counter on display
  
- `data=1` → **RIGHT** column
  - Typically used for right-side person detection
  - Updates second counter on display
  
- `data=2` → **BOTH** column
  - Used when both persons are detected together
  - Updates third counter on display

### Operation Details

- `status=0` → **INCREMENT** (+1)
  - Adds 1 to the selected counter
  - Use when detection occurs
  
- `status=1` → **DECREMENT** (-1)
  - Subtracts 1 from the selected counter
  - Use for correction or reset operations

**Note:** Counters can go negative. There are no upper or lower limits.

## 📡 Example Requests

### Using cURL (Windows PowerShell)

```powershell
# Increment LEFT counter
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=0&status=0"

# Increment RIGHT counter
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=1&status=0"

# Increment BOTH counter
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=2&status=0"

# Decrement LEFT counter
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=0&status=1"
```

### Using cURL (Linux/Mac)

```bash
# Increment LEFT counter
curl -X POST http://192.168.1.100/screen -d "data=0&status=0"

# Increment RIGHT counter
curl -X POST http://192.168.1.100/screen -d "data=1&status=0"

# Decrement BOTH counter
curl -X POST http://192.168.1.100/screen -d "data=2&status=1"
```

### Using Python

```python
import requests

ESP32_IP = "192.168.1.100"
url = f"http://{ESP32_IP}/screen"

# Increment left counter
response = requests.post(url, data={'data': 0, 'status': 0})
print(response.json())
# Output: {"status":"ok","left":1,"right":0,"both":0}

# Increment right counter
response = requests.post(url, data={'data': 1, 'status': 0})
print(response.json())
# Output: {"status":"ok","left":1,"right":1,"both":0}

# Decrement both counter
response = requests.post(url, data={'data': 2, 'status': 1})
print(response.json())
# Output: {"status":"ok","left":1,"right":1,"both":-1}
```

### Using JavaScript (Browser/Node.js)

```javascript
const ESP32_IP = "192.168.1.100";
const url = `http://${ESP32_IP}/screen`;

// Increment left counter
fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'data=0&status=0'
})
.then(response => response.json())
.then(data => console.log(data));
// Output: {status: "ok", left: 1, right: 0, both: 0}
```

## 🐍 Python Integration

### Simple Test Script

Run the basic test script:
```bash
cd pythonscripts
python test_screen.py
```

This script will:
1. Test LEFT column (increment twice)
2. Test RIGHT column (increment)
3. Test BOTH column (increment)
4. Test LEFT column (decrement)
5. Test RIGHT column (increment again)
6. Test BOTH column (decrement)

### Advanced Controller

Use the `ScreenController` class for production code:

```python
# Make sure to add pythonscripts to your path or run from that directory
import sys
sys.path.append('pythonscripts')
from advanced_screen_control import ScreenController

# Initialize controller with ESP32 IP
controller = ScreenController("192.168.1.100")

# Simple operations
controller.increment_left()   # LEFT +1
controller.increment_right()  # RIGHT +1
controller.increment_both()   # BOTH +1

controller.decrement_left()   # LEFT -1
controller.decrement_right()  # RIGHT -1
controller.decrement_both()   # BOTH -1

# Get current counter values
counters = controller.get_counters()
print(f"Left: {counters['left']}")
print(f"Right: {counters['right']}")
print(f"Both: {counters['both']}")

# Generic update (more flexible)
controller.update('left', increment=True)   # Same as increment_left()
controller.update('right', increment=False) # Same as decrement_right()
```

### Face Detection Integration Example

Here's a complete example integrating with OpenCV face detection:

```python
import cv2
import sys
sys.path.append('pythonscripts')
from advanced_screen_control import ScreenController

# Setup
ESP32_IP = "192.168.1.100"
controller = ScreenController(ESP32_IP)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Open video capture (0 = default camera)
cap = cv2.VideoCapture(0)

print("Starting face detection... Press 'q' to quit")

while True:
    # Capture frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Get frame dimensions
    height, width = frame.shape[:2]
    
    # Separate left and right regions
    left_faces = []
    right_faces = []
    
    for (x, y, w, h) in faces:
        # Calculate face center
        face_center_x = x + w // 2
        
        # Classify by region
        if face_center_x < width // 2:
            left_faces.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, 'LEFT', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        else:
            right_faces.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, 'RIGHT', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Update OLED display based on detections
    if len(left_faces) > 0 and len(right_faces) > 0:
        # Both sides have faces
        controller.increment_both()
        cv2.putText(frame, 'BOTH DETECTED', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif len(left_faces) > 0:
        # Only left side
        controller.increment_left()
        cv2.putText(frame, 'LEFT DETECTED', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    elif len(right_faces) > 0:
        # Only right side
        controller.increment_right()
        cv2.putText(frame, 'RIGHT DETECTED', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Draw center line
    cv2.line(frame, (width//2, 0), (width//2, height), (0, 255, 0), 2)
    
    # Display current counters
    counters = controller.get_counters()
    cv2.putText(frame, f"L:{counters['left']} R:{counters['right']} B:{counters['both']}", 
                (10, height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Show frame
    cv2.imshow('Face Detection + OLED Control', frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
```

### Interactive Control Mode

Run the advanced script for interactive testing:

```bash
cd pythonscripts
python advanced_screen_control.py
```

**Choose from 3 modes:**

1. **Simple Test** - Automated test sequence
   - Automatically tests all columns
   - Shows results after each operation
   
2. **Face Detection Simulation** - Random detection simulation
   - Simulates face detection for 30 seconds
   - Randomly triggers LEFT, RIGHT, BOTH, or NONE
   - Shows total counts at the end
   
3. **Manual Control** - Keyboard control interface
   - Commands:
     - `l+` - Increment LEFT
     - `l-` - Decrement LEFT
     - `r+` - Increment RIGHT
     - `r-` - Decrement RIGHT
     - `b+` - Increment BOTH
     - `b-` - Decrement BOTH
     - `q` - Quit

## 🎨 Display Layout

The OLED screen shows a clean 3-column layout:

```
┌────────────────────────────┐
│ LEFT   RIGHT   BOTH        │  ← Column headers (small font)
│ ───────────────────────    │  ← Separator line
│                            │
│  5      3       2          │  ← Counters (large font, 2x size)
│                            │
│                            │
└────────────────────────────┘
```

### Layout Details:

- **Screen Size**: 128x64 pixels (SSD1306)
- **Headers**: Row 1, font size 1x
- **Separator**: Horizontal line at y=10
- **Counters**: Starting at y=25, font size 2x
- **Spacing**: Evenly distributed across width

## 🔧 Troubleshooting

### OLED Display Not Starting

**Symptom**: Display is blank or shows "OLED ekran başlatılamadı" in Serial Monitor

**Solutions:**

1. **Check Wiring**
   ```
   VCC → 3.3V (some modules need 5V)
   GND → GND
   SDA → D10
   SCL → D11
   ```

2. **Check I2C Address**
   - Most common: 0x3C
   - Alternative: 0x3D
   - Scan for address (see Installation Guide)

3. **Test Module**
   - Try with another Arduino/ESP32
   - Verify module is not defective

### HTTP Request Not Responding

**Symptom**: Python script or cURL fails to connect

**Solutions:**

1. **Verify IP Address**
   ```bash
   ping 192.168.1.100
   ```
   - Check Serial Monitor for correct IP
   - Device must be on same network

2. **Check Firewall**
   - Temporarily disable firewall
   - Add exception for ESP32 IP

3. **ESP32 Status**
   - Restart ESP32
   - Check Serial Monitor for errors
   - Verify WiFi connection

### Compilation Error

**Symptom**: "Sketch too big" or other compile errors

**Solutions:**

1. **Partition Scheme** (MOST COMMON)
   - **Must** select: `Tools -> Partition Scheme -> Huge APP`
   - This is mandatory for this project

2. **Library Issues**
   - Update all Adafruit libraries
   - Reinstall ESP32 board package
   - Verify Wire library is available

3. **Memory Issues**
   - Disable face recognition if not needed
   - Reduce camera resolution in code

### Display Shows Garbage

**Symptom**: Random pixels or incorrect characters

**Solutions:**

1. **Cable Quality**
   - Use cables shorter than 20cm
   - Avoid running near power cables
   - Use shielded or twisted pair cables

2. **I2C Speed**
   ```cpp
   // In setup(), try reducing I2C speed:
   Wire.setClock(100000); // 100kHz instead of 400kHz
   ```

3. **Power Supply**
   - Use quality USB cable
   - Check voltage at VCC pin (should be stable 3.3V)
   - Add 100nF capacitor near VCC/GND if needed

### Slow Response

**Symptom**: Updates take longer than expected

**Normal latency:** 50-100ms

**If slower:**
- Check WiFi signal strength
- Move closer to router
- Check network congestion
- Try external antenna

## 📸 Camera Features Compatibility

This OLED addition **does not affect camera functions**:

- ✅ **Video Streaming** continues to work (`http://IP/stream`)
- ✅ **Snapshot Capture** available (`http://IP/capture`)
- ✅ **Face Detection** features preserved (if enabled)
- ✅ **Camera Settings** unchanged (`http://IP/control`)
- ✅ **Web Interface** fully functional

## 🎯 Performance Specifications

| Metric | Value | Notes |
|--------|-------|-------|
| **HTTP Response Time** | 50-100ms | Typical latency |
| **Display Update Time** | ~100ms | I2C communication |
| **Simultaneous Operation** | Yes | Camera + display work together |
| **Memory Usage** | ~1KB RAM | Minimal footprint |
| **Flash Usage** | ~50KB | Added code size |
| **I2C Speed** | 400kHz | Standard fast mode |
| **Max Request Rate** | ~10/sec | Practical limit |

## 📝 Important Notes

### I2C Communication
- Display uses I2C bus (SDA/SCL)
- No conflict with camera (uses different pins)
- All operations are non-blocking

### Counter Behavior
- Counters can go negative
- No upper or lower limits
- Persists until reset/power cycle
- Not saved to EEPROM (resets on reboot)

### Network Considerations
- Must be on 2.4GHz WiFi
- ESP32 doesn't support 5GHz
- No authentication (add if needed for production)
- JSON responses for easy parsing

### Thread Safety
- All operations are thread-safe
- Multiple simultaneous requests handled correctly
- Display updates are queued automatically

## 🤝 Getting Help

If you're still having issues:

1. **Check Serial Monitor** (115200 baud) for error messages
2. **Verify Hardware** connections match the wiring diagram
3. **Test Components** individually (camera first, then display)
4. **Review Logs** for HTTP request/response details
5. **Create Issue** on GitHub with:
   - Serial Monitor output
   - Hardware setup details
   - Code modifications (if any)
   - Error messages

## 📄 License

This code is provided as an example and can be used freely under the MIT License.

---

**📚 See Also:**
- [Installation Guide](INSTALLATION.md) - Detailed setup instructions
- [Wiring Diagrams](WIRING.md) - Visual connection guides
- [Code Changes](CHANGES.md) - Technical implementation details
- [Main README](../README.md) - Project overview

---

*Last updated: November 2025*
