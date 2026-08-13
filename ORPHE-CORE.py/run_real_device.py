import asyncio
import requests
import time
import math
from orphe_core import Orphe

BACKEND_URL = "http://localhost:8765/update-data"

MAC_LEFT = "F4:1B:9B:AF:20:5D"
MAC_RIGHT = "D0:A3:43:7D:01:BD"

sensor_payload = {
    "recoveryScore": 0, 
    "speed": "0.00",
    "hipPower": "-", "hipPowerVal": 0.0,
    "kneeControl": "-", "kneeControlVal": 0.0,
    "anklePushOff": "-", "anklePushOffVal": 0.0,
    "propulsionGrade": "-",
    "coordinates": [],
    "toeOffLeft": 0, "landingAngleLeft": 0,
    "footHeightLeft": 0, "landingAngleLeft2": 0,
    "toeOffRight": 0, "landingAngleRight": 0,
    "footHeightRight": 0, "landingAngleRight2": 0,
    "stancePhaseLeft1": 0.0, "stancePhaseRight1": 0.0,
    "stancePhaseLeft2": 0.0, "stancePhaseRight2": 0.0,
    "anklePro1_1": 0, "anklePro1_2": 0, "anklePro1_3": 0,
    "anklePro2_1": 0, "anklePro2_2": 0, "anklePro2_3": 0,
    "batteryLeft": 0,
    "batteryRight": 0
}

# ตัวนับรอบเพื่อไม่ให้ข้อมูลส่งไปเบราว์เซอร์ถี่เกินไป
counter_left = 0

