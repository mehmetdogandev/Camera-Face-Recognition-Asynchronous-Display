"""
Gelişmiş OLED Ekran Kontrolü - Anlık güncellemeler için
"""
import requests
import time
import random

# ESP32-CAM IP adresi
ESP32_IP = "10.64.220.72"  # BURAYA KENDI IP ADRESİNİZİ YAZIN
SCREEN_URL = f"http://{ESP32_IP}/screen"

class ScreenController:
    """OLED ekran kontrolcüsü"""
    
    def __init__(self, ip_address):
        self.url = f"http://{ip_address}/screen"
        self.last_response = None
    
    def update(self, column, increment=True):
        """
        Ekranı güncelle
        
        Args:
            column (str): 'left', 'right', 'both'
            increment (bool): True=arttır, False=azalt
        """
        # Sütun mapping
        column_map = {
            'left': 0,
            'sol': 0,
            'right': 1,
            'sag': 1,
            'sağ': 1,
            'both': 2,
            'ikisi': 2
        }
        
        data = column_map.get(column.lower(), 0)
        status = 0 if increment else 1
        
        payload = {'data': data, 'status': status}
        
        try:
            response = requests.post(self.url, data=payload, timeout=1)
            if response.status_code == 200:
                self.last_response = response.json()
                return True
            return False
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
            return False
    
    def get_counters(self):
        """Son bilinen sayaç değerlerini döndür"""
        if self.last_response:
            return self.last_response
        return {'left': 0, 'right': 0, 'both': 0}
    
    def increment_left(self):
        """Sol sayacı arttır"""
        return self.update('left', increment=True)
    
    def decrement_left(self):
        """Sol sayacı azalt"""
        return self.update('left', increment=False)
    
    def increment_right(self):
        """Sağ sayacı arttır"""
        return self.update('right', increment=True)
    
    def decrement_right(self):
        """Sağ sayacı azalt"""
        return self.update('right', increment=False)
    
    def increment_both(self):
        """İkisi sayacı arttır"""
        return self.update('both', increment=True)
    
    def decrement_both(self):
        """İkisi sayacı azalt"""
        return self.update('both', increment=False)

# Örnek kullanım 1: Basit test
def simple_test(controller):
    """Basit test fonksiyonu"""
    print("\n=== BASIT TEST ===")
    
    print("Sol +5")
    for _ in range(5):
        controller.increment_left()
        time.sleep(0.2)
    
    print("Sağ +3")
    for _ in range(3):
        controller.increment_right()
        time.sleep(0.2)
    
    print("İkisi +2")
    for _ in range(2):
        controller.increment_both()
        time.sleep(0.2)
    
    counters = controller.get_counters()
    print(f"\nSonuç: Sol={counters['left']}, Sağ={counters['right']}, İkisi={counters['both']}")

# Örnek kullanım 2: Yüz tanıma simülasyonu
def face_detection_simulation(controller, duration=30):
    """
    Yüz tanıma simülasyonu - Python projenizle nasıl entegre edeceğinizi gösterir
    
    Args:
        controller: ScreenController instance
        duration: Kaç saniye çalışacak
    """
    print(f"\n=== YÜZ TANIMA SİMÜLASYONU ({duration} saniye) ===")
    print("Sol: Sol kişi tespit edildi")
    print("Sağ: Sağ kişi tespit edildi")
    print("İkisi: Her iki kişi tespit edildi")
    print()
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Rastgele yüz tespiti simülasyonu
        detection = random.choice(['left', 'right', 'both', 'none'])
        
        if detection == 'left':
            print("👤 Sol kişi tespit edildi!")
            controller.increment_left()
        elif detection == 'right':
            print("👤 Sağ kişi tespit edildi!")
            controller.increment_right()
        elif detection == 'both':
            print("👥 Her ikisi tespit edildi!")
            controller.increment_both()
        else:
            print("   Kimse yok")
        
        # Gerçek uygulamanızda burada kamera frame'i analiz edilecek
        time.sleep(1)
    
    counters = controller.get_counters()
    print(f"\n📊 Toplam Tespit:")
    print(f"   Sol kişi: {counters['left']} kez")
    print(f"   Sağ kişi: {counters['right']} kez")
    print(f"   İkisi birlikte: {counters['both']} kez")

# Örnek kullanım 3: Manuel kontrol
def manual_control(controller):
    """Manuel kontrol - Klavyeden komut alır"""
    print("\n=== MANUEL KONTROL ===")
    print("Komutlar:")
    print("  l+ : Sol arttır    | l- : Sol azalt")
    print("  r+ : Sağ arttır    | r- : Sağ azalt")
    print("  b+ : İkisi arttır  | b- : İkisi azalt")
    print("  q  : Çıkış")
    print()
    
    while True:
        cmd = input("Komut: ").strip().lower()
        
        if cmd == 'q':
            break
        elif cmd == 'l+':
            controller.increment_left()
            print("Sol +1")
        elif cmd == 'l-':
            controller.decrement_left()
            print("Sol -1")
        elif cmd == 'r+':
            controller.increment_right()
            print("Sağ +1")
        elif cmd == 'r-':
            controller.decrement_right()
            print("Sağ -1")
        elif cmd == 'b+':
            controller.increment_both()
            print("İkisi +1")
        elif cmd == 'b-':
            controller.decrement_both()
            print("İkisi -1")
        else:
            print("Geçersiz komut!")
        
        counters = controller.get_counters()
        print(f"Durum: Sol={counters['left']}, Sağ={counters['right']}, İkisi={counters['both']}\n")

if __name__ == "__main__":
    print("OLED Ekran Kontrol Sistemi")
    print("=" * 60)
    print()
    print("IP adresini güncelleyin ve bir test seçin:")
    print("1. Basit Test")
    print("2. Yüz Tanıma Simülasyonu")
    print("3. Manuel Kontrol")
    print()
    
    choice = input("Seçim (1-3): ").strip()
    
    # Controller oluştur
    controller = ScreenController(ESP32_IP)
    
    if choice == '1':
        simple_test(controller)
    elif choice == '2':
        face_detection_simulation(controller, duration=30)
    elif choice == '3':
        manual_control(controller)
    else:
        print("Geçersiz seçim!")
