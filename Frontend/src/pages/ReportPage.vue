<template>
  <q-page class="q-pa-xl">
    <!-- แบนเนอร์แจ้งเตือนสถานะการเชื่อมต่อ (เชื่อม / ไม่เชื่อม) -->
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

    <div class="row q-col-gutter-xl">
      <!-- คอลัมน์ซ้าย: Recovery Score และ Lower Limb Status -->
      <div class="col-12 col-md-4 column q-gutter-y-lg">
        <!-- Recovery Score -->
        <q-card class="figma-card q-pa-xl">
          <div class="text-weight-bolder text-h5 q-mb-lg text-dark">Recovery Score</div>
          <div class="row items-center justify-between">
            <div>
              <div :class="isConnected ? 'text-green-6' : 'text-grey-5'">
                <span class="text-weight-bolder" style="font-size: 64px; line-height: 1;">
                  {{ isConnected ? reportData.recoveryScore : '0' }}
                </span>
                <span class="text-grey-5 text-h5 text-weight-bold">/100</span>
              </div>
              <div class="text-weight-bold q-mt-sm" :class="isConnected ? 'text-green-6' : 'text-grey-5'">
                {{ isConnected ? '↑ +6 this week' : 'Default state' }}
              </div>
            </div>
            <div class="relative-position">
              <q-circular-progress 
                :value="isConnected ? reportData.recoveryScore : 0" 
                size="90px" 
                :thickness="0.25" 
                :color="isConnected ? 'green-5' : 'grey-4'" 
                track-color="green-1" 
              />
              <q-icon name="favorite" :color="isConnected ? 'green-5' : 'grey-4'" size="md" class="absolute-center" />
            </div>
          </div>
        </q-card>

        <!-- Lower Limb Status -->
        <q-card class="figma-card q-pa-xl flex-grow-1">
          <div class="text-weight-bolder text-h5 q-mb-md text-dark">Lower Limb Status</div>
          
          <!-- Graphic Placeholder (ยังไม่ใส่รูปตามคำขอ) -->
          <div class="flex flex-center q-mb-xl q-mt-md">
            <div style="height: 180px; width: 100px; border: 2px dashed #ccc; border-radius: 10px;" class="flex flex-center text-grey-5 text-caption text-center">
              [ Graphic ขา ]
            </div>
          </div>
          
          <div class="q-gutter-y-lg">
            <div>
              <div class="row items-center q-mb-sm">
                <div class="icon-circle bg-green-1 q-mr-sm"><q-icon name="north_east" :color="isConnected ? 'green-6' : 'grey-5'" size="xs" /></div>
                <div class="col text-weight-bold text-dark text-subtitle1">Hip Power</div>
                <div :class="isConnected ? 'text-green-6' : 'text-grey-5'" class="text-weight-bold">
                  {{ isConnected ? reportData.hipPower : 'default' }}
                </div>
              </div>
              <q-linear-progress :value="isConnected ? 0.8 : 0" :color="isConnected ? 'green-6' : 'grey-4'" track-color="green-2" rounded size="10px" />
            </div>

            <div>
              <div class="row items-center q-mb-sm">
                <div class="icon-circle bg-blue-1 q-mr-sm"><q-icon name="horizontal_rule" :color="isConnected ? 'blue-6' : 'grey-5'" size="xs" /></div>
                <div class="col text-weight-bold text-dark text-subtitle1">Knee Control</div>
                <div :class="isConnected ? 'text-blue-6' : 'text-grey-5'" class="text-weight-bold">
                  {{ isConnected ? reportData.kneeControl : 'default' }}
                </div>
              </div>
              <q-linear-progress :value="isConnected ? 0.6 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" track-color="blue-2" rounded size="10px" />
            </div>

            <div>
              <div class="row items-center q-mb-sm">
                <div class="icon-circle bg-orange-1 q-mr-sm"><q-icon name="south_east" :color="isConnected ? 'orange-6' : 'grey-5'" size="xs" /></div>
                <div class="col text-weight-bold text-dark text-subtitle1">Ankle Push-off</div>
                <div :class="isConnected ? 'text-orange-6' : 'text-grey-5'" class="text-weight-bold">
                  {{ isConnected ? reportData.anklePushOff : 'default' }}
                </div>
              </div>
              <q-linear-progress :value="isConnected ? 0.3 : 0" :color="isConnected ? 'orange-6' : 'grey-4'" track-color="orange-2" rounded size="10px" />
            </div>
          </div>
        </q-card>
      </div>
      
      <!-- คอลัมน์ขวา: กราฟและข้อมูลการวิเคราะห์ -->
      <div class="col-12 col-md-8">
        <div class="row q-col-gutter-lg">
          <!-- Propulsion 4 การ์ด -->
          <div class="col-12 col-sm-6" v-for="i in 4" :key="i">
            <q-card class="figma-card q-pa-lg">
              <div class="row justify-between items-center q-mb-sm">
                <div class="text-weight-bold text-dark text-subtitle1"><q-icon name="directions_run" class="q-mr-xs"/> Propulsion</div>
                <div class="bg-green-1 text-green-8 rounded-borders" style="width:20px; height:20px; text-align:center; font-weight:bold; font-size:12px; line-height:20px;">?</div>
              </div>
              <div class="row justify-between items-end q-mb-md">
                <div :class="isConnected ? 'text-blue-6' : 'text-grey-5'" style="font-size: 64px; font-weight: 800; line-height: 1;">
                  {{ isConnected ? reportData.propulsionGrade : '-' }}
                </div>
                <div class="text-caption text-right">
                  <div class="text-dark text-weight-bold"><div class="dot-indicator bg-blue-6"></div>ครั้งที่ 1</div>
                  <div class="text-dark text-weight-bold q-mt-xs"><div class="dot-indicator bg-green-6"></div>ครั้งที่ 2</div>
                </div>
              </div>
              <div class="text-right text-caption text-blue-6 text-weight-bold q-mb-xs">
                {{ isConnected ? reportData.speed + 'm/s ▼' : '0.00m/s' }}
              </div>
              <div class="gradient-bar" :style="isConnected ? '' : 'filter: grayscale(100%); opacity: 0.3;'">
                <div v-if="isConnected" class="triangle-marker"></div>
              </div>
              <div class="row justify-between text-grey-7 text-weight-bold q-px-sm" style="font-size: 11px; margin-top: -14px; pointer-events: none; position:relative; z-index: 1;">
                <span>ช้า</span><span>เร็ว</span>
              </div>
            </q-card>
          </div>

          <!-- Toe-off Angle (Left & Right) -->
          <div class="col-12 col-sm-6" v-for="(side, index) in ['Left foot', 'Right foot']" :key="'toe'+index">
             <q-card class="figma-card q-pa-lg full-height">
               <div class="text-weight-bold text-dark q-mb-md">Toe-off Angle, Foot Height, Landing Angle <br><span class="text-green-6 text-caption">{{side}}</span></div>
               <div class="row q-col-gutter-sm items-center q-mb-sm">
                 <div class="col-1"><div class="bg-blue-6" style="width:12px; height:12px; border-radius:2px;"></div></div>
                 <div class="col-3 text-caption">{{ isConnected ? '65.9°' : '0.0°' }}</div>
                 <div class="col-4"><q-linear-progress :value="isConnected ? 0.7 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" rounded /></div>
                 <div class="col-4 text-right text-caption">{{ isConnected ? '21.1°' : '0.0°' }}</div>
               </div>
               <div class="row q-col-gutter-sm items-center">
                 <div class="col-1"><div class="bg-green-6" style="width:12px; height:12px; border-radius:2px;"></div></div>
                 <div class="col-3 text-caption">{{ isConnected ? '51.5°' : '0.0°' }}</div>
                 <div class="col-4"><q-linear-progress :value="isConnected ? 0.5 : 0" :color="isConnected ? 'green-6' : 'grey-4'" rounded /></div>
                 <div class="col-4 text-right text-caption">{{ isConnected ? '6.8°' : '0.0°' }}</div>
               </div>
             </q-card>
          </div>

          <!-- Ankle Pronation -->
          <div class="col-12 col-sm-6">
            <q-card class="figma-card q-pa-lg">
              <div class="text-weight-bold text-dark q-mb-md">Ankle Pronation</div>
              <div class="row items-center q-mb-sm">
                <div class="col-2 text-caption">1</div>
                <div class="col-3 text-caption">{{ isConnected ? '7.3°' : '0.0°' }}</div>
                <div class="col-4"><q-linear-progress :value="isConnected ? 0.6 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" rounded /></div>
                <div class="col-3 text-right text-caption">{{ isConnected ? '11.6°' : '0.0°' }}</div>
              </div>
              <div class="row items-center">
                <div class="col-2 text-caption">2</div>
                <div class="col-3 text-caption">{{ isConnected ? '4.3°' : '0.0°' }}</div>
                <div class="col-4"><q-linear-progress :value="isConnected ? 0.4 : 0" :color="isConnected ? 'green-6' : 'grey-4'" rounded /></div>
                <div class="col-3 text-right text-caption">{{ isConnected ? '9.0°' : '0.0°' }}</div>
              </div>
            </q-card>
          </div>

          <!-- Stance Phase -->
          <div class="col-12 col-sm-6">
             <q-card class="figma-card q-pa-lg">
               <div class="text-weight-bold text-dark q-mb-md">Stance Phase</div>
               <div class="row items-center q-mb-sm"><div class="col-4 text-caption">Left foot</div><div class="col-8"><q-linear-progress :value="isConnected ? 0.7 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" rounded /></div></div>
               <div class="row items-center q-mb-sm"><div class="col-4 text-caption">Right foot</div><div class="col-8"><q-linear-progress :value="isConnected ? 0.7 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" rounded /></div></div>
             </q-card>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isConnected = ref(false)
const reportData = ref({
  recoveryScore: 0,
  hipPower: 'default',
  kneeControl: 'default',
  anklePushOff: 'default',
  propulsionGrade: '-',
  speed: '0.00'
})

let socket = null

onMounted(() => {
  // เชื่อมต่อ WebSocket ไปยัง Python Backend (FastAPI)
  socket = new WebSocket('ws://localhost:8765/ws')

  socket.onopen = () => {
    isConnected.value = true
  }

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      reportData.value = data
      isConnected.value = true
    } catch (e) {
      console.error('Error parsing real-time data:', e)
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
.figma-card { border: 1px solid #eef0f2; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); }
.icon-circle { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.dot-indicator { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
.gradient-bar { background: linear-gradient(90deg, #f44336 0%, #ff9800 50%, #4caf50 100%); border-radius: 12px; height: 16px; position: relative; width: 100%; }
.triangle-marker { position: absolute; top: -8px; left: 70%; width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid #1e88e5; }
.border-orange { border: 1px solid #ffb74d; }
.border-green { border: 1px solid #81c784; }
</style>