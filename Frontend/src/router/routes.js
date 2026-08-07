const authGuard = (to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  if (to.path !== '/login' && !isLoggedIn) {
    next('/login')
  } else {
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
      { path: 'report', name: 'Report', component: () => import('../pages/ReportPage.vue') }
    ]
  }
]

export default routes