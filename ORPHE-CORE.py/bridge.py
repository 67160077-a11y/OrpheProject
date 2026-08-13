import time
import requests
# ดึงฟังก์ชันมาจากไฟล์เดิมของคุณ เช่น get_sensor_values.py
# สมมติว่าใน get_sensor_values มีฟังก์ชัน get_all_values()
from get_sensor_values import get_all_values 

BACKEND_URL = "http://localhost:8765/update-data"

while True:
    # 1. ดึงค่าจากฮาร์ดแวร์ (ปรับเปลี่ยนตามฟังก์ชันจริงของคุณ)
    sensor_data = get_all_values() 
    
    # 2. ยิงค่าไปที่ Backend
    try:
        requests.post(BACKEND_URL, json=sensor_data)
    except:
        print("Backend ยังไม่เปิด...")
        
    time.sleep(0.5)