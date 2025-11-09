# Hızlı Kurulum Rehberi

## 1️⃣ Arduino IDE Kütüphane Kurulumu

### Adım 1: Kütüphane Yöneticisini Açın
- Arduino IDE'yi açın
- `Sketch` → `Include Library` → `Manage Libraries...` menüsüne gidin

### Adım 2: Adafruit GFX Kütüphanesini Yükleyin
1. Arama kutusuna `Adafruit GFX` yazın
2. "Adafruit GFX Library" by Adafruit'i bulun
3. `Install` butonuna tıklayın
4. Bağımlılıkları da yüklemek ister, `Install All` deyin

### Adım 3: Adafruit SSD1306 Kütüphanesini Yükleyin
1. Arama kutusuna `Adafruit SSD1306` yazın
2. "Adafruit SSD1306" by Adafruit'i bulun
3. `Install` butonuna tıklayın
4. Bağımlılıkları da yüklemek ister, `Install All` deyin

## 2️⃣ Donanım Bağlantısı

### OLED Ekran (SSD1306) Bağlantısı

```
OLED Pin  →  Deneyap Kart
─────────────────────────
VCC       →  3.3V
GND       →  GND
SDA       →  D10 (GPIO)
SCL       →  D11 (GPIO)
```

⚠️ **DİKKAT**: 
- Bazı OLED modüller 5V ile çalışır, kendi modülünüzün pinout'una bakın
- I2C adresi genellikle 0x3C'dir, bazılarında 0x3D olabilir

## 3️⃣ Arduino IDE Ayarları

### Board Ayarları (Tools menüsünden):
- **Board**: "Deneyap Kart 1A" veya "Deneyap Kart 1A v2"
- **Partition Scheme**: ⚠️ **"Huge APP (3MB No OTA/1MB SPIFFS)"**
- **Upload Speed**: 921600
- **CPU Frequency**: 240MHz (WiFi/BT)
- **Flash Frequency**: 80MHz
- **Flash Mode**: QIO
- **Port**: Kartınızın bağlı olduğu COM port

### Partition Scheme Neden Önemli?
Bu proje büyük bir firmware oluşturur:
- Kamera driver
- WiFi
- Web server
- OLED driver
- Yüz tanıma (opsiyonel)

Bu yüzden **"Huge APP"** seçilmeli!

## 4️⃣ WiFi Ayarları

`KameraYuzTanima.ino` dosyasını açın ve şu satırları düzenleyin:

```cpp
const char* ssid = "WiFi_Aginizin_Adi";
const char* password = "WiFi_Sifreniz";
```

## 5️⃣ Kod Yükleme

1. Arduino IDE'de `KameraYuzTanima.ino` dosyasını açın
2. Yukarıdaki ayarları kontrol edin
3. ✅ **Verify/Compile** butonuna basın
4. Hata yoksa ⬆️ **Upload** butonuna basın
5. Yükleme tamamlanana kadar bekleyin (~2-3 dakika)

## 6️⃣ IP Adresini Öğrenme

1. Arduino IDE'de `Tools` → `Serial Monitor` açın
2. Baud rate'i **115200** yapın
3. ESP32 reset olacak ve bağlantı bilgilerini göreceksiniz:

```
Wi-Fi agina baglanildi 
Kamera hazir! Baglanmak icin 'http://192.168.1.100' adresini kullaniniz
```

📝 Bu IP adresini not alın!

## 7️⃣ Test Etme

### Web Tarayıcıdan:
- Tarayıcınıza `http://192.168.1.100` (kendi IP'niz) yazın
- Kamera stream'ini göreceksiniz

### OLED Ekranı Test Etme:

#### Yöntem 1: cURL (Windows PowerShell)
```powershell
# Sol sütunu arttır
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=0&status=0"

# Sağ sütunu arttır
Invoke-WebRequest -Uri "http://192.168.1.100/screen" -Method POST -Body "data=1&status=0"
```

#### Yöntem 2: Python
```bash
# Python requirements yükle
pip install requests

# Test script'i çalıştır
python test_screen.py
```

📝 Python script'te IP adresini güncellemeyi unutmayın!

## 8️⃣ Sorun Giderme

### ❌ "OLED ekran başlatılamadı"
- **Çözüm 1**: Kablo bağlantılarını kontrol edin
- **Çözüm 2**: I2C adresini kontrol edin (kod içinde OLED_ADDR)
- **Çözüm 3**: OLED'in VCC pinini kontrol edin (3.3V mi 5V mi?)

### ❌ "WiFi'ye bağlanamıyor"
- SSID ve şifreyi kontrol edin
- 2.4GHz WiFi kullanın (ESP32 5GHz desteklemez)
- Özel karakterler varsa dikkat edin

### ❌ "Sketch too big" hatası
- Partition Scheme'i **Huge APP** yapın!
- `Tools` → `Partition Scheme` → `Huge APP (3MB No OTA/1MB SPIFFS)`

### ❌ "A fatal error occurred: Failed to connect"
- Kartı USB'den çıkarıp tekrar takın
- Başka bir USB portu deneyin
- Upload hızını 115200'e düşürün

### ❌ HTTP POST çalışmıyor
- IP adresini doğru yazdığınızdan emin olun
- Bilgisayarınız ve ESP32 aynı ağda olmalı
- Firewall engellemiş olabilir

## 9️⃣ Başarı Kriterleri

✅ **Başarılı kurulum şu şekilde görünür:**

1. **Serial Monitor çıktısı:**
```
Wi-Fi agina baglanildi 
SSD1306 OLED başarıyla başlatıldı!
Kamera hazir! Baglanmak icin 'http://192.168.1.100' adresini kullaniniz
```

2. **OLED Ekran:**
```
SOL    SAG    IKISI
─────────────────
 0      0      0
```

3. **Web tarayıcı:** Kamera görüntüsü akıyor

4. **Python testi:** JSON response geliyor
```json
{"status":"ok","left":1,"right":0,"both":0}
```

## 🎓 İleri Seviye

### I2C Adresini Değiştirme
Eğer ekranınız başlamıyorsa, I2C adresini tarayın:

```cpp
// Test kodu - setup() içine ekleyin
Wire.begin(D10, D11);
for (byte i = 0; i < 127; i++) {
  Wire.beginTransmission(i);
  if (Wire.endTransmission() == 0) {
    Serial.printf("I2C cihaz bulundu: 0x%02X\n", i);
  }
}
```

Bulunan adresi `OLED_ADDR` makrosunda kullanın.

## 📞 Yardım

Hala sorun yaşıyorsanız:
1. Serial Monitor çıktısını paylaşın
2. Hata mesajlarını not edin
3. README_SCREEN.md dosyasını inceleyin
