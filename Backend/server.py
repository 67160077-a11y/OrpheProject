from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import asyncio

app = FastAPI()

# ==========================================
# 1. เพิ่มฟังก์ชันคำนวณ nCI (Normalized Circular Index) ตรงนี้
# ==========================================
def calculate_nci(data_points):
    """
    ฟังก์ชันคำนวณสูตร nCI จากชุดพิกัด x, y
    ตัวอย่าง data_points: [[1.0, 2.0], [2.5, 4.1], [4.0, 5.5]]
    """
    n = len(data_points)
    if n < 2:
        return 0.0  # ถ้าจุดน้อยกว่า 2 จุด คำนวณความชันไม่ได้
    
    ci = 0.0
    for i in range(n - 1):
        x1, y1 = data_points[i]
        x2, y2 = data_points[i+1]
        
        # ป้องกัน error กรณีหารด้วย 0 (พิกัด x ทับกัน)
        if (x2 - x1) == 0:
            continue
            
        mi = (y2 - y1) / (x2 - x1) # หาความชัน
        ci += mi # นำมารวมกัน (Summation)
        
    nci = ci / (n - 1) # หารด้วยจำนวนจุด - 1
    return nci


# ตัวเก็บข้อมูลล่าสุดแบบ Real-time
latest_data = {
    "recoveryScore": 69,
    "hipPower": "improving",
    "kneeControl": "stable",
    "anklePushOff": "weak",
    "propulsionGrade": "A+",
    "speed": "1.16",
    "nciValue": 0.0  # เพิ่มตัวแปรมารอรับค่า nCI
}

connected_clients = []

# ==========================================
# 2. API สำหรับรับข้อมูลจากอุปกรณ์ (Device / Bridge)
# ==========================================
@app.post("/update-data")
async def receive_data(data: dict):
    global latest_data
    
    # สมมติว่า Device ของคุณส่ง key ที่ชื่อว่า "coordinates" ซึ่งมีพิกัด [x, y] มาด้วย
    # เช่น {"coordinates": [[1.2, 3.4], [2.0, 4.1], [3.5, 5.0]], "recoveryScore": 80, ...}
    if "coordinates" in data:
        # ดึงชุดข้อมูลพิกัดไปคำนวณผ่านสูตร nCI
        nci_result = calculate_nci(data["coordinates"])
        
        # นำค่าที่คำนวณเสร็จแล้ว ยัดกลับเข้าไปในชุดข้อมูล (ปัดเศษ 2 ตำแหน่ง)
        data["nciValue"] = round(nci_result, 2)
    
    latest_data = data # อัปเดตข้อมูลใหม่ทันที
    
    # ส่งข้อมูลใหม่กระจายไปให้หน้าเว็บทุกจอที่เปิดอยู่ทันทีแบบ Real-time
    for client in connected_clients:
        try:
            await client.send_json(latest_data)
        except:
            pass
            
    return {"status": "success", "message": "Data updated and nCI calculated"}

# ==========================================
# 3. WebSocket สำหรับส่งข้อมูลให้หน้าเว็บ Frontend (Quasar)
# ==========================================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print("Frontend connected!")
    
    try:
        # ส่งข้อมูลล่าสุดให้ทันทีที่หน้าเว็บเชื่อมต่อเข้ามา
        await websocket.send_json(latest_data)
        
        while True:
            # เปิดช่องสัญญาณเชื่อมต่อค้างไว้รอรับ/ส่งข้อมูลแบบ Real-time
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("Frontend disconnected!")

if __name__ == "__main__":
    # รันเซิร์ฟเวอร์ที่พอร์ต 8765
    uvicorn.run(app, host="localhost", port=8765)