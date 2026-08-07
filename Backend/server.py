from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import asyncio

app = FastAPI()

# ตัวเก็บข้อมูลล่าสุดแบบ Real-time (ไม่มี Database ใช้ตัวแปรนี้เก็บบน RAM ชั่วคราว)
latest_data = {
    "recoveryScore": 69,
    "hipPower": "improving",
    "kneeControl": "stable",
    "anklePushOff": "weak",
    "propulsionGrade": "A+",
    "speed": "1.16"
}

# รายชื่อหน้าเว็บที่เชื่อมต่อเข้ามาทาง WebSocket
connected_clients = []

# 1. API สำหรับรับข้อมูลจากอุปกรณ์ (Device / Bridge ส่งค่าเข้ามาที่นี่)
@app.post("/update-data")
async def receive_data(data: dict):
    global latest_data
    latest_data = data # อัปเดตข้อมูลใหม่ทันที
    
    # ส่งข้อมูลใหม่กระจายไปให้หน้าเว็บทุกจอที่เปิดอยู่ทันทีแบบ Real-time
    for client in connected_clients:
        try:
            await client.send_json(latest_data)
        except:
            pass
            
    return {"status": "success", "message": "Data updated"}

# 2. WebSocket สำหรับส่งข้อมูลให้หน้าเว็บ Frontend (Quasar)
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