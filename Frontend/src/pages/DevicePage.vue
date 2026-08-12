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
      <!-- ซ้าย: ส่วนรูปภาพประกอบ (ยังไม่ใส่รูป ตามคำขอ) -->
      <div class="col-12 col-md-9">
        <q-card class="figma-card full-height flex flex-center bg-white" style="min-height: 550px;">
           <div class="text-center text-grey-5">
             <q-icon name="view_in_ar" size="64px" class="q-mb-sm" />
             <div class="text-h6">[ ส่วนประกอบ Device - ยังไม่ใส่รูปภาพ ]</div>
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
</style>