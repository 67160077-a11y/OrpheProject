ORPHEPJ - Smart Shoe Sensor Dashboard
ระบบวิเคราะห์ข้อมูลจากเซ็นเซอร์รองเท้าอัจฉริยะ (ORPHE) แบบ Real-time ที่ประมวลผลข้อมูลผ่าน Backend และแสดงผลผ่านหน้าแดชบอร์ด Quasar

🚀 How to Run (คำสั่งการรันระบบ)
เพื่อให้ระบบทำงานได้ครบถ้วน คุณต้องเปิด Terminal และรันคำสั่งทั้ง 3 ส่วนนี้ในหน้าต่างที่แยกกัน:

install
npm install
pip install -r requirements.txt

1. Backend (FastAPI Server)
ทำหน้าที่รับข้อมูลจากเซ็นเซอร์ คำนวณค่า NCI และส่งข้อมูลผ่าน WebSocket:
cd Backend
python server.py

2. Device Bridge (Sensor Connector)
ทำหน้าที่เชื่อมต่อกับเซ็นเซอร์ Orphe จริง และส่งข้อมูลเข้าสู่ Backend:
python ORPHE-CORE.py/run_real_device.py

3. Frontend (Quasar Dashboard)
ทำหน้าที่แสดงผลแดชบอร์ดบนเบราว์เซอร์:
cd Frontend
npm run dev
