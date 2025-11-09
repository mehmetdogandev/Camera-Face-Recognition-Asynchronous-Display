# Wiring Diagrams & Hardware Setup

Comprehensive hardware connection guide for the ESP32-CAM OLED Screen Control System.

## 📋 Table of Contents

1. [Quick Connection Guide](#-quick-connection-guide)
2. [Detailed Wiring Diagram](#-detailed-wiring-diagram)
3. [Component Specifications](#-component-specifications)
4. [I2C Configuration](#-i2c-configuration)
5. [Alternative Pin Options](#-alternative-pin-options)
6. [System Architecture](#-system-architecture)
7. [Physical Setup](#-physical-setup)
8. [Hardware Troubleshooting](#-hardware-troubleshooting)
9. [Final Checklist](#-final-checklist)

---

## 🔌 Quick Connection Guide

### OLED SSD1306 Display Wiring

Connect your OLED display to Deneyap Kart (ESP32-CAM) as follows:

```
╔════════════════════════════════════════════╗
║  OLED Pin    →    ESP32-CAM Pin           ║
╠════════════════════════════════════════════╣
║  VCC         →    3.3V                    ║
║  GND         →    GND                     ║
║  SDA         →    D10 (GPIO 19)           ║
║  SCL         →    D11 (GPIO 20)           ║
╚════════════════════════════════════════════╝
```

### Pin Mapping Reference

| OLED Pin | Function | ESP32 Pin | GPIO | Wire Color (typical) |
|----------|----------|-----------|------|---------------------|
| VCC      | Power (+) | 3.3V     | -    | Red                 |
| GND      | Ground (-) | GND      | -    | Black               |
| SDA      | I2C Data  | D10      | 19   | Blue/Green          |
| SCL      | I2C Clock | D11      | 20   | Yellow/White        |

---

## 🎨 Detailed Wiring Diagram

### Visual Connection Diagram

```
        OLED SSD1306 Display
    ┌─────────────────────────┐
    │                         │
    │      128 x 64 px        │
    │    OLED Display         │
    │                         │
    └─────────┬───────────────┘
              │
    ┌─────────┴───────────────┐
    │  VCC GND SDA SCL        │  ← OLED Pins
    └───┬───┬───┬─────┬───────┘
        │   │   │     │
        │   │   │     │
    Red Black Blue Yellow
        │   │   │     │
        │   │   │     │
        ↓   ↓   ↓     ↓
    ┌───┴───┴───┴─────┴───────┐
    │  3.3V GND D10 D11       │  ← ESP32 Pins
    │                         │
    │    Deneyap Kart 1A      │
    │      (ESP32-CAM)        │
    │                         │
    │    ┌──────────┐         │
    │    │  Camera  │         │
    │    │  Module  │         │
    │    └──────────┘         │
    └─────────────────────────┘
```

### Breadboard Layout

```
     Breadboard
    ═══════════════
    
    3.3V ────────● (Red wire to OLED VCC)
    
    GND  ────────● (Black wire to OLED GND)
    
    D10  ────────● (Blue wire to OLED SDA)
    
    D11  ────────● (Yellow wire to OLED SCL)
    
    ═══════════════
```

### Connection Flow

```
┌──────────────┐         I2C Bus          ┌──────────────┐
│              │                           │              │
│   ESP32-CAM  │◄────── SDA (Data) ──────►│  OLED SSD1306│
│              │                           │              │
│  Deneyap     │◄────── SCL (Clock) ─────►│  128x64 px   │
│   Kart 1A    │                           │              │
│              │────── 3.3V (Power) ─────►│              │
│              │                           │              │
│              │────── GND (Ground) ─────►│              │
│              │                           │              │
└──────────────┘                           └──────────────┘
```

---

## 🔧 Component Specifications

### OLED Display (SSD1306)

**Display Specifications:**
- **Resolution**: 128x64 pixels
- **Controller**: SSD1306
- **Interface**: I2C (Two-wire)
- **Default I2C Address**: 0x3C (sometimes 0x3D)
- **Voltage**: 3.3V - 5V (check your specific module!)
- **Current Draw**: ~20mA active, ~10μA sleep
- **Viewing Angle**: >160°
- **Colors**: Monochrome (white, blue, or yellow)

**Compatible Modules:**
- ✅ 0.96" OLED I2C Display
- ✅ 128x64 SSD1306
- ✅ 4-pin I2C variant
- ❌ SPI variants (different pinout)

### ESP32-CAM (Deneyap Kart 1A)

**Microcontroller Specifications:**
- **Chip**: ESP32-S3 / ESP32
- **Flash**: 4MB minimum
- **PSRAM**: Required for camera
- **WiFi**: 2.4GHz 802.11 b/g/n
- **GPIO Available**: Multiple (D10, D11 used for I2C)
- **Voltage**: 5V input via USB, 3.3V logic

**I2C Pins Used:**
- **D10** (GPIO 19): SDA - Serial Data
- **D11** (GPIO 20): SCL - Serial Clock

---

## ⚙️ I2C Configuration

### I2C Address

Most SSD1306 displays use address **0x3C**, but some use **0x3D**.

**How to find your display's address:**

Add this code to your `setup()` function:

```cpp
void setup() {
  Serial.begin(115200);
  Wire.begin(D10, D11);
  
  Serial.println("\nI2C Scanner");
  Serial.println("Scanning...");
  
  byte count = 0;
  
  for (byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    byte error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.printf("I2C device found at address 0x%02X\n", i);
      count++;
    }
    else if (error == 4) {
      Serial.printf("Unknown error at address 0x%02X\n", i);
    }
  }
  
  if (count == 0) {
    Serial.println("No I2C devices found\n");
  } else {
    Serial.printf("\nFound %d device(s)\n", count);
  }
}

void loop() {}
```

**Expected Output:**
```
I2C Scanner
Scanning...
I2C device found at address 0x3C

Found 1 device(s)
```

**Update your code:**
```cpp
#define OLED_ADDR 0x3C  // Use the address you found
```

### I2C Speed

Default I2C speed is 100kHz (standard mode). Can be increased to 400kHz (fast mode).

**Standard Mode (default):**
```cpp
Wire.begin(D10, D11);
Wire.setClock(100000); // 100kHz
```

**Fast Mode (faster updates):**
```cpp
Wire.begin(D10, D11);
Wire.setClock(400000); // 400kHz
```

**If you have communication issues:**
```cpp
Wire.begin(D10, D11);
Wire.setClock(50000); // 50kHz - very slow but reliable
```

### I2C Pull-up Resistors

I2C requires pull-up resistors on SDA and SCL lines.

**Built-in Pull-ups:**
- Most OLED modules have built-in 4.7kΩ or 10kΩ resistors
- ESP32 has optional internal pull-ups (enabled by default)

**If you need external pull-ups:**
```
     3.3V
      │
      ├──[4.7kΩ]───● SDA
      │
      └──[4.7kΩ]───● SCL
```

Only needed if:
- Long cables (>30cm)
- Multiple I2C devices
- Communication errors persist

---

## 🔄 Alternative Pin Options

### Using Different GPIO Pins

If D10/D11 are occupied, you can use other GPIO pins:

**Available GPIO Options:**
```cpp
// Option 1: D8 and D9
Wire.begin(D8, D9);  // SDA=D8, SCL=D9

// Option 2: D12 and D13
Wire.begin(D12, D13);

// Option 3: Direct GPIO numbers
Wire.begin(21, 22);  // SDA=GPIO21, SCL=GPIO22
```

⚠️ **Important Restrictions:**

**DO NOT USE these pins (camera conflict):**
- D0-D9: Camera data pins
- CAMXC, CAMPC, CAMV, CAMH: Camera control
- CAMSD, CAMSC: Camera I2C (different from display I2C)

**Safe GPIO pins for I2C:**
- GPIO 15, 16, 17, 18
- GPIO 19, 20 (D10, D11 - default)
- GPIO 21, 22

### Pin Mapping Table

| Deneyap Label | GPIO Number | Safe for I2C? | Notes |
|---------------|-------------|---------------|-------|
| D0-D7         | Various     | ❌ No         | Camera data |
| D8            | 15          | ✅ Yes        | Alternative |
| D9            | 16          | ✅ Yes        | Alternative |
| D10           | 19          | ✅ Yes        | Default SDA |
| D11           | 20          | ✅ Yes        | Default SCL |
| D12           | 21          | ✅ Yes        | Alternative |
| D13           | 22          | ✅ Yes        | Alternative |

---

## 🏗️ System Architecture

### Component Interaction Diagram

```
┌────────────────────────────────────────────────┐
│              ESP32-CAM System                  │
│                                                │
│  ┌──────────────┐      ┌──────────────┐      │
│  │              │      │              │      │
│  │   Camera     │      │   WiFi       │      │
│  │   Module     │      │   Module     │      │
│  │   (OV2640)   │      │  (2.4GHz)    │      │
│  │              │      │              │      │
│  └──────┬───────┘      └──────┬───────┘      │
│         │                     │              │
│         ↓                     ↓              │
│  ┌──────────────────────────────────┐       │
│  │        ESP32 Processor            │       │
│  │                                   │       │
│  │  ┌────────┐      ┌────────┐     │       │
│  │  │ Camera │      │  HTTP  │     │       │
│  │  │ Driver │      │ Server │     │       │
│  │  └────────┘      └────────┘     │       │
│  │                                   │       │
│  │  ┌────────┐      ┌────────┐     │       │
│  │  │  I2C   │      │  OLED  │     │       │
│  │  │ Master │      │ Driver │     │       │
│  │  └───┬────┘      └────────┘     │       │
│  └──────┼───────────────────────────┘       │
│         │                                    │
│         │ SDA/SCL                            │
│         ↓                                    │
└─────────┼────────────────────────────────────┘
          │
          │ I2C Bus
          │
    ┌─────┴─────┐
    │           │
    │   OLED    │
    │  Display  │
    │ SSD1306   │
    │           │
    └───────────┘
```

### Data Flow

```
External Device (PC/Phone)
        │
        │ HTTP POST /screen
        │ (data=0, status=0)
        ↓
┌──────────────────┐
│   WiFi Module    │
└────────┬─────────┘
         │
         │ TCP/IP
         ↓
┌──────────────────┐
│   HTTP Server    │
│   (app_httpd)    │
└────────┬─────────┘
         │
         │ Parse request
         ↓
┌──────────────────┐
│ Screen Handler   │
│  counterLeft++   │
└────────┬─────────┘
         │
         │ Call function
         ↓
┌──────────────────┐
│  updateDisplay() │
└────────┬─────────┘
         │
         │ I2C commands
         ↓
┌──────────────────┐
│   OLED Driver    │
│  (Adafruit lib)  │
└────────┬─────────┘
         │
         │ I2C protocol
         ↓
┌──────────────────┐
│  OLED Hardware   │
│   (SSD1306)      │
└──────────────────┘
```

---

## 🛠️ Physical Setup

### Cable Management

**Best Practices:**
- ✅ Use cables <20cm long for I2C
- ✅ Keep I2C wires twisted together (reduces noise)
- ✅ Route away from power wires
- ✅ Secure connections with hot glue or tape
- ❌ Avoid coiling excess wire
- ❌ Don't run parallel to high-current wires

### Breadboard Layout

```
    ESP32-CAM Side              OLED Side
    ═════════════              ═══════════
    
    [ 3.3V ]──────────────────►[ VCC ]
    
    [ GND  ]──────────────────►[ GND ]
    
    [ D10  ]──────────────────►[ SDA ]
    
    [ D11  ]──────────────────►[ SCL ]
```

### Permanent Installation

For permanent projects:

1. **Solder Connections**
   - More reliable than jumper wires
   - Use heat shrink tubing for insulation

2. **Use Header Pins**
   - Allows disconnection for maintenance
   - Reduces wear on component pins

3. **Add Mounting**
   - 3D printed case
   - Standoffs for PCB
   - Velcro for display

4. **Power Considerations**
   - Dedicated 5V 2A power supply
   - Not just USB for permanent installations
   - Add decoupling capacitors (100nF, 10µF)

---

## 🔍 Hardware Troubleshooting

### OLED Display Issues

#### Problem: Display Completely Blank

**Check List:**
1. ✅ Power LED on OLED module (if present)?
2. ✅ VCC connected to 3.3V (or 5V if module requires)?
3. ✅ GND connected properly?
4. ✅ Measure voltage at OLED VCC pin (should be 3.3V)

**Voltage Test:**
```
Multimeter between OLED VCC and GND:
Expected: 3.3V ± 0.1V
If 0V: Power not connected
If <3V: Power supply issue
If >3.5V: Wrong voltage! (may damage 3.3V displays)
```

#### Problem: Garbled Display

**Possible Causes:**
1. **Cable Issues**
   - Loose connections
   - Cables too long (>20cm)
   - Electromagnetic interference

2. **I2C Speed Too High**
   ```cpp
   Wire.setClock(100000); // Try reducing to 100kHz
   ```

3. **Power Supply Noise**
   - Add 100nF capacitor near OLED VCC/GND
   - Use better quality USB cable/power supply

#### Problem: Display Flickers

**Solutions:**
1. **Stabilize Power**
   - Add 100µF capacitor at ESP32 power input
   - Use powered USB hub
   - Dedicated power supply

2. **Check Current Draw**
   - Ensure power supply can provide >500mA
   - USB 2.0 port minimum

3. **Software Update Rate**
   - Don't update display faster than 10Hz
   - Add delays in code if needed

### I2C Communication Issues

#### Problem: "I2C device not found"

**Systematic Debugging:**

1. **Hardware Check**
   ```
   Step 1: Check continuity
   - Multimeter resistance test:
     ESP32 D10 to OLED SDA: Should be ~0Ω
     ESP32 D11 to OLED SCL: Should be ~0Ω
   
   Step 2: Check for shorts
   - SDA to SCL: Should be open (∞Ω)
   - VCC to GND: Should be open (∞Ω)
   ```

2. **Run I2C Scanner** (code provided earlier)
   - If found at different address: Update `OLED_ADDR`
   - If not found: Hardware problem

3. **Try Different Pins**
   ```cpp
   Wire.begin(D12, D13); // Try alternative pins
   ```

4. **External Pull-ups**
   - Add 4.7kΩ resistors from SDA/SCL to 3.3V

#### Problem: Works Initially, Then Stops

**Possible Causes:**

1. **Wire Fatigue**
   - Flex in jumper wires breaks connections
   - Solution: Solder connections or use better quality wires

2. **Heating Issues**
   - Components overheating
   - Solution: Improve ventilation, check current draw

3. **Software Crash**
   - Check Serial Monitor for error messages
   - Add watchdog timer

### Power Supply Issues

#### Problem: ESP32 Resets Randomly

**Diagnosis:**
- Insufficient current from USB port
- Camera and OLED together draw >500mA

**Solutions:**
1. **Use USB 3.0 Port** (can provide more current)
2. **Powered USB Hub**
3. **External 5V 2A Power Supply**
4. **Add Bulk Capacitor** (1000µF at 5V input)

#### Problem: Brown-out Detection

Serial Monitor shows:
```
Brownout detector was triggered
```

**Solutions:**
- Better power supply (5V 2A minimum)
- Shorter/better USB cable
- Lower WiFi transmission power in code

---

## ✅ Final Checklist

### Before First Power-On

Hardware Checklist:
- [ ] VCC connected to 3.3V (or 5V if module requires)
- [ ] GND connected to GND
- [ ] SDA connected to D10
- [ ] SCL connected to D11
- [ ] No short circuits (checked with multimeter)
- [ ] All connections are secure
- [ ] Cables are <20cm long
- [ ] OLED module is correct type (I2C, not SPI)

Software Checklist:
- [ ] Arduino libraries installed (Adafruit GFX, Adafruit SSD1306)
- [ ] Partition Scheme set to "Huge APP"
- [ ] WiFi credentials configured
- [ ] I2C address correct (0x3C or 0x3D)
- [ ] Code compiled without errors

### After Power-On

Verification Checklist:
- [ ] Serial Monitor shows boot messages
- [ ] WiFi connects successfully
- [ ] IP address displayed
- [ ] "OLED ekran başarıyla başlatıldı!" message appears
- [ ] OLED shows initial display (LEFT RIGHT BOTH / 0 0 0)
- [ ] Camera web interface accessible
- [ ] HTTP POST request works
- [ ] Display updates correctly

### For Production Deployment

Optional Improvements:
- [ ] Solder all connections
- [ ] Add strain relief for wires
- [ ] Mount in enclosure/case
- [ ] Label connections
- [ ] Add status LED indicators
- [ ] Use dedicated power supply
- [ ] Add fuse for safety
- [ ] Document final pin usage

---

## 📐 Mechanical Specifications

### Display Dimensions (typical 0.96" OLED)

```
    27.5mm
  ┌────────┐
  │  OLED  │ 27mm
  │ Active │
  │  Area  │
  └────────┘
```

### Mounting Holes

Most modules have 2-4 mounting holes:
- Diameter: 2-3mm
- Spacing: Standard varies by module
- Use M2 or M2.5 screws

### Clearance Requirements

```
        │← 5mm →│
        ╔════════╗  ↑
     ───╣  OLED  ╠  │ Clearance
        ╚════════╝  ↓ for heat
        │← 5mm →│
```

Minimum clearances:
- Top: 5mm (for heat dissipation)
- Sides: 3mm (for wiring)
- Bottom: 10mm (for pins/wiring)

---

## 🔗 References

### Datasheets
- [SSD1306 Datasheet](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf)
- [ESP32-S3 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)

### Related Guides
- [Installation Guide](INSTALLATION.md)
- [Screen Features](SCREEN_FEATURES.md)
- [Code Changes](CHANGES.md)
- [Main README](../README.md)

---

*Last updated: November 2025*
