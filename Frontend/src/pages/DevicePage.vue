<template>
  <q-page class="q-pa-xl">
    <!-- แบนเนอร์แจ้งเตือนสถานะการเชื่อมต่อ -->
    <q-banner :class="isConnected ? 'bg-green-1 text-green-9 border-green' : 'bg-orange-1 text-orange-9 border-orange'" class="q-mb-lg rounded-borders">
      <template v-slot:avatar>
        <q-icon :name="isConnected ? 'check_circle' : 'warning'" :color="isConnected ? 'green' : 'orange'" />
      </template>
      <div class="text-weight-bold">
        สถานะอุปกรณ์:
        <span v-if="isConnected">เชื่อมต่อสำเร็จ (Device Connected - แสดงข้อมูล Real-time)</span>
        <span v-else>ยังไม่ได้เชื่อมต่ออุปกรณ์ (Device Disconnected - แสดงค่าเริ่มต้นทั้งหมด)</span>
      </div>
    </q-banner>

    <div class="text-subtitle1 text-weight-bolder q-mb-lg text-uppercase text-dark" style="letter-spacing: 0.5px;">ORPHE CORE DETAILS</div>

    <div class="row q-col-gutter-xl">
      <!-- ซ้าย: ส่วนรูปภาพประกอบ -->
      <div class="col-12 col-md-9">
        <q-card class="figma-card full-height bg-white relative-position" style="min-height: 550px;">
          <div class="device-diagram-wrapper">
            <div class="image-container">
              <img src="@/assets/Devicephoto.png" alt="Orphe Core Device" class="device-image" />

              <!-- ฝาครอบด้านบน -->
              <div class="label-item label-left" style="top: 18%;">
                <div class="label-text text-right">ฝาครอบด้านบน<br/>( Top Cover )</div>
                <div class="label-line"></div>
              </div>

              <!-- กรอบตรงกลาง -->
              <div class="label-item label-right" style="top: 30%;">
                <div class="label-line"></div>
                <div class="label-text text-left">กรอบตรงกลาง<br/>(Mid-Frame / Gasket)</div>
              </div>

              <!-- แผงวงจรหลัก -->
              <div class="label-item label-left" style="top: 44%;">
                <div class="label-text text-right">แผงวงจรหลัก<br/>( mainPCB ASSEMBLY )</div>
                <div class="label-line"></div>
              </div>

              <!-- โมดูลแบตเตอรี่ -->
              <div class="label-item label-right" style="top: 62%;">
                <div class="label-line"></div>
                <div class="label-text text-left">โมดูลแบตเตอรี่<br/>(Battery Module)</div>
              </div>

              <!-- พอร์ต -->
              <div class="label-item label-left" style="top: 80%;">
                <div class="label-text text-right">แผงวงจรพอร์ตและขั้วต่อ<br/>(Port &amp; Connector PCB)</div>
                <div class="label-line"></div>
              </div>

              <!-- เคสฐาน -->
              <div class="label-item label-right" style="top: 80%;">
                <div class="label-line"></div>
                <div class="label-text text-left">เคสฐานด้านล่าง<br/>(Bottom Base Case)</div>
              </div>
            </div>
          </div>
        </q-card>
      </div>

      <!-- ขวา: แบตเตอรี่ และ สถานะการเชื่อมต่อ -->
      <div class="col-12 col-md-3 column q-gutter-y-lg">

        <!-- แบตเตอรี่ซ้าย (Machine L) -->
        <q-card class="figma-card q-pa-lg text-center">
          <div class="text-weight-bold text-subtitle1 q-mb-md text-dark">Battery Status</div>
          <q-circular-progress show-value :value="isConnected ? deviceData.batteryLeft : 0" size="110px" :thickness="0.12" :color="isConnected ? (deviceData.batteryLeft < 20 ? 'orange-6' : 'green-7') : 'grey-4'" track-color="green-1" class="q-mb-md text-h5 text-weight-bolder text-dark">
            {{ isConnected ? deviceData.batteryLeft + '%' : '--' }}
          </q-circular-progress>

          <div class="row justify-between items-center text-caption text-weight-bold q-mb-sm">
            <span class="text-dark">Machine L (Left)</span>
            <span :class="isConnected ? (deviceData.batteryLeft < 20 ? 'text-orange-6' : 'text-green-6') : 'text-grey-5'">
              {{ isConnected ? (deviceData.batteryLeft < 20 ? 'Low' : 'Good') : 'Default' }}
            </span>
          </div>

          <q-linear-progress :value="isConnected ? deviceData.batteryLeft / 100 : 0" :color="isConnected ? (deviceData.batteryLeft < 20 ? 'orange-6' : 'green-6') : 'grey-4'" track-color="grey-2" rounded size="6px" />
        </q-card>

        <!-- แบตเตอรี่ขวา (Machine R) -->
        <q-card class="figma-card q-pa-lg text-center">
          <div class="text-weight-bold text-subtitle1 q-mb-md text-dark">Battery Status</div>
          <q-circular-progress show-value :value="isConnected ? deviceData.batteryRight : 0" size="110px" :thickness="0.12" :color="isConnected ? (deviceData.batteryRight < 20 ? 'orange-6' : 'green-7') : 'grey-4'" track-color="green-1" class="q-mb-md text-h5 text-weight-bolder text-dark">
            {{ isConnected ? deviceData.batteryRight + '%' : '--' }}
          </q-circular-progress>

          <div class="row justify-between items-center text-caption text-weight-bold q-mb-sm">
            <span class="text-dark">Machine R (Right)</span>
            <span :class="isConnected ? (deviceData.batteryRight < 20 ? 'text-orange-6' : 'text-green-6') : 'text-grey-5'">
              {{ isConnected ? (deviceData.batteryRight < 20 ? 'Low' : 'Good') : 'Default' }}
            </span>
          </div>

          <q-linear-progress :value="isConnected ? deviceData.batteryRight / 100 : 0" :color="isConnected ? (deviceData.batteryRight < 20 ? 'orange-6' : 'green-6') : 'grey-4'" track-color="grey-2" rounded size="6px" />
        </q-card>

        <!-- สถานะการเชื่อมต่อ -->
        <q-card class="figma-card q-pa-lg text-center flex-grow-1">
          <div class="text-weight-bold text-subtitle1 q-mb-md text-dark">สถานะการเชื่อมต่อ</div>
          <div :class="isConnected ? 'bg-green-1' : 'bg-grey-2'" class="flex flex-center q-mx-auto q-mb-md" style="width: 70px; height: 70px; border-radius: 50%;">
             <q-icon name="power" size="36px" :color="isConnected ? 'green-7' : 'grey-5'" />
          </div>
          <div :class="isConnected ? 'text-green-7' : 'text-grey-6'" class="text-weight-bolder text-h6 q-mb-xs">
            {{ isConnected ? 'Connected' : 'Disconnected' }}
          </div>
          <div class="text-grey-6 text-caption text-weight-bold">
            {{ isConnected ? 'เชื่อมต่อแล้ว' : 'ยังไม่ได้เชื่อมต่อ' }}
          </div>
        </q-card>

      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isConnected = ref(false)
