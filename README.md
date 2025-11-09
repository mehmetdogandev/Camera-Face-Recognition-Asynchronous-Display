# ESP32-CAM OLED Screen Control System

[![Platform](https://img.shields.io/badge/platform-ESP32-blue.svg)](https://www.espressif.com/en/products/socs/esp32)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Arduino](https://img.shields.io/badge/Arduino-Compatible-brightgreen.svg)](https://www.arduino.cc/)

A comprehensive ESP32-CAM project featuring real-time camera streaming with integrated OLED display control via HTTP API. Perfect for face detection applications, visitor counting, or any project requiring visual feedback with camera integration.

![ESP32-CAM with OLED Display](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Hardware Requirements](#-hardware-requirements)
- [Software Requirements](#-software-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Python Integration](#-python-integration)
- [Documentation](#-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Camera Capabilities
- 📸 **HD Video Streaming** - Real-time MJPEG stream over HTTP
- 🎯 **Face Detection** - Built-in face recognition support (optional)
- 📷 **Snapshot Capture** - Take still images on demand
- ⚙️ **Configurable Settings** - Adjust resolution, quality, and more

### OLED Display Control
- 🖥️ **3-Column Display** - Track LEFT, RIGHT, and BOTH counters
- 🔄 **Real-time Updates** - Instant display refresh via HTTP POST
- 📊 **Counter Management** - Increment/decrement any column
- 🎨 **Clean UI** - Professional layout with headers and large numbers

### Network & API
- 🌐 **RESTful API** - Simple HTTP POST interface
- 📱 **JSON Responses** - Structured data for easy integration
- ⚡ **Fast Response** - ~50-100ms latency
- 🔒 **Reliable** - Thread-safe operations

### Integration Ready
- 🐍 **Python Support** - Ready-to-use Python controllers
- 🔧 **Easy Integration** - Drop-in solution for face detection projects
- 📝 **Well Documented** - Comprehensive guides and examples
- 🎯 **Modular Design** - Camera and display work independently

---

## 🚀 Quick Start

### 1. Hardware Setup

Connect your SSD1306 OLED display to Deneyap Kart (ESP32-CAM):

```
OLED Pin    →    ESP32 Pin
────────────────────────────
VCC         →    3.3V
GND         →    GND
SDA         →    D10
SCL         →    D11
```

### 2. Software Installation

#### Install Arduino Libraries
Open Arduino IDE and install these libraries via Library Manager:
- **Adafruit GFX Library**
- **Adafruit SSD1306**

#### Configure WiFi
Edit `KameraYuzTanima.ino`:
```cpp
const char* ssid = "YourWiFiName";
const char* password = "YourWiFiPassword";
```

#### Upload Code
1. Set **Tools → Partition Scheme → Huge APP**
2. Select your Deneyap Kart board
3. Click **Upload**

### 3. Get IP Address

Open Serial Monitor (115200 baud) and note the IP address:
```
Wi-Fi agina baglanildi 
OLED ekran başarıyla başlatıldı!
Kamera hazir! Baglanmak icin 'http://192.168.1.100' adresini kullaniniz
```

### 4. Test It!

#### Via Browser
Visit `http://192.168.1.100` to see the camera stream

#### Via Python
```bash
cd pythonscripts
pip install -r requirements.txt
python test_screen.py
```

**🎉 You're all set!**

---

## 🔧 Hardware Requirements

| Component | Specification | Notes |
|-----------|--------------|-------|
| **Microcontroller** | Deneyap Kart 1A (ESP32-CAM) | Must have camera connector |
| **Display** | OLED SSD1306 128x64 | I2C interface (0x3C or 0x3D) |
| **Camera** | OV2640 or compatible | Included with Deneyap Kart |
| **Power** | 5V/1A USB or external | Via USB or VIN pin |
| **Cables** | Jumper wires | For OLED connection |

### Optional Components
- **Breadboard** - For prototyping
- **Case** - For permanent installation
- **External Antenna** - For better WiFi range

---

## 💻 Software Requirements

### Arduino IDE
- **Version**: 1.8.x or 2.x
- **ESP32 Board Package**: Latest version
- **Required Libraries**:
  - Adafruit GFX Library (≥ 1.11.0)
  - Adafruit SSD1306 (≥ 2.5.0)
  - Wire (built-in)

### Python (for testing/integration)
- **Version**: Python 3.7+
- **Dependencies**: `requests >= 2.28.0`

### Development Environment
- **OS**: Windows, macOS, or Linux
- **WiFi**: 2.4GHz network (ESP32 doesn't support 5GHz)

---

## 📥 Installation

### Step-by-Step Guide

#### 1. Clone or Download
```bash
git clone https://github.com/yourusername/KameraYuzTanima.git
cd KameraYuzTanima
```

#### 2. Arduino IDE Setup
1. **Install ESP32 Board Support**
   - Open Arduino IDE
   - Go to `File → Preferences`
   - Add to "Additional Board Manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to `Tools → Board → Board Manager`
   - Search "ESP32" and install

2. **Install Required Libraries**
   - `Sketch → Include Library → Manage Libraries`
   - Search and install:
     - "Adafruit GFX"
     - "Adafruit SSD1306"

#### 3. Hardware Connection
Follow the wiring diagram in [Hardware Setup Guide](docs/BAGLANTI_SEMASI.md)

#### 4. Configure and Upload
1. Open `KameraYuzTanima.ino`
2. Update WiFi credentials:
   ```cpp
   const char* ssid = "YourWiFiSSID";
   const char* password = "YourPassword";
   ```
3. Select board: `Tools → Board → Deneyap Kart 1A`
4. **Important**: Set `Tools → Partition Scheme → Huge APP`
5. Select port: `Tools → Port → COMx`
6. Click **Upload** (➡️)

#### 5. Python Setup (Optional)
```bash
pip install -r requirements.txt
```

**📚 For detailed installation guide, see [Installation Documentation](docs/KURULUM.md)**

---

## 🎮 Usage

### Camera Access

#### View Live Stream
Open your browser and navigate to:
```
http://[ESP32_IP]/stream
```

#### Capture Still Image
```
http://[ESP32_IP]/capture
```

#### Camera Settings
Access the web interface at:
```
http://[ESP32_IP]/
```

### OLED Display Control

#### HTTP API Endpoint
```
POST http://[ESP32_IP]/screen
```

#### Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `data` | `0` | LEFT column |
| `data` | `1` | RIGHT column |
| `data` | `2` | BOTH column |
| `status` | `0` | INCREMENT (+1) |
| `status` | `1` | DECREMENT (-1) |

#### Example Requests

**Using cURL (Windows PowerShell):**
```powershell
# Increment LEFT counter
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=0&status=0"

# Increment RIGHT counter
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=1&status=0"

# Decrement BOTH counter
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=2&status=1"
```

**Using Python:**
```python
import requests

ESP32_IP = "192.168.1.100"
url = f"http://{ESP32_IP}/screen"

# Increment left counter
response = requests.post(url, data={'data': 0, 'status': 0})
print(response.json())
# Output: {"status":"ok","left":1,"right":0,"both":0}
```

#### Response Format
```json
{
  "status": "ok",
  "left": 5,
  "right": 3,
  "both": 2
}
```

### Display Layout

The OLED screen shows a 3-column layout:

```
┌────────────────────────────┐
│ LEFT   RIGHT   BOTH        │  ← Headers (small font)
│ ───────────────────────    │  ← Separator line
│                            │
│  5      3       2          │  ← Counters (large font)
│                            │
│                            │
└────────────────────────────┘
```

---

## 📘 API Reference

### Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface with camera controls |
| `/stream` | GET | MJPEG video stream |
| `/capture` | GET | Capture single image (JPEG) |
| `/control` | GET | Camera settings API |
| `/status` | GET | Camera status information |
| `/screen` | POST | Update OLED display |

### Screen Control API

#### POST /screen

Update OLED display counters.

**Request Body (form-data):**
```
data: 0-2 (column selector)
status: 0-1 (operation)
```

**Success Response (200 OK):**
```json
{
  "status": "ok",
  "left": 10,
  "right": 5,
  "both": 3
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Invalid parameters"
}
```

#### Column Selection (data parameter)
- `0` - LEFT column
- `1` - RIGHT column
- `2` - BOTH column

#### Operation Selection (status parameter)
- `0` - INCREMENT (add 1)
- `1` - DECREMENT (subtract 1)

**Note:** Counters can go negative. There are no limits.

---

## 🐍 Python Integration

### Quick Test Script

Run the basic test:
```bash
cd pythonscripts
python test_screen.py
```

This will test all three columns sequentially.

### Advanced Controller

Use the `ScreenController` class for your projects:

```python
# Add pythonscripts to path or run from that directory
import sys
sys.path.append('pythonscripts')
from advanced_screen_control import ScreenController

# Initialize controller
controller = ScreenController("192.168.1.100")

# Simple operations
controller.increment_left()
controller.increment_right()
controller.increment_both()

controller.decrement_left()
controller.decrement_right()
controller.decrement_both()

# Get current values
counters = controller.get_counters()
print(f"Left: {counters['left']}, Right: {counters['right']}, Both: {counters['both']}")
```

### Face Detection Integration Example

```python
import cv2
from advanced_screen_control import ScreenController

# Setup
controller = ScreenController("192.168.1.100")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect faces
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    
    # Split frame into left/right regions
    width = frame.shape[1]
    left_faces = [f for f in faces if f[0] + f[2]/2 < width/2]
    right_faces = [f for f in faces if f[0] + f[2]/2 >= width/2]
    
    # Update counters based on detection
    if len(left_faces) > 0 and len(right_faces) > 0:
        controller.increment_both()
    elif len(left_faces) > 0:
        controller.increment_left()
    elif len(right_faces) > 0:
        controller.increment_right()
    
    # Display
    cv2.imshow('Face Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Interactive Control

Run the advanced script for interactive testing:
```bash
cd pythonscripts
python advanced_screen_control.py
```

Choose from:
1. **Simple Test** - Automated test sequence
2. **Face Detection Simulation** - Random detection simulation
3. **Manual Control** - Keyboard control interface

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

### Turkish Documentation (Türkçe Dökümanlar)

| Document | Description |
|----------|-------------|
| [📖 README_SCREEN.md](docs/README_SCREEN.md) | Complete feature guide and usage (Tam özellik rehberi) |
| [🔧 KURULUM.md](docs/KURULUM.md) | Step-by-step installation guide (Adım adım kurulum) |
| [🔌 BAGLANTI_SEMASI.md](docs/BAGLANTI_SEMASI.md) | Detailed wiring diagrams (Detaylı bağlantı şemaları) |
| [📝 DEGISIKLIKLER.md](docs/DEGISIKLIKLER.md) | Code changes and modifications (Kod değişiklikleri) |

### Quick Links

- **First time user?** → Start with [Installation Guide](docs/KURULUM.md)
- **Hardware setup?** → Check [Wiring Diagrams](docs/BAGLANTI_SEMASI.md)
- **API details?** → Read [Feature Guide](docs/README_SCREEN.md)
- **Troubleshooting?** → See sections below

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### ❌ OLED Display Not Working

**Problem:** Display shows nothing or "OLED ekran başlatılamadı" error

**Solutions:**
1. **Check wiring:**
   - VCC → 3.3V (or 5V if your module requires it)
   - GND → GND
   - SDA → D10
   - SCL → D11

2. **Check I2C address:**
   ```cpp
   // In KameraYuzTanima.ino, try:
   #define OLED_ADDR 0x3C  // Most common
   // or
   #define OLED_ADDR 0x3D  // Some modules
   ```

3. **Test I2C connection:**
   Add this to `setup()` to scan for devices:
   ```cpp
   Wire.begin(D10, D11);
   Serial.println("Scanning I2C...");
   for (byte i = 0; i < 127; i++) {
     Wire.beginTransmission(i);
     if (Wire.endTransmission() == 0) {
       Serial.printf("Found device at 0x%02X\n", i);
     }
   }
   ```

#### ❌ WiFi Connection Failed

**Problem:** ESP32 can't connect to WiFi

**Solutions:**
1. **Check credentials:**
   - SSID is case-sensitive
   - Password is correct
   - Special characters may cause issues

2. **Network requirements:**
   - Must be 2.4GHz network (ESP32 doesn't support 5GHz)
   - WPA/WPA2 security (WPA3 may not work)

3. **Signal strength:**
   - Move closer to router
   - Consider external antenna

#### ❌ Compilation Errors

**Problem:** "Sketch too big" or compilation fails

**Solutions:**
1. **Partition scheme:**
   - **Must** select `Tools → Partition Scheme → Huge APP`
   - This is the most common issue!

2. **Memory optimization:**
   - Disable face recognition if not needed
   - Reduce camera resolution in code

3. **Library conflicts:**
   - Update all libraries to latest versions
   - Reinstall ESP32 board package

#### ❌ HTTP POST Not Working

**Problem:** Python script or cURL fails to connect

**Solutions:**
1. **IP address:**
   - Verify IP from Serial Monitor
   - Ping the ESP32: `ping 192.168.1.100`

2. **Network:**
   - Computer and ESP32 must be on same network
   - Check firewall settings
   - Try disabling antivirus temporarily

3. **ESP32 status:**
   - Check Serial Monitor for errors
   - Restart ESP32 if needed

#### ❌ Camera Not Streaming

**Problem:** Video stream doesn't work

**Solutions:**
1. **Camera initialization:**
   - Check Serial Monitor for camera errors
   - Try power cycling the device

2. **Browser compatibility:**
   - Use Chrome, Firefox, or Edge
   - Some browsers don't support MJPEG streams

3. **Resolution:**
   - Try lower resolution in camera settings
   - PSRAM must be enabled

### Performance Issues

#### Slow Response
- **Normal latency:** 50-100ms
- **If slower:** Check WiFi signal strength
- **If much slower:** Restart ESP32

#### Display Flickering
- **Cause:** Weak power supply
- **Solution:** Use quality USB cable and power source
- **Check:** Voltage at VCC should be stable

### Getting Help

If you're still stuck:

1. **Check Serial Monitor** at 115200 baud for error messages
2. **Verify hardware** connections twice
3. **Test components** individually (camera, then display)
4. **Review documentation** in `docs/` folder
5. **Create an issue** on GitHub with:
   - Serial Monitor output
   - Your hardware setup
   - Code modifications (if any)

---

## 🎯 Project Structure

```
KameraYuzTanima/
│
├── KameraYuzTanima.ino         # Main Arduino sketch
├── app_httpd.cpp               # Web server and API handlers
├── camera_index.h              # Web interface HTML (gzipped)
├── .gitignore                  # Git ignore rules
│
├── README.md                   # Main project documentation (English)
│
├── docs/                       # Complete documentation
│   ├── README.md               # Documentation index
│   ├── SCREEN_FEATURES.md      # Feature guide & API reference
│   ├── INSTALLATION.md         # Installation guide
│   ├── WIRING.md               # Wiring diagrams & hardware
│   └── CHANGES.md              # Technical changes & code docs
│
└── pythonscripts/              # Python integration scripts
    ├── test_screen.py          # Basic test script
    ├── advanced_screen_control.py  # Advanced controller
    └── requirements.txt        # Python dependencies
```

---

## ⚡ Performance Specifications

| Metric | Value |
|--------|-------|
| **HTTP Response Time** | 50-100ms |
| **Display Update Time** | ~100ms |
| **Camera FPS** | Up to 20 FPS (QVGA) |
| **WiFi Range** | ~50m (indoor) |
| **Power Consumption** | ~500mA @ 5V |
| **Memory Usage** | ~1KB RAM for display |
| **Flash Usage** | ~2.8MB (requires Huge APP) |

---

## 🔐 Security Considerations

⚠️ **Important:** This project has no built-in authentication!

For production use, consider:
- Adding password protection to web interface
- Using HTTPS instead of HTTP
- Implementing API keys for POST requests
- Restricting access by IP address
- Using a VPN for remote access

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Areas for Contribution
- Additional language support
- Web interface improvements
- New API features
- Bug fixes
- Documentation improvements
- Example projects

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Espressif** - For ESP32 platform
- **Adafruit** - For excellent display libraries
- **Arduino** - For the development environment
- **Deneyap** - For Turkish maker community support

---

## 📞 Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/mehmetdogandev/KameraYuzTanima/issues)
- **Documentation:** Check the `docs/` folder for detailed guides
- **Community:** Join discussions in Issues section

---

## 👨‍💻 Developer

<div align="center">
  <img src="https://avatars.githubusercontent.com/u/115467130?v=4" alt="Mehmet Doğan" width="100" height="100" style="border-radius: 50%;" />
  
  **Mehmet Doğan**
  
  [![GitHub](https://img.shields.io/badge/GitHub-mehmetdogandev-181717?style=flat&logo=github)](https://github.com/mehmetdogandev)
  [![Email](https://img.shields.io/badge/Email-mehmetdogan.dev@gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:mehmetdogan.dev@gmail.com)
</div>

---

## 🌟 Star History

If this project helped you, please consider giving it a ⭐ on GitHub!

---

**Made with ❤️ for makers and developers**

*Last updated: November 2025*
