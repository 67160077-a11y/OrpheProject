<template>
  <div class="login-wrapper flex flex-center">
    <div class="logo-header text-center q-mb-md">
      <div class="row justify-center items-center">
        <div class="logo-box flex flex-center q-mr-sm">
          <q-icon name="insights" size="20px" color="white" />
        </div>
        <div class="text-h4 text-weight-bold text-dark" style="letter-spacing: -0.5px;">Orphe</div>
      </div>
    </div>

    <div class="login-card shadow-3 bg-white">
      <div class="text-center q-mb-xl">
        <div class="text-h5 text-weight-bold text-dark" style="font-size: 24px;">
          {{ isSignUpMode ? 'Create an Account' : 'Welcome to Orphe' }}
        </div>
      </div>

      <q-form @submit.prevent="handleSubmit" class="q-gutter-y-md">
        <!-- Name Field (โชว์เฉพาะตอน Sign Up) -->
        <div v-if="isSignUpMode">
          <div class="text-weight-bold text-dark q-mb-xs" style="font-size: 13px;">Full Name</div>
          <q-input outlined rounded dense v-model="formName" placeholder="Enter your name" class="custom-input" hide-bottom-space required />
        </div>

        <!-- Email Field -->
        <div>
          <div class="text-weight-bold text-dark q-mb-xs" style="font-size: 13px;">Email Address</div>
          <q-input outlined rounded dense v-model="formEmail" placeholder="Enter your email" class="custom-input" hide-bottom-space required />
        </div>

        <!-- Password Field -->
        <div>
          <div class="text-weight-bold text-dark q-mb-xs" style="font-size: 13px;">Password</div>
          <q-input outlined rounded dense type="password" v-model="formPassword" placeholder="Enter your password" class="custom-input" hide-bottom-space required />
          <div class="text-right q-mt-xs" v-if="!isSignUpMode">
            <a href="#" class="text-grey-5 text-caption text-weight-medium" style="text-decoration: none;">Forgot Password ?</a>
          </div>
        </div>

        <!-- Submit Button -->
        <q-btn 
          unelevated rounded class="full-width q-py-sm q-mt-sm text-weight-bold" 
          type="submit" 
          :label="isSignUpMode ? 'Sign Up' : 'Sign In'" 
          style="background-color: #21963f; color: white; font-size: 15px; text-transform: none;"
        />

        <!-- Toggle Switch ระหว่าง Login กับ Sign Up -->
        <div class="text-center q-mt-md">
          <span class="text-grey-7" style="font-size: 13px;">
            {{ isSignUpMode ? 'Already have an account?' : "Don't have an account?" }} 
            <span class="text-primary text-weight-bold cursor-pointer" @click="isSignUpMode = !isSignUpMode">
              {{ isSignUpMode ? 'Sign In' : 'Sign Up' }}
            </span>
          </span>
        </div>
      </q-form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isSignUpMode = ref(false)

// ตัวแปรเก็บค่าฟอร์ม
const formName = ref('')
const formEmail = ref('admin@gmail.com')
const formPassword = ref('admin123')

// ข้อมูลเริ่มต้นสำหรับระบบ
const initializeDB = () => {
  const existingUsers = localStorage.getItem('appUsers')
  if (!existingUsers) {
    const defaultUsers = [
      { email: 'admin@gmail.com', password: 'admin123', name: 'System Admin', avatar: 'https://cdn.quasar.dev/img/avatar4.jpg', role: 'admin' },
      { email: 'user@gmail.com', password: '1234', name: 'Matasit Udomtanaput', avatar: 'https://i.pravatar.cc/150?img=47', role: 'user' }
    ]
    localStorage.setItem('appUsers', JSON.stringify(defaultUsers))
  }
}

onMounted(() => {
  initializeDB() // สร้าง DB จำลองเมื่อหน้าเว็บโหลด
})

const handleSubmit = () => {
  const usersDB = JSON.parse(localStorage.getItem('appUsers')) || []

  if (isSignUpMode.value) {
    // ---------------- SIGN UP LOGIC ----------------
    const userExists = usersDB.find(u => u.email === formEmail.value)
    if (userExists) {
      alert('อีเมลนี้ถูกใช้งานไปแล้ว!')
      return
    }
    // สร้าง User ใหม่ (ค่าเริ่มต้นเป็น User ธรรมดา และให้สุ่มรูปโปรไฟล์)
    const newUser = {
      email: formEmail.value,
      password: formPassword.value,
      name: formName.value,
      avatar: `https://i.pravatar.cc/150?u=${formEmail.value}`, // สุ่มรูป
      role: 'user' 
    }
    usersDB.push(newUser)
    localStorage.setItem('appUsers', JSON.stringify(usersDB))
    alert('สร้างบัญชีสำเร็จ! กรุณาเข้าสู่ระบบ')
    isSignUpMode.value = false // สลับกลับไปหน้า Login
  } 
  else {
    // ---------------- SIGN IN LOGIC ----------------
    const validUser = usersDB.find(u => u.email === formEmail.value && u.password === formPassword.value)
    if (validUser) {
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('user', JSON.stringify(validUser)) // เก็บ session
      router.push('/device')
    } else {
      alert('อีเมลหรือรหัสผ่านไม่ถูกต้อง!')
    }
  }
}
</script>

<style scoped>
/* พื้นหลังและลายน้ำ */
.login-wrapper {
  min-height: 100vh;
  width: 100vw;
  flex-direction: column;
  background-color: #eef1f5;
  background-image: radial-gradient(circle, #e2e6eb 1px, transparent 1px);
  background-size: 24px 24px;
}
/* โลโก้ด้านบน */
.logo-box { background-color: #21963f; border-radius: 8px; width: 32px; height: 32px; }
/* กล่องการ์ด */
.login-card { width: 100%; max-width: 440px; border-radius: 20px; padding: 45px 36px; border: 1px solid #e2e6eb; }
/* Input */
.custom-input :deep(.q-field__control) { border-radius: 30px !important; border-color: #dcdcdc; }
</style>