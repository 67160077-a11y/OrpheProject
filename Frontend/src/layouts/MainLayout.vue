<template>
  <q-layout view="lHh Lpr lFf" class="bg-grey-2">
    <q-header class="bg-white text-dark" style="border-bottom: 1px solid #e0e0e0;">
      <q-toolbar class="q-px-lg q-py-sm">
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" color="grey-8" />
        <q-toolbar-title class="text-weight-bolder text-subtitle1 q-ml-md">{{ route.name }}</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above class="bg-grey-1 column justify-between" :width="280">
      <div>
        <div class="q-pa-lg row items-center">
          <div class="logo-box flex flex-center q-mr-sm"><q-icon name="insights" size="20px" color="white" /></div>
          <div class="text-h6 text-weight-bolder">Orphe</div>
        </div>
        <div class="q-px-md q-mt-lg">
          <div class="text-grey-6 text-caption text-weight-bold q-mb-md text-uppercase">Main Menu</div>
          <q-item clickable to="/device" class="menu-pill q-mb-md" active-class="menu-active" exact>
            <q-item-section avatar><q-icon name="explore" size="sm" /></q-item-section>
            <q-item-section class="text-weight-bold">Device</q-item-section>
            <q-item-section side><div class="dot-indicator"></div></q-item-section>
          </q-item>
          <q-item clickable to="/report" class="menu-pill" active-class="menu-active" exact>
            <q-item-section avatar><q-icon name="assessment" size="sm" /></q-item-section>
            <q-item-section class="text-weight-bold">Report</q-item-section>
            <q-item-section side><div class="dot-indicator"></div></q-item-section>
          </q-item>
        </div>
      </div>
      
      <!-- ส่วนแสดงโปรไฟล์ตามผู้ใช้ที่ Login -->
      <div class="q-pa-md" style="border-top: 1px solid #e0e0e0;">
        <!-- เอา clickable และ @click ออกจากตรงนี้ เพื่อไม่ให้กดที่ชื่อแล้ว Log out -->
        <q-item class="rounded-borders q-px-sm">
          <q-item-section avatar>
            <q-avatar size="36px">
              <!-- ใช้รูป Placeholder ไปก่อน -->
              <img src="https://cdn.quasar.dev/img/avatar.png">
            </q-avatar>
          </q-item-section>
          
          <q-item-section>
            <q-item-label class="text-weight-bold">{{ userProfile.name }}</q-item-label>
          </q-item-section>
          
          <!-- เปลี่ยนไอคอนเป็นปุ่มที่กดได้ และย้ายคำสั่ง Log out มาไว้ตรงนี้แทน -->
          <q-item-section side>
            <q-btn flat round dense icon="logout" color="red" @click="logout" />
          </q-item-section>
        </q-item>
      </div>
    </q-drawer>

    <q-page-container><router-view /></q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const leftDrawerOpen = ref(true)
const router = useRouter()
const route = useRoute()

// กำหนดค่าเริ่มต้นเป็น Guest
const userProfile = ref({
  name: 'Guest User',
  avatar: ''
})

// ดึงข้อมูล User จาก localStorage เมื่อเปิดหน้าเว็บ
onMounted(() => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    try {
      userProfile.value = JSON.parse(savedUser)
    } catch (e) {
      console.error('Failed to parse user data', e)
    }
  }
})

const logout = () => { 
  localStorage.removeItem('isLoggedIn')
  localStorage.removeItem('user')
  router.push('/login') 
}
</script>

<style scoped>
.logo-box { background-color: #2ea33c; border-radius: 8px; width: 32px; height: 32px; }
.menu-pill { border-radius: 12px; padding: 12px 16px; background-color: #9ba4b5; color: white !important; }
.menu-active { background-color: #2ea33c !important; }
.dot-indicator { width: 6px; height: 6px; border-radius: 50%; background: #42a5f5; }
</style>