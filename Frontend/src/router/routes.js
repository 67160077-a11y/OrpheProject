const authGuard = (to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  
  // ดึงข้อมูล user ปัจจุบันเพื่อเอามาเช็คสิทธิ์ (Role)
  const userData = JSON.parse(localStorage.getItem('user')) || {}

  if (to.path !== '/login' && !isLoggedIn) {
    // ถ้ายังไม่ล็อกอิน ให้ส่งไปหน้า login
    next('/login')
  } 
  else if (to.path === '/manage-users' && userData.role !== 'admin') {
    // ถ้าพยายามเข้าหน้า manage-users แต่ไม่ใช่ admin ให้เด้งกลับไปหน้า device
    next('/device')
  } 
  else {
    // กรณีอื่นๆ ให้ผ่านไปได้ตามปกติ
    next()
  }
}

const routes = [
  {
    path: '/login',
    component: () => import('../pages/LoginPage.vue')
  },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    beforeEnter: authGuard,
    children: [
      { path: '', redirect: '/device' },
      { path: 'device', name: 'Overview', component: () => import('../pages/DevicePage.vue') },
      { path: 'report', name: 'Report', component: () => import('../pages/ReportPage.vue') },
      { path: 'manage-users', name: 'Manage Users', component: () => import('../pages/ManageUsersPage.vue') },
    ]
  }
]

export default routes