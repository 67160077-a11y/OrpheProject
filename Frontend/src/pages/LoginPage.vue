<template>
  <div class="login-wrapper flex flex-center">
    <!-- ส่วนหัว Logo ด้านบนการ์ด -->
    <div class="logo-header text-center q-mb-md">
      <div class="row justify-center items-center">
        <div class="logo-box flex flex-center q-mr-sm">
          <q-icon name="insights" size="20px" color="white" />
        </div>
        <div class="text-h4 text-weight-bold text-dark" style="letter-spacing: -0.5px;">Orphe</div>
      </div>
    </div>

    <!-- กล่อง Login Card สีขาว -->
    <div class="login-card shadow-3 bg-white">
      <div class="text-center q-mb-xl">
        <div class="text-h5 text-weight-bold text-dark" style="font-size: 24px;">Welcome to Orphe</div>
      </div>

      <q-form @submit.prevent="handleLogin" class="q-gutter-y-md">
        <!-- Email Field -->
        <div>
          <div class="text-weight-bold text-dark q-mb-xs" style="font-size: 13px;">Email Address</div>
          <q-input 
            outlined 
            rounded 
            dense 
            v-model="email" 
            placeholder="Enter your email" 
            class="custom-input bg-white" 
            hide-bottom-space 
          />
        </div>

        <!-- Password Field -->
        <div>
          <div class="text-weight-bold text-dark q-mb-xs" style="font-size: 13px;">Password</div>
          <q-input 
            outlined 
            rounded 
            dense 
            type="password" 
            v-model="password" 
            placeholder="Enter your password" 
            class="custom-input bg-white" 
            hide-bottom-space 
          />
          <div class="text-right q-mt-xs">
            <a href="#" class="text-grey-5 text-caption text-weight-medium" style="text-decoration: none; font-size: 12px;">Forgot Password ?</a>
          </div>
        </div>

        <!-- Sign In Button -->
        <q-btn 
          unelevated 
          rounded 
          class="full-width q-py-sm q-mt-sm text-weight-bold" 
          type="submit" 
          label="Sign In" 
          style="background-color: #21963f; color: white; font-size: 15px; text-transform: none;"
        />

        <!-- Divider: or sign in with: -->
        <div class="row items-center q-my-lg">
          <q-separator class="col" style="background-color: #dcdcdc;" />
          <div class="col-auto q-px-md text-weight-bold text-dark" style="font-size: 13px;">or sign in with:</div>
          <q-separator class="col" style="background-color: #dcdcdc;" />
        </div>

        <!-- Social Icons (Google, Microsoft, Apple) -->
        <div class="row justify-center q-gutter-x-md q-pb-sm">
          <div class="social-btn">
            <img src="https://cdn-icons-png.flaticon.com/512/2991/2991148.png" width="22" />
          </div>
          <div class="social-btn">
            <img src="https://cdn-icons-png.flaticon.com/512/732/732221.png" width="20" />
          </div>
          <div class="social-btn">
            <img src="https://cdn-icons-png.flaticon.com/512/0/747.png" width="22" />
          </div>
        </div>
      </q-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('admin1234@gmail.com')
const password = ref('1234')

const handleLogin = () => {
  if (email.value === 'admin1234@gmail.com' && password.value === '1234') {
    localStorage.setItem('isLoggedIn', 'true')
    router.push('/device')
  } else {
    alert('รหัสผ่านไม่ถูกต้อง! กรุณาใช้ admin1234@gmail.com / 1234')
  }
}
</script>

<style scoped>
/* พื้นหลังและลายน้ำคนวิ่งจำลอง */
.login-wrapper {
  min-height: 100vh;
  width: 100vw;
  flex-direction: column;
  background-color: #eef1f5;
  background-image: radial-gradient(circle, #e2e6eb 1px, transparent 1px);
  background-size: 24px 24px;
}

/* โลโก้ด้านบน */
.logo-box {
  background-color: #21963f;
  border-radius: 8px;
  width: 32px;
  height: 32px;
}

/* กล่องการ์ดสีขาวตรงกลาง */
.login-card {
  width: 100%;
  max-width: 440px;
  border-radius: 20px;
  padding: 45px 36px;
  border: 1px solid #e2e6eb;
}

/* ช่องกรอกข้อมูลขอบมน */
.custom-input :deep(.q-field__control) {
  border-radius: 30px !important;
  border-color: #dcdcdc;
}
.custom-input :deep(.q-field__control:before) {
  border-color: #dcdcdc !important;
}

/* ปุ่ม Social กลมๆ */
.social-btn {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background-color: #f1f3f5;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background 0.2s;
}
.social-btn:hover {
  background-color: #e2e6eb;
}
</style>
```eof

Your login page is now updated to match the exact design specifications from your reference image, including the rounded inputs, divider lines, and social login icons! Let me know if you need any further adjustments.