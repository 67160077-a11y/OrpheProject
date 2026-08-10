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

    <div class="row q-col-gutter-xl">
      <!-- ================= คอลัมน์ซ้าย ================= -->
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
          
          <div class="relative-position flex flex-center q-mb-xl q-mt-md" style="height: 220px;">
            <img :src="legOutlineImg" alt="Leg Outline" style="height: 100%; object-fit: contain;" />
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
      
      <!-- ================= คอลัมน์ขวา ================= -->
      <div class="col-12 col-md-8">
        <div class="row q-col-gutter-lg">
          <!-- Propulsion 4 การ์ด -->
          <div class="col-12 col-sm-6" v-for="i in 4" :key="i">
            <q-card class="figma-card q-pa-lg">
              <div class="row justify-between items-center q-mb-sm">
                <div class="text-weight-bold text-dark text-subtitle1"><q-icon name="directions_run" class="q-mr-xs"/> Propulsion</div>
                <div class="bg-green-1 text-green-8 rounded-borders help-icon text-center">?</div>
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

          <!-- Toe-off Angle Placeholder -->
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

          <!-- ================= Ankle Pronation (ดีไซน์สมบูรณ์แบบตาม Figma) ================= -->
          <div class="col-12 col-sm-6">
            <q-card class="figma-card q-pa-lg full-height">
              
              <!-- หัวการ์ด -->
              <div class="text-weight-bolder text-h5 text-dark q-mb-md" style="letter-spacing: -0.5px;">Ankle Pronation</div>

              <!-- รูปภาพข้อเท้าซ้ายและขวาตรงกลาง -->
              <div class="row justify-around items-center q-mb-md" style="height: 70px;">
                <img :src="ankleLeftImg" style="height: 100%; object-fit: contain;" alt="Ankle Left" />
                <img :src="ankleRightImg" style="height: 100%; object-fit: contain;" alt="Ankle Right" />
              </div>

              <!-- แถวที่ 1: เลข 1 (สีฟ้า จัดกึ่งกลางวงกลมเป๊ะ) พร้อมหลอด 3 ช่อง -->
              <div class="row items-center q-mb-md no-wrap">
                <div class="flex flex-center text-bold text-white shadow-1 custom-badge bg-blue-6 q-mr-md">1</div>
                
                <div class="col row q-col-gutter-sm no-wrap items-center">
                  <!-- ช่องที่ 1 -->
                  <div class="col row items-center no-wrap">
                    <q-linear-progress :value="isConnected ? reportData.anklePro1_1 / 20 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-2"/>
                    <span class="q-ml-xs text-caption text-weight-bold text-dark" style="width: 32px;">{{ isConnected ? reportData.anklePro1_1 + '°' : '' }}</span>
                  </div>
                  <!-- ช่องที่ 2 -->
                  <div class="col row items-center no-wrap">
                    <q-linear-progress :value="isConnected ? reportData.anklePro1_2 / 20 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-2"/>
                    <span class="q-ml-xs text-caption text-weight-bold text-dark" style="width: 32px;">{{ isConnected ? reportData.anklePro1_2 + '°' : '' }}</span>
                  </div>
                  <!-- ช่องที่ 3 -->
                  <div class="col row items-center no-wrap">
                    <q-linear-progress :value="isConnected ? reportData.anklePro1_3 / 20 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-2"/>
                    <span class="q-ml-xs text-caption text-weight-bold text-dark" style="width: 32px;">{{ isConnected ? reportData.anklePro1_3 + '°' : '' }}</span>
                  </div>
                </div>
              </div>

              <!-- แถวที่ 2: เลข 2 (สีเขียว จัดกึ่งกลางวงกลมเป๊ะ) พร้อมหลอด 3 ช่อง -->
              <div class="row items-center no-wrap">
                <div class="flex flex-center text-bold text-white shadow-1 custom-badge bg-green-6 q-mr-md">2</div>
                
                <div class="col row q-col-gutter-sm no-wrap items-center">
                  <!-- ช่องที่ 1 -->
                  <div class="col row items-center no-wrap">
                    <q-linear-progress :value="isConnected ? reportData.anklePro2_1 / 20 : 0" :color="isConnected ? 'green-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-2"/>
                    <span class="q-ml-xs text-caption text-weight-bold text-dark" style="width: 32px;">{{ isConnected ? reportData.anklePro2_1 + '°' : '' }}</span>
                  </div>
                  <!-- ช่องที่ 2 -->
                  <div class="col row items-center no-wrap">
                    <q-linear-progress :value="isConnected ? reportData.anklePro2_2 / 20 : 0" :color="isConnected ? 'green-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-2"/>
                    <span class="q-ml-xs text-caption text-weight-bold text-dark" style="width: 32px;">{{ isConnected ? reportData.anklePro2_2 + '°' : '' }}</span>
                  </div>
                  <!-- ช่องที่ 3 -->
                  <div class="col row items-center no-wrap">
                    <q-linear-progress :value="isConnected ? reportData.anklePro2_3 / 20 : 0" :color="isConnected ? 'green-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-2"/>
                    <span class="q-ml-xs text-caption text-weight-bold text-dark" style="width: 32px;">{{ isConnected ? reportData.anklePro2_3 + '°' : '' }}</span>
                  </div>
                </div>
              </div>
              
            </q-card>
          </div>

          <!-- ================= Stance Phase ================= -->
          <div class="col-12 col-sm-6">
             <q-card class="figma-card q-pa-lg full-height">
               
               <div class="row justify-between items-start q-mb-lg">
                 <div class="text-weight-bolder text-h5 text-dark" style="letter-spacing: -0.5px;">Stance Phase</div>
               </div>

               <div class="row items-center">
                 <!-- ฝั่งซ้าย: หลอดแสดงผล -->
                 <div class="col-9 q-gutter-y-md q-pr-md" style="border-right: 1px solid #eef0f2;">
                   
                   <!-- ครั้งที่ 1: สีน้ำเงิน (Left Foot) -->
                   <div class="row items-center no-wrap">
                     <div class="text-caption text-teal-6 text-weight-bold" style="width: 70px;">Left foot</div>
                     <div class="col row items-center no-wrap">
                       <q-linear-progress :value="isConnected ? reportData.stancePhaseLeft1 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-3"/>
                       <span class="q-ml-sm text-caption text-weight-bold text-dark" style="width: 35px;">
                         {{ isConnected ? Math.round(reportData.stancePhaseLeft1 * 100) + '%' : '' }}
                       </span>
                     </div>
                   </div>
                   
                   <!-- ครั้งที่ 1: สีน้ำเงิน (Right Foot) -->
                   <div class="row items-center no-wrap">
                     <div class="text-caption text-dark text-weight-bold" style="width: 70px;">Right foot</div>
                     <div class="col row items-center no-wrap">
                       <q-linear-progress reverse :value="isConnected ? reportData.stancePhaseRight1 : 0" :color="isConnected ? 'blue-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-3"/>
                       <span class="q-ml-sm text-caption text-weight-bold text-dark" style="width: 35px;">
                         {{ isConnected ? Math.round(reportData.stancePhaseRight1 * 100) + '%' : '' }}
                       </span>
                     </div>
                   </div>

                   <!-- ครั้งที่ 2: สีเขียว (Left Foot) -->
                   <div class="row items-center no-wrap q-mt-lg">
                     <div class="text-caption text-teal-6 text-weight-bold" style="width: 70px;">Left foot</div>
                     <div class="col row items-center no-wrap">
                       <q-linear-progress :value="isConnected ? reportData.stancePhaseLeft2 : 0" :color="isConnected ? 'green-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-3"/>
                       <div class="q-ml-sm" style="width: 35px;"></div>
                     </div>
                   </div>

                   <!-- ครั้งที่ 2: สีเขียว (Right Foot) -->
                   <div class="row items-center no-wrap">
                     <div class="text-caption text-dark text-weight-bold" style="width: 70px;">Right foot</div>
                     <div class="col row items-center no-wrap">
                       <q-linear-progress reverse :value="isConnected ? reportData.stancePhaseRight2 : 0" :color="isConnected ? 'green-6' : 'grey-4'" size="14px" rounded class="col" track-color="grey-3"/>
                       <div class="q-ml-sm" style="width: 35px;"></div>
                     </div>
                   </div>

                 </div>
                 
                 <!-- ฝั่งขวา: รูปไอคอนคนเดิน -->
                 <div class="col-3 flex flex-center">
                   <img :src="walkIconImg" style="height: 80px; object-fit: contain; opacity: 0.6;" alt="Walk Icon" />
                 </div>
               </div>
               
             </q-card>
          </div>

        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Import รูปจากโฟลเดอร์ assets
import legOutlineImg from '../assets/leg-outline.png'
import walkIconImg from '../assets/walk-icon.png'
import ankleLeftImg from '../assets/ankle-left.png'
import ankleRightImg from '../assets/ankle-right.png'

const isConnected = ref(false)
const reportData = ref({
  recoveryScore: 0,
  hipPower: 'improving',
  kneeControl: 'stable',
  anklePushOff: 'weak',
  propulsionGrade: 'A+',
  speed: '1.16',
  
  // Stance Phase 
  stancePhaseLeft1: 0.70,   
  stancePhaseRight1: 0.70,  
  stancePhaseLeft2: 0.35,   
  stancePhaseRight2: 0.40,
  
  // Ankle Pronation (ค่าเริ่มต้นก่อนเชื่อมต่อ)
  anklePro1_1: 0,
  anklePro1_2: 0,
  anklePro1_3: 0,
  anklePro2_1: 0,
  anklePro2_2: 0,
  anklePro2_3: 0
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
      reportData.value = { ...reportData.value, ...data }
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

/* CSS สำหรับจัดเลข 1 และ 2 ให้อยู่กึ่งกลางวงกลมเป๊ะๆ */
.custom-badge {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>