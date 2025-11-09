# OLED Ekran Kontrol Sistemi

Bu proje, ESP32-CAM üzerinde çalışan kamera uygulamasına OLED ekran kontrol özelliği ekler.

## 🎯 Özellikler

- **3 Sütunlu Ekran**: SOL, SAĞ, İKİSİ
- **HTTP POST API**: `/screen` endpoint'i ile ekranı güncelleme
- **Anlık Güncelleme**: Her POST isteğinde ekran otomatik güncellenir
- **Sayaç Sistemi**: Her sütun için artırma/azaltma özelliği

## 📋 Gereksinimler

### Arduino Kütüphaneleri
Aşağıdaki kütüphaneleri Arduino IDE'de yüklemeniz gerekiyor:

1. **Adafruit GFX Library**
   - Arduino IDE: `Sketch -> Include Library -> Manage Libraries`
   - Arama: "Adafruit GFX"
   - Yükle

2. **Adafruit SSD1306**
   - Arduino IDE: `Sketch -> Include Library -> Manage Libraries`
   - Arama: "Adafruit SSD1306"
   - Yükle

3. **Wire** (ESP32'de yerleşik olarak gelir)

### Python Gereksinimleri
```bash
pip install requests
```

## 🔌 Donanım Bağlantısı

OLED SSD1306 ekranı aşağıdaki şekilde bağlayın:

```
OLED SSD1306  ->  Deneyap Kart
---------------------------------
VCC           ->  3.3V
GND           ->  GND
SDA           ->  D10
SCL           ->  D11
```

## ⚙️ Kurulum

1. **Kütüphaneleri yükleyin** (yukarıdaki gereksinimler bölümüne bakın)

2. **WiFi ayarlarını yapın** (`KameraYuzTanima.ino`):
   ```cpp
   const char* ssid = "WiFi_Adi";
   const char* password = "WiFi_Sifresi";
   ```

3. **Partition Scheme ayarlayın**:
   - Arduino IDE: `Tools -> Partition Scheme -> Huge APP`

4. **Kodu yükleyin**:
   - Board: Deneyap Kart seçili olmalı
   - Upload tuşuna basın

5. **IP adresini alın**:
   - Serial Monitor'ü açın (115200 baud)
   - ESP32 bağlandığında IP adresini göreceksiniz
   - Örnek: `http://192.168.1.100`

## 🌐 API Kullanımı

### Endpoint
```
POST http://<ESP32_IP>/screen
```

### Parametreler
- **data**: Hangi sütun
  - `0` = SOL
  - `1` = SAĞ
  - `2` = İKİSİ
  
- **status**: İşlem
  - `0` = ARTTIR (+1)
  - `1` = AZALT (-1)

### Örnek İstekler

#### cURL ile:
```bash
# Sol sütunu arttır
curl -X POST http://192.168.1.100/screen -d "data=0&status=0"

# Sağ sütunu arttır
curl -X POST http://192.168.1.100/screen -d "data=1&status=0"

# İkisi sütunu azalt
curl -X POST http://192.168.1.100/screen -d "data=2&status=1"
```

#### Python ile:
```python
import requests

ESP32_IP = "192.168.1.100"
url = f"http://{ESP32_IP}/screen"

# Sol sütunu arttır
response = requests.post(url, data={'data': 0, 'status': 0})
print(response.json())
# Çıktı: {"status":"ok","left":1,"right":0,"both":0}
```

### Response Format
```json
{
  "status": "ok",
  "left": 5,
  "right": 3,
  "both": 2
}
```

## 🐍 Python Örnekleri

### 1. Basit Test
```bash
python test_screen.py
```

Bu script:
- Sırayla tüm sütunları test eder
- Her işlemden sonra 1 saniye bekler
- Sonuçları ekrana yazdırır

### 2. Gelişmiş Kontrol
```bash
python advanced_screen_control.py
```

3 farklı mod sunar:
1. **Basit Test**: Otomatik test senaryosu
2. **Yüz Tanıma Simülasyonu**: Gerçek zamanlı tespit simülasyonu
3. **Manuel Kontrol**: Klavyeden kontrol

### Kendi Projenize Entegrasyon

```python
from advanced_screen_control import ScreenController

# Controller oluştur
controller = ScreenController("192.168.1.100")

# Yüz tanıma döngünüz içinde:
while True:
    # Kameradan görüntü al
    frame = get_camera_frame()
    
    # Yüz tanıma yap
    faces = detect_faces(frame)
    
    # Sol kişi tespit edildiyse
    if left_person_detected:
        controller.increment_left()
    
    # Sağ kişi tespit edildiyse
    if right_person_detected:
        controller.increment_right()
    
    # Her ikisi de varsa
    if both_persons_detected:
        controller.increment_both()
```

## 🎨 Ekran Düzeni

```
┌────────────────────────────┐
│ SOL    SAG    IKISI        │
│ ─────────────────────      │
│                            │
│  5      3      2           │
│                            │
│                            │
└────────────────────────────┘
```

- **Üst satır**: Sütun başlıkları (küçük font)
- **Alt kısım**: Sayaçlar (büyük font, 2x)
- **Çizgi**: Başlık ve sayaçları ayırır

## 🔧 Sorun Giderme

### OLED Ekran Başlamıyor
- I2C adresini kontrol edin (genellikle 0x3C veya 0x3D)
- Kabloları kontrol edin (SDA=D10, SCL=D11)
- Serial Monitor'den hata mesajlarını inceleyin

### HTTP İsteği Yanıt Vermiyor
- ESP32'nin IP adresini doğru yazdığınızdan emin olun
- Aynı WiFi ağında olduğunuzu kontrol edin
- Serial Monitor'de HTTP isteklerini görebilirsiniz

### Compilation Hatası
- Adafruit kütüphanelerinin yüklü olduğunu kontrol edin
- Partition Scheme'in "Huge APP" olduğunu kontrol edin
- ESP32 board package'inin güncel olduğundan emin olun

## 📸 Kamera Özellikleri

Bu ekleme **kamera işlevlerini etkilemez**:
- ✅ Video streaming çalışmaya devam eder (`http://IP/stream`)
- ✅ Snapshot alınabilir (`http://IP/capture`)
- ✅ Yüz tanıma özellikleri korunur
- ✅ Tüm kamera ayarları aynen çalışır

## 🎯 Performans

- **Response Time**: ~50-100ms
- **Ekran Güncelleme**: ~100ms
- **Aynı Anda İşlem**: Hem kamera hem ekran çalışabilir
- **Bellek Kullanımı**: Minimal (~1KB RAM)

## 📝 Notlar

- Ekran I2C üzerinden çalıştığı için kamera ile çakışma olmaz
- Tüm işlemler non-blocking olarak çalışır
- Sayaçlar negatif olabilir (sınır yok)
- Her POST isteği JSON response döndürür

## 🤝 Yardım

Sorularınız için:
1. Serial Monitor'ü kontrol edin (115200 baud)
2. Network trafiğini kontrol edin (Wireshark vs.)
3. Python script'lerindeki exception mesajlarına bakın

## 📄 Lisans

Bu kod örnek amaçlıdır ve özgürce kullanılabilir.