const deviceData = ref({
  batteryLeft: 0,
  batteryRight: 0
})

let socket = null

onMounted(() => {
  socket = new WebSocket('ws://localhost:8765/ws')

  socket.onopen = () => {
    isConnected.value = true
  }

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      deviceData.value.batteryLeft = data.batteryLeft || 0
      deviceData.value.batteryRight = data.batteryRight || 0
      isConnected.value = true
    } catch (e) {
      console.error('Error parsing device data:', e)
    }
  }

  socket.onclose = () => {
    isConnected.value = false
  }

  socket.onerror = () => {
    isConnected.value = false
  }
})

onUnmounted(() => {
  if (socket) socket.close()
})
</script>

<style scoped>
.figma-card {
  border: 1px solid #eef0f2;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}
.border-orange { border: 1px solid #ffb74d; }
.border-green { border: 1px solid #81c784; }

.device-diagram-wrapper {
  width: 100%;
  height: 100%;
  min-height: 600px; /* เพิ่มความสูงขั้นต่ำให้รับกับรูปที่ใหญ่ขึ้น */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  overflow-x: auto; 
}

.image-container {
  position: relative;
  /* 🌟 ขยายขนาดรูปให้ใหญ่ขึ้นมากสุดที่ 500px (จากเดิม 350px) */
  width: clamp(250px, 45vw, 500px); 
  aspect-ratio: 1 / 1;
  /* ขอบซ้ายขวาสำหรับวางตัวหนังสือ ยืดหยุ่นตามขนาดจอ */
  margin: 0 clamp(100px, 12vw, 160px); 
}

.device-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.label-item {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 6px;
  width: max-content;
  max-width: 160px; /* ขยายกรอบตัวหนังสือให้ยาวขึ้นนิดนึง */
}

.label-left {
  right: 100%; 
  justify-content: flex-end;
}

.label-right {
  left: 100%; 
}

.label-text {
  font-size: clamp(11px, 1.2vw, 14px); /* 🌟 ขยายฟอนต์ให้ใหญ่ขึ้นตามรูป */
  font-weight: 700;
  color: #2d2d2d;
  line-height: 1.3;
}
.label-left .label-text { text-align: right; }
.label-right .label-text { text-align: left; }

.label-line {
  height: 1px;
  background-color: #444;
  width: clamp(20px, 4vw, 50px); /* ยืดเส้นชี้ให้ยาวขึ้นสมดุลกับจอ */
  flex-shrink: 0;
  position: relative;
}

.label-left .label-line::after,
.label-right .label-line::before {
  content: '';
  position: absolute;
  top: -3px;
  width: 0; height: 0;
  border-top: 3px solid transparent;
  border-bottom: 3px solid transparent;
}

.label-left .label-line::after {
  right: -1px;
  border-left: 5px solid #444;
}

.label-right .label-line::before {
  left: -1px;
  border-right: 5px solid #444;
}

/* =========================================
   Media Query: ปรับอัตโนมัติสำหรับมือถือ/แท็บเล็ต 
   ========================================= */
@media (max-width: 768px) {
  .image-container {
    margin: 0 90px; 
  }
  .device-diagram-wrapper {
    min-height: 400px;
  }
}
</style>