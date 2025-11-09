# 🔌 Bağlantı Şeması

## OLED SSD1306 Ekran Bağlantısı

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                  Deneyap Kart 1A                        │
│                                                         │
│  ┌────┐  ┌────┐  ┌────┐  ┌────┐                       │
│  │3.3V│  │GND │  │D10 │  │D11 │                       │
│  └─┬──┘  └─┬──┘  └─┬──┘  └─┬──┘                       │
│    │       │       │       │                           │
└────┼───────┼───────┼───────┼───────────────────────────┘
     │       │       │       │
     │       │       │       │
     │       │       │       │
     │       │       │       │     ┌────────────────────┐
     │       │       │       │     │                    │
     │       │       │       └─────┤ SCL    OLED        │
     │       │       │             │        SSD1306     │
     │       │       └─────────────┤ SDA    128x64      │
     │       │                     │                    │
     │       └─────────────────────┤ GND                │
     │                             │                    │
     └─────────────────────────────┤ VCC                │
                                   │                    │
                                   └────────────────────┘
```

## Detaylı Bağlantı Tablosu

| Deneyap Pin | → | OLED Pin | Açıklama |
|-------------|---|----------|----------|
| **3.3V**    | → | **VCC**  | Güç beslemesi (bazı modüllerde 5V) |
| **GND**     | → | **GND**  | Topraklama |
| **D10**     | → | **SDA**  | I2C Data hattı |
| **D11**     | → | **SCL**  | I2C Clock hattı |

## ⚠️ Önemli Notlar

### Voltaj Seçimi
```
┌────────────────────────────────────────┐
│ OLED Modül Etiketine Bakın:           │
├────────────────────────────────────────┤
│ "3.3V-5V" yazıyorsa → 3.3V kullanın   │
│ Sadece "5V" yazıyorsa → 5V gerekir    │
│ Sadece "3.3V" yazıyorsa → 3.3V gerekir│
└────────────────────────────────────────┘
```

### I2C Adresi Kontrolü

Bazı OLED modüllerde adres farklı olabilir:

```cpp
// KameraYuzTanima.ino içinde:
#define OLED_ADDR 0x3C  // Yaygın adres

// Eğer başlamazsa 0x3D deneyin:
#define OLED_ADDR 0x3D
```

### Adres Tarama Kodu

Eğer ekran başlamazsa, bu kodu çalıştırarak adresi bulabilirsiniz:

```cpp
void setup() {
  Serial.begin(115200);
  Wire.begin(D10, D11);
  
  Serial.println("I2C Adres Taraması Başlıyor...");
  
  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.printf("I2C cihaz bulundu: 0x%02X\n", address);
    }
  }
  
  Serial.println("Tarama tamamlandı!");
}

void loop() {}
```

## 🎯 Pin Alternatifleri

Eğer D10/D11 başka bir şey için kullanıyorsanız, I2C pinlerini değiştirebilirsiniz:

### Kod Değişikliği:
```cpp
// KameraYuzTanima.ino içinde:
Wire.begin(D10, D11);  // Varsayılan

// Alternatif pinler:
Wire.begin(D8, D9);    // veya
Wire.begin(D12, D13);  // veya başka GPIO'lar
```

⚠️ **Dikkat:** Kamera pinleri ile çakışmamalı!

## 📊 Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────┐
│                    ESP32-CAM (Deneyap)                   │
│                                                           │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │   Kamera    │    │  Web Server  │    │    I2C     │ │
│  │   Modülü    │    │   (WiFi)     │    │  OLED      │ │
│  │             │    │              │    │  Driver    │ │
│  │  Görüntü ──→│──→│ HTTP Stream  │    │            │ │
│  │   Akışı     │    │              │    │  Display ──→ │
│  └─────────────┘    │              │    │  Update    │ │
│                     │ /screen ────→│──→│            │ │
│                     │  endpoint    │    └────────────┘ │
│                     └──────────────┘                    │
│                            ↑                            │
└────────────────────────────┼────────────────────────────┘
                             │
                             │ WiFi
                             ↓
                    ┌────────────────┐
                    │   PC/Laptop    │
                    │                │
                    │  Python Script │
                    │  POST Request  │
                    └────────────────┘
```

