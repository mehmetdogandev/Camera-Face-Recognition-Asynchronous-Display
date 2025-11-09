"""
Test script for OLED screen control via HTTP POST
"""
import requests
import time

# ESP32-CAM IP adresi (seri monitörden alacaksınız)
ESP32_IP = ""  # BURAYA KENDI IP ADRESİNİZİ YAZIN
SCREEN_URL = f"http://{ESP32_IP}/screen"

def update_screen(data, status):
    """
    OLED ekranı güncelle
    
    Args:
        data (int): 0=SOL, 1=SAĞ, 2=İKİSİ
        status (int): 0=ARTTIR, 1=AZALT
    """
    payload = {
        'data': data,
        'status': status
    }
    
    try:
        response = requests.post(SCREEN_URL, data=payload, timeout=2)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Başarılı: Sol={result['left']}, Sağ={result['right']}, İkisi={result['both']}")
        else:
            print(f"✗ Hata: {response.status_code}")
    except Exception as e:
        print(f"✗ Bağlantı hatası: {e}")

# Test senaryoları
if __name__ == "__main__":
    print("OLED Ekran Test Scripti")
    print("=" * 50)
    print()
    
    # Sol sütunu arttır
    print("1. Sol sütunu arttır (data=0, status=0)")
    update_screen(data=0, status=0)
    time.sleep(1)
    
    # Sol sütunu arttır
    print("2. Sol sütunu arttır (data=0, status=0)")
    update_screen(data=0, status=0)
    time.sleep(1)
    
    # Sağ sütunu arttır
    print("3. Sağ sütunu arttır (data=1, status=0)")
    update_screen(data=1, status=0)
    time.sleep(1)
    
    # İkisi sütunu arttır
    print("4. İkisi sütunu arttır (data=2, status=0)")
    update_screen(data=2, status=0)
    time.sleep(1)
    
    # Sol sütunu azalt
    print("5. Sol sütunu azalt (data=0, status=1)")
    update_screen(data=0, status=1)
    time.sleep(1)
    
    # Sağ sütunu arttır
    print("6. Sağ sütunu arttır (data=1, status=0)")
    update_screen(data=1, status=0)
    time.sleep(1)
    
    # İkisi sütunu azalt
    print("7. İkisi sütunu azalt (data=2, status=1)")
    update_screen(data=2, status=1)
    
    print()
    print("Test tamamlandı!")
