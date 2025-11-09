# Installation Guide - Step by Step

Complete installation guide for the ESP32-CAM OLED Screen Control System.

## 📋 Table of Contents

1. [Prerequisites](#-prerequisites)
2. [Arduino IDE Setup](#-arduino-ide-setup)
3. [Library Installation](#-library-installation)
4. [Hardware Connection](#-hardware-connection)
5. [Code Configuration](#-code-configuration)
6. [Upload Process](#-upload-process)
7. [Verification](#-verification)
8. [Python Setup](#-python-setup)
9. [Troubleshooting](#-troubleshooting)

---

## ✅ Prerequisites

Before you begin, make sure you have:

### Hardware
- ✅ Deneyap Kart 1A (ESP32-CAM) with camera connector
- ✅ OLED SSD1306 display (128x64, I2C)
- ✅ USB cable (data capable, not charge-only)
- ✅ Jumper wires (4 pieces minimum)
- ✅ Computer with USB port

### Software
- ✅ Arduino IDE (version 1.8.x or 2.x)
- ✅ ESP32 board package installed
- ✅ Python 3.7+ (optional, for testing)

### Network
- ✅ 2.4GHz WiFi network (ESP32 doesn't support 5GHz)
- ✅ WiFi credentials (SSID and password)

---

## 🔧 Arduino IDE Setup

### Step 1: Install Arduino IDE

If you don't have Arduino IDE installed:

1. Download from [arduino.cc/en/software](https://www.arduino.cc/en/software)
2. Install following the wizard
3. Launch Arduino IDE

### Step 2: Add ESP32 Board Support

1. Open Arduino IDE
2. Go to `File → Preferences`
3. Find "Additional Board Manager URLs" field
4. Add this URL:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
5. If there are already URLs, separate with comma or click the button next to the field
6. Click **OK**

7. Go to `Tools → Board → Board Manager...`
8. Search for "**ESP32**"
9. Find "**esp32 by Espressif Systems**"
10. Click **Install** (may take several minutes)
11. Wait for installation to complete
12. Close Board Manager

### Step 3: Select Your Board

1. Go to `Tools → Board`
2. Navigate to **ESP32 Arduino**
3. Select **Deneyap Kart 1A** (or Deneyap Kart 1A v2 if you have v2)

### Step 4: Configure Board Settings

**CRITICAL**: These settings are mandatory!

1. `Tools → Partition Scheme → Huge APP (3MB No OTA/1MB SPIFFS)`
   - ⚠️ **This is the most important setting!**
   - Without this, code won't fit and compilation will fail

2. `Tools → Upload Speed → 921600`
   - If upload fails, try 115200

3. `Tools → CPU Frequency → 240MHz (WiFi/BT)`

4. `Tools → Flash Frequency → 80MHz`

5. `Tools → Flash Mode → QIO`

6. `Tools → Port → COMx` (Windows) or `/dev/ttyUSBx` (Linux/Mac)
   - Select the port your board is connected to

---

## 📚 Library Installation

### Method 1: Using Library Manager (Recommended)

#### Install Adafruit GFX Library

1. Open `Sketch → Include Library → Manage Libraries...`
2. In the search box, type: **Adafruit GFX**
3. Find "**Adafruit GFX Library by Adafruit**"
4. Click **Install**
5. When prompted to install dependencies, click **Install All**
6. Wait for installation to complete

#### Install Adafruit SSD1306 Library

1. In the same Library Manager window
2. Search for: **Adafruit SSD1306**
3. Find "**Adafruit SSD1306 by Adafruit**"
4. Click **Install**
5. When prompted to install dependencies, click **Install All**
6. Wait for installation to complete

#### Verify Wire Library

- **Wire** library is built-in with ESP32
- No installation needed
- Automatically included with ESP32 board package

### Method 2: Manual Installation (Alternative)

If Library Manager doesn't work:

1. Download libraries from GitHub:
   - [Adafruit GFX](https://github.com/adafruit/Adafruit-GFX-Library)
   - [Adafruit SSD1306](https://github.com/adafruit/Adafruit_SSD1306)

2. Extract ZIP files

3. Copy folders to Arduino libraries directory:
   - **Windows**: `Documents\Arduino\libraries\`
   - **Mac**: `~/Documents/Arduino/libraries/`
   - **Linux**: `~/Arduino/libraries/`

4. Restart Arduino IDE

### Verification

To verify libraries are installed:
1. Go to `Sketch → Include Library`
2. You should see:
   - Adafruit GFX Library
   - Adafruit SSD1306

---

## 🔌 Hardware Connection

### OLED Display Wiring

Connect your OLED SSD1306 display to Deneyap Kart:

```
╔════════════════════════════════════════════╗
║  OLED Pin    →    Deneyap Kart Pin        ║
╠════════════════════════════════════════════╣
║  VCC         →    3.3V                    ║
║  GND         →    GND                     ║
║  SDA         →    D10                     ║
║  SCL         →    D11                     ║
╚════════════════════════════════════════════╝
```

### Visual Guide

```
     OLED Display                    ESP32-CAM
    ┌─────────────┐                ┌──────────┐
    │             │                │          │
    │   128x64    │                │  Camera  │
    │    OLED     │                │  Module  │
    │             │                │          │
    └─────┬───────┘                └────┬─────┘
          │                             │
    ┌─────┴──────┐               ┌─────┴──────┐
    │ VCC GND    │               │            │
    │ SDA SCL    │               │  3.3V GND  │
    └──┬───┬─────┘               │  D10  D11  │
       │   │                     └──┬────┬────┘
       │   │                        │    │
       │   └────────────────────────┘    │
       └─────────────────────────────────┘
```

### Important Connection Notes

⚠️ **Voltage Selection**
- Most OLED modules work with **3.3V**
- Some modules require **5V** - check your module label!
- Wrong voltage can damage the display

⚠️ **Pin Assignment**
- SDA (Data) → D10
- SCL (Clock) → D11
- Do NOT swap these pins!

⚠️ **Cable Quality**
- Use cables shorter than 20cm
- Longer cables may cause I2C communication issues
- Avoid running near power cables

⚠️ **Secure Connections**
- Make sure all connections are firm
- Loose connections cause intermittent failures
- Use breadboard or soldered connections for permanent setup

---

## ⚙️ Code Configuration

### Step 1: Open the Project

1. Download or clone the project
2. Open `KameraYuzTanima.ino` in Arduino IDE

### Step 2: Configure WiFi

Find these lines near the top of the file:

```cpp
const char* ssid = "Memet";          // Change this
const char* password = "aaaa11112";   // Change this
```

Replace with your WiFi credentials:

```cpp
const char* ssid = "Your_WiFi_Name";       // Your network name
const char* password = "Your_WiFi_Password";  // Your network password
```

**Notes:**
- SSID is case-sensitive: "MyWiFi" ≠ "mywifi"
- Password must be exact
- Avoid special characters if possible (especially quotes)
- Must be 2.4GHz network

### Step 3: Check I2C Address (Optional)

Default I2C address is 0x3C:

```cpp
#define OLED_ADDR 0x3C
```

If your display doesn't work, try 0x3D:

```cpp
#define OLED_ADDR 0x3D
```

### Step 4: Verify Pin Assignments (Optional)

Default pins are D10 and D11:

```cpp
Wire.begin(D10, D11);  // SDA, SCL
```

If you need to use different pins:

```cpp
Wire.begin(D8, D9);   // Example: Different pins
```

**Warning:** Don't use pins that conflict with camera!

---

## 📤 Upload Process

### Step 1: Connect Board

1. Connect Deneyap Kart to computer via USB cable
2. Wait for drivers to install (first time only)
3. Check Device Manager (Windows) or `ls /dev/tty*` (Linux/Mac) to see port

### Step 2: Verify Code

1. Click the **Verify** button (✓) or press `Ctrl+R`
2. Wait for compilation to complete
3. Check for errors in the output window

**Common compilation errors:**
- "Sketch too big" → Change Partition Scheme to Huge APP
- Library not found → Install missing libraries
- Syntax error → Check your WiFi credentials for special characters

### Step 3: Upload

1. Click the **Upload** button (→) or press `Ctrl+U`
2. Wait for "Connecting..." message
3. Upload will take 2-3 minutes
4. Watch for "Done uploading" message

**If upload fails:**
- Press and hold BOOT button on Deneyap Kart while uploading
- Try different USB cable
- Try different USB port
- Reduce upload speed to 115200

### Step 4: Monitor Progress

Watch the output window for:
```
Sketch uses XXXXX bytes (XX%) of program storage space.
Writing at 0x00010000... (100%)
Wrote XXXXX bytes (XXXXX compressed) at 0x00010000 in X.X seconds
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```

---

## ✅ Verification

### Step 1: Open Serial Monitor

1. Click `Tools → Serial Monitor` or press `Ctrl+Shift+M`
2. Set baud rate to **115200** (bottom right)
3. Board will automatically reset and start

### Step 2: Check Output

You should see something like:

```
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0x1 (POWERON),boot:0x8 (SPI_FAST_FLASH_BOOT)
...
Wi-Fi agina baglaniliyor...
..........
Wi-Fi agina baglanildi 
SSD1306 OLED başarıyla başlatıldı!
Kamera hazir! Baglanmak icin 'http://192.168.1.100' adresini kullaniniz
```

### Step 3: Note IP Address

📝 **Write down the IP address!** Example: `192.168.1.100`

You'll need this for:
- Accessing camera web interface
- Sending OLED update requests
- Python scripts

### Step 4: Test OLED Display

The OLED should show:

```
┌────────────────────────────┐
│ LEFT   RIGHT   BOTH        │
│ ───────────────────────    │
│                            │
│  0      0       0          │
│                            │
└────────────────────────────┘
```

If display is blank, see Troubleshooting section.

### Step 5: Test Web Interface

1. Open web browser
2. Navigate to: `http://192.168.1.100` (use your IP)
3. You should see camera interface
4. Try viewing video stream

### Step 6: Test OLED API

**Using PowerShell (Windows):**
```powershell
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=0&status=0"
```

**Using curl (Linux/Mac):**
```bash
curl -X POST http://192.168.1.100/screen -d "data=0&status=0"
```

You should see:
- JSON response in terminal
- LEFT counter on OLED increments to 1

---

## 🐍 Python Setup (Optional)

If you want to use Python scripts for testing:

### Step 1: Install Python

1. Download Python 3.7+ from [python.org](https://www.python.org/)
2. During installation, check **"Add Python to PATH"**
3. Complete installation

### Step 2: Install Requirements

Navigate to pythonscripts directory and install:

```bash
cd pythonscripts
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests
```

### Step 3: Update IP Address

Edit `pythonscripts/test_screen.py` and `pythonscripts/advanced_screen_control.py`:

```python
ESP32_IP = "192.168.1.100"  # Change to your IP
```

### Step 4: Run Test Script

```bash
cd pythonscripts
python test_screen.py
```

You should see output like:
```
OLED Ekran Test Scripti
==================================================

1. Sol sütunu arttır (data=0, status=0)
✓ Başarılı: Sol=1, Sağ=0, İkisi=0
...
```

---

## 🔧 Troubleshooting

### ❌ OLED Display Not Working

**Symptom:** Display is blank or shows "OLED ekran başlatılamadı"

**Solutions:**

1. **Check Wiring**
   ```
   VCC → 3.3V (not 5V, unless your module requires it)
   GND → GND
   SDA → D10
   SCL → D11
   ```

2. **Scan I2C Bus**
   
   Add this code to `setup()` temporarily:
   ```cpp
   Wire.begin(D10, D11);
   Serial.println("Scanning I2C bus...");
   
   for (byte i = 8; i < 120; i++) {
     Wire.beginTransmission(i);
     byte error = Wire.endTransmission();
     
     if (error == 0) {
       Serial.printf("I2C device found at address 0x%02X\n", i);
     }
   }
   Serial.println("Scan complete");
   ```
   
   Upload and check Serial Monitor. If you see an address like 0x3C or 0x3D, update:
   ```cpp
   #define OLED_ADDR 0x3C  // or 0x3D
   ```

3. **Test Display**
   - Try with another Arduino/ESP32
   - Verify display is not defective

### ❌ WiFi Won't Connect

**Symptom:** Stuck at "Wi-Fi agina baglaniliyor..."

**Solutions:**

1. **Check Credentials**
   - SSID is correct and case-sensitive
   - Password is correct
   - No extra spaces in code

2. **Check Network**
   - Must be 2.4GHz (not 5GHz)
   - WPA/WPA2 security (WPA3 may not work)
   - Router is working and in range

3. **Test Code**
   ```cpp
   WiFi.begin(ssid, password);
   int attempts = 0;
   while (WiFi.status() != WL_CONNECTED && attempts < 20) {
     delay(500);
     Serial.print(".");
     attempts++;
   }
   
   if (WiFi.status() != WL_CONNECTED) {
     Serial.println("\nFailed to connect to WiFi");
     Serial.printf("SSID: %s\n", ssid);
   }
   ```

### ❌ Sketch Too Big Error

**Symptom:** "Sketch too big; see http://www.arduino.cc/en/Guide/Troubleshooting#size"

**Solution:**
- **Must** set: `Tools → Partition Scheme → Huge APP (3MB No OTA/1MB SPIFFS)`
- This is the #1 most common issue!

### ❌ Upload Failed

**Symptom:** "A fatal error occurred: Failed to connect to ESP32"

**Solutions:**

1. **Press BOOT Button**
   - Hold BOOT button on board
   - Click Upload
   - Release BOOT when "Connecting..." appears

2. **Try Different Cable**
   - Use a data-capable USB cable (not charge-only)
   - Try different USB port
   - Avoid USB hubs

3. **Reduce Upload Speed**
   - Change to 115200 baud: `Tools → Upload Speed → 115200`

4. **Check Drivers**
   - Windows: Update CH340/CP210x drivers
   - Linux: Check user permissions (`sudo usermod -a -G dialout $USER`)

### ❌ Port Not Showing

**Symptom:** No port available in `Tools → Port`

**Solutions:**

1. **Windows:**
   - Check Device Manager for COM ports
   - Install CH340 or CP210x drivers
   - Try different USB cable

2. **Linux:**
   ```bash
   ls /dev/tty*
   # Should see /dev/ttyUSB0 or similar
   
   # Add user to dialout group:
   sudo usermod -a -G dialout $USER
   # Log out and back in
   ```

3. **Mac:**
   ```bash
   ls /dev/cu.*
   # Should see /dev/cu.usbserial-*
   ```

### ❌ HTTP Requests Fail

**Symptom:** Python script or curl can't connect

**Solutions:**

1. **Ping Test**
   ```bash
   ping 192.168.1.100
   ```
   If ping fails:
   - Check IP address in Serial Monitor
   - Verify on same network
   - Check firewall

2. **Check ESP32**
   - Restart ESP32
   - Check Serial Monitor for errors
   - Verify WiFi connected

3. **Update IP in Code**
   - Make sure you're using correct IP from Serial Monitor

---

## ✅ Success Checklist

Installation is successful when:

- ✅ Serial Monitor shows:
  ```
  Wi-Fi agina baglanildi 
  SSD1306 OLED başarıyla başlatıldı!
  Kamera hazir! Baglanmak icin 'http://192.168.1.100' adresini kullaniniz
  ```

- ✅ OLED Display shows:
  ```
  LEFT   RIGHT   BOTH
  ─────────────────
   0      0      0
  ```

- ✅ Web browser shows camera interface at `http://IP`

- ✅ Video stream works at `http://IP/stream`

- ✅ HTTP POST request updates display:
  ```bash
  curl -X POST http://IP/screen -d "data=0&status=0"
  ```

- ✅ Python test script runs successfully

---

## 🎓 Next Steps

Now that installation is complete:

1. **Test the API** - Try all column and operation combinations
2. **Read API Documentation** - [Screen Features](SCREEN_FEATURES.md)
3. **Check Wiring Guide** - [Wiring Diagrams](WIRING.md)
4. **Build Your Project** - Integrate with face detection
5. **Review Code Changes** - [Changes Documentation](CHANGES.md)

---

## 📞 Getting Help

If you're still stuck:

1. **Double-check everything** in this guide
2. **Review error messages** in Serial Monitor
3. **Test components individually** (camera, then display)
4. **Check GitHub Issues** for similar problems
5. **Create new issue** with:
   - Serial Monitor output (full log)
   - Arduino IDE version and settings
   - Hardware details (board version, display model)
   - Photos of wiring if applicable

---

**📚 Related Documentation:**
- [Screen Features & API](SCREEN_FEATURES.md)
- [Wiring Diagrams](WIRING.md)
- [Code Changes](CHANGES.md)
- [Main README](../README.md)

---

*Last updated: November 2025*
