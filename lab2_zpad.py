import urllib.request
import os
from datetime import datetime
import pandas as pd

# Словник для заміни індексів NOAA (англійська абетка) на українську абетку
noaa_to_ukr = {
    1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21,
    11: 9, 12: 26, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16,
    20: 27, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5
}

def download_vhi_data():
    if not os.path.exists('vhi_data'):
        os.makedirs('vhi_data')
        
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Завантажуємо для областей з 1 по 27 (0 - ігноруємо)
    for province_id in range(1, 28):
        # Перевірка на колізію (чи є вже файл для цієї області)
        existing_files = [f for f in os.listdir('vhi_data') if f.startswith(f"vhi_id_{province_id}_")]
        if existing_files:
            print(f"Дані для області {province_id} вже існують. Пропускаємо.")
            continue
            
        url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1=1981&year2=2024&type=Mean"
        filename = f"vhi_data/vhi_id_{province_id}_{current_time}.csv"
        
        try:
            # Читаємо дані, ігноруючи HTML-теги на початку
            vhi_url = urllib.request.urlopen(url)
            text = vhi_url.read()
            text = text.decode().replace("<tt><pre>", "").replace("</pre></tt>", "")
            
            with open(filename, 'w') as out:
                out.write(text)
            print(f"Збережено: {filename}")
        except Exception as e:
            print(f"Помилка завантаження області {province_id}: {e}")

download_vhi_data()