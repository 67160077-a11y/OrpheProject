import asyncio
from orphe_core import Orphe

MAC_LEFT = "F4:1B:9B:AF:20:5D"

# ฟังก์ชันรับข้อมูลดิบ (ความเร่ง) ตามโครงสร้างไลบรารีเป๊ะๆ
def got_converted_acc(acc):
    print("🚀 [เซ็นเซอร์ทำงาน!] ", end="")
    acc.print()  # ให้ตัวไลบรารีปริ้นท์ค่าแกน X Y Z ออกมาเองเลย

async def main():
    print("กำลังเชื่อมต่อเซ็นเซอร์ข้างซ้าย...")
    orphe = Orphe()
    
    # เชื่อมต่อกับข้างซ้าย
    if not await orphe.connect(MAC_LEFT):
        print("❌ เชื่อมต่อไม่สำเร็จ")
        return
        
    print("✅ เชื่อมต่อสำเร็จ!")
    
    # 🌟 ผูกฟังก์ชันดึงค่าความเร่งดิบ (คำสั่งที่ถูกต้อง)
    orphe.set_got_converted_acc_callback(got_converted_acc)
    
    # เปิดการรับส่งข้อมูลดิบ
    await orphe.start_sensor_values_notification()
    
    print("🟢 ลองหยิบรองเท้ามาเขย่า หรือแกว่งมือดูเลยครับ! (ตัวเลขต้องวิ่งรัวๆ)")
    
    try:
        while True:
            await asyncio.sleep(1)
            if not orphe.is_connected():
                print("⚠️ สัญญาณบลูทูธหลุด")
                break
    except KeyboardInterrupt:
        print("\nกำลังปิดระบบ...")
    finally:
        if orphe.is_connected():
            await orphe.stop_sensor_values_notification()
            await orphe.disconnect()
            print("ปิดการเชื่อมต่อเรียบร้อย")

if __name__ == "__main__":
    asyncio.run(main())