## 🔍 Fiziksel Bağlantı Kontrolü

### Adım 1: Güç Kontrolü
```
Multimetre ile kontrol:
VCC pin → GND pin arası: ~3.3V olmalı
```

### Adım 2: I2C Sinyalleri
```
Oscilloscope varsa:
SDA ve SCL pinlerinde kare dalga görmeli
```

### Adım 3: Görsel Kontrol
```
✓ Kablolar sağlam takılı mı?
✓ OLED ekranda LED yanıyor mu?
✓ Lehim soğuk mu? (DIY modüllerde)
```

## 🛠️ Sorun Giderme - Donanım

### Sorun: OLED hiç yanmıyor

1. **Güç kontrolü:**
   ```
   ☑ VCC → 3.3V bağlı mı?
   ☑ GND → GND bağlı mı?
   ☑ Kart çalışıyor mu? (LED yanıyor mu?)
   ```

2. **OLED arızası:**
   - Başka bir OLED ile test edin
   - Veya başka bir Arduino ile test edin

### Sorun: "OLED ekran başlatılamadı" hatası

1. **I2C bağlantısı:**
   ```
   ☑ SDA → D10 doğru mu?
   ☑ SCL → D11 doğru mu?
   ☑ Kablolar kopuk değil mi?
   ```

2. **I2C adresi:**
   - Adres tarama kodunu çalıştırın
   - Bulunan adresi kullanın (0x3C veya 0x3D)

3. **Pull-up dirençleri:**
   - Bazı OLED'lerde dahili pull-up var
   - Yoksa 4.7kΩ dirençler ekleyin:
   ```
   3.3V ──┬── 4.7kΩ ──┬── SDA
          │           │
          └── 4.7kΩ ──┴── SCL
   ```

### Sorun: Ekran bozuk görüntü veriyor

1. **Kablo boyu:**
   - 20cm'den kısa kablolar kullanın
   - Uzun kablolar sinyal bozulmasına yol açar

2. **Elektromanyetik gürültü:**
   - OLED'i kamera modülünden uzak tutun
   - Twisted pair kablo kullanın

3. **I2C hızı:**
   ```cpp
   // Hızı düşür (bazı OLED'ler yavaştır)
   Wire.setClock(100000);  // 100kHz (varsayılan 400kHz)
   ```

## 📸 Örnek Bağlantı Fotoğrafları

```
Doğru Bağlantı:
┌──────────────┐
│ OLED         │
│ ┌──┐ ┌──┐   │
│ │  │ │  │   │◄── Pinler düzgün takılı
│ └──┘ └──┘   │
└──────────────┘
      ││
      ││  ◄── Kısa, düzgün kablolar
      ││
┌────────────────┐
│  Deneyap Kart  │
└────────────────┘


Yanlış Bağlantı:
┌──────────────┐
│ OLED         │
│ ┌──┐ ┌──┐   │
│ │  │ │  │   │◄── Gevşek
│ └──┘ └──┘   │
└──────────────┘
      ││
      ││  ◄── Çok uzun veya karışık
    ┌─┴┴─┐
    │    │
┌────────────────┐
│  Deneyap Kart  │
└────────────────┘
```

## ✅ Final Checklist

Bağlantı yapmadan önce:

- [ ] OLED'in voltaj gereksinimini kontrol ettim (3.3V veya 5V)
- [ ] Kablo uzunluğu 20cm'den kısa
- [ ] Pinler doğru: VCC→3.3V, GND→GND, SDA→D10, SCL→D11
- [ ] Kablolar sağlam takılı
- [ ] Kamera pinleri ile çakışma yok
- [ ] I2C adresini biliyorum (genellikle 0x3C)

Kod yüklemeden önce:

- [ ] Bağlantıları tekrar kontrol ettim
- [ ] USB kablosu sağlam
- [ ] Partition Scheme = Huge APP
- [ ] WiFi SSID ve şifre doğru

İlk çalıştırmada:

- [ ] Serial Monitor açık (115200 baud)
- [ ] "OLED ekran başarıyla başlatıldı!" mesajını gördüm
- [ ] OLED'de "SOL SAG IKISI" başlıkları görünüyor
- [ ] IP adresini not aldım

Hepsi ✅ ise devam! 🚀