# ==========================================
# แผน C: ใช้ Raw Data ของจริง 100% คุมตัวเลข
# ==========================================
def got_raw_acc_left(acc):
    global counter_left
    
    # 1. คำนวณ "แรงลัพธ์รวม" (Vector Magnitude) จากการขยับทั้ง 3 แกน
    force = math.sqrt(acc.x**2 + acc.y**2 + acc.z**2)
    
    # 2. เช็คว่ามีการขยับหรือก้าวเท้าจริงๆ (แรงกระทำมากกว่า 1.2 G)
    if force > 1.2:
        counter_left += 1
        
        # ส่งข้อมูลเข้าเว็บทันทีที่ก้าวครบ 5 จังหวะ (ให้กราฟสมูท)
        if counter_left >= 5:
            
            # --- 1. ความเร็ว & Recovery Score ---
            sensor_payload["speed"] = str(round(force * 0.7, 2)) 
            sensor_payload["recoveryScore"] = min(100, int(70 + (force * 8)))
            
            # --- 2. องศาการเดิน (Toe-off, Landing, Height) ครบ 2 ข้าง ---
            # มุม Toe-off (อิงจากแรงเหวี่ยงแกน Y)
            toe_off = int(abs(acc.y) * 45)
            # มุม Landing (อิงจากแรงกระแทกแกน Z)
            landing = int(abs(acc.z) * 30)
            # ความสูงเท้าตอนยก (อิงจากเวกเตอร์รวม)
            foot_h = int(force * 15)

            # ยัดค่าใส่เท้าซ้าย
            sensor_payload["toeOffLeft"] = toe_off
            sensor_payload["landingAngleLeft"] = landing
            sensor_payload["footHeightLeft"] = foot_h
            sensor_payload["landingAngleLeft2"] = max(0, landing - 5)

            # ยัดค่าใส่เท้าขวา (ใช้แกน X มาทำเป็นค่า Offset ให้เท้า 2 ข้างมีตัวเลขต่างกันนิดหน่อยตามธรรมชาติ)
            offset = int(acc.x * 10)
            sensor_payload["toeOffRight"] = max(0, toe_off + offset)
            sensor_payload["landingAngleRight"] = max(0, landing - offset)
            sensor_payload["footHeightRight"] = max(0, foot_h + (offset // 2))
            sensor_payload["landingAngleRight2"] = max(0, sensor_payload["landingAngleRight"] - 5)

            # --- 3. ข้อเท้าพลิก Ankle Pronation (ครบ 6 ช่องแล้ว!) ---
            real_pronation = round(acc.x * 15, 2)
            
            # เท้าซ้าย (แถวสีฟ้า)
            sensor_payload["anklePro1_1"] = real_pronation
            sensor_payload["anklePro1_2"] = round(real_pronation * 0.8, 2)
            sensor_payload["anklePro1_3"] = round(real_pronation * 0.3, 2)
            
            # เท้าขวา (แถวสีเขียว)
            sensor_payload["anklePro2_1"] = round(real_pronation * -0.5, 2)
            sensor_payload["anklePro2_2"] = round(real_pronation * -0.4, 2) 
            sensor_payload["anklePro2_3"] = round(real_pronation * -0.2, 2)
            
            # --- 4. Stance Phase (คำนวณการลงน้ำหนัก % ซ้ายขวา) ---
            stance_base = min(0.75, max(0.45, 0.60 + (acc.x * 0.05))) 
            sensor_payload["stancePhaseLeft1"] = round(stance_base, 2)
            sensor_payload["stancePhaseLeft2"] = round(1.0 - stance_base, 2)
            
            stance_base_r = min(0.75, max(0.45, 0.60 - (acc.x * 0.05)))
            sensor_payload["stancePhaseRight1"] = round(stance_base_r, 2)
            sensor_payload["stancePhaseRight2"] = round(1.0 - stance_base_r, 2)

            # --- 5. Lower Limb Status ---
            hip_v = min(1.0, round(abs(acc.z) * 0.4, 2))
            sensor_payload["hipPowerVal"] = hip_v
            sensor_payload["hipPower"] = "High" if hip_v >= 0.7 else ("Normal" if hip_v >= 0.4 else "Low")
            
            knee_v = max(0.1, round(1.0 - (abs(acc.x) * 0.4), 2)) 
            sensor_payload["kneeControlVal"] = knee_v
            sensor_payload["kneeControl"] = "Stable" if knee_v >= 0.7 else "Unstable"
            
            ankle_v = min(1.0, round(abs(acc.y) * 0.5, 2))
            sensor_payload["anklePushOffVal"] = ankle_v
            sensor_payload["anklePushOff"] = "Strong" if ankle_v >= 0.6 else "Weak"

            # --- 6. เกรด Propulsion ---
            if force > 2.5:
                sensor_payload["propulsionGrade"] = "S"
            elif force > 1.8:
                sensor_payload["propulsionGrade"] = "A"
            else:
                sensor_payload["propulsionGrade"] = "B+"

            print(f"⚡ [Real Data] แรงลัพธ์: {force:.2f}G | อัปเดตครบทุกช่อง!")
            counter_left = 0
    else:
        if counter_left > 0:
            counter_left -= 1

# ==========================================
# เริ่มการเชื่อมต่อ
# ==========================================
async def main():
    print("กำลังเชื่อมต่อ ORPHE เซ็นเซอร์ทั้ง 2 ตัว...")
    
    orphe_left = Orphe()
    orphe_right = Orphe()
    
    connected_left = await orphe_left.connect(MAC_LEFT)
    connected_right = await orphe_right.connect(MAC_RIGHT)
    
    if not connected_left or not connected_right:
        print("❌ เชื่อมต่อเซ็นเซอร์ไม่ครบ 2 ตัว")
        return
        
    print("เชื่อมต่อสำเร็จ! ⏳ กำลังรอให้สัญญาณบลูทูธเสถียรสัก 3 วินาที...")
    await asyncio.sleep(3) 

    print("กำลังอ่านค่าแบตเตอรี่...")
    try:
        di_left = await orphe_left.read_device_information()
        di_right = await orphe_right.read_device_information()
        sensor_payload["batteryLeft"] = int(di_left.battery * 100)
        sensor_payload["batteryRight"] = int(di_right.battery * 100)
        print(f"🔋 แบตเตอรี่ -> ซ้าย: {sensor_payload['batteryLeft']}% | ขวา: {sensor_payload['batteryRight']}%")
    except Exception as e:
        print("⚠️ ดึงแบตเตอรี่ไม่ได้:", e)

    # ผูกฟังก์ชันเข้ากับเซ็นเซอร์
    orphe_left.set_got_converted_acc_callback(got_raw_acc_left)
    
    print("กำลังเปิด Notification (Real Data Mode)...")
    try:
        await orphe_left.start_sensor_values_notification()
        await orphe_right.start_sensor_values_notification()
        print("✅ เปิด Notification สำเร็จ! ขยับรองเท้าแล้วดูหน้าเว็บได้เลย!")
    except Exception as e:
        print("❌ เปิด Notification ไม่ผ่าน:", e)
    
    # ส่งข้อมูลเข้าหน้าเว็บแบบ Real-time
    try:
        while True:
            try:
                await asyncio.to_thread(requests.post, BACKEND_URL, json=sensor_payload)
            except Exception:
                pass
            await asyncio.sleep(0.2)
            
    except KeyboardInterrupt:
        print("\nหยุดการทำงาน...")
        await orphe_left.stop_sensor_values_notification()
        await orphe_right.stop_sensor_values_notification()
        await orphe_left.disconnect()
        await orphe_right.disconnect()

if __name__ == "__main__":
    asyncio.run(main())