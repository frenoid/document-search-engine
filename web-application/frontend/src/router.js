import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

const router = new Router({
  mode: '',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/login',
      component: () => import('@/views/dashboard/pages/Login'),
      meta: {
        public: true,
      },
    },
    {
      path: '/verify-otp',
      component: () => import('@/views/dashboard/pages/VerifyOTP'),
      meta: {
        public: true,
      },
    },
    {
      path: '/setup-otp',
      component: () => import('@/views/dashboard/pages/SetupOTP'),
      meta: {
        public: false,
      },
    },
    {
      path: '/register',
      component: () => import('@/views/dashboard/pages/Register'),
      meta: {
        public: true,
      },
    },
    {
      path: '/',
      component: () => import('@/views/dashboard/Index'),
      children: [
        // Dashboard
        {
          name: 'dashboard',
          path: '',
          component: () => import('@/views/dashboard/Dashboard'),
        },
        // Pages
        {
          name: 'User Profile',
          path: 'pages/user',
          component: () => import('@/views/dashboard/pages/UserProfile'),
        },
        {
          name: 'Notifications',
          path: 'components/notifications',
          component: () => import('@/views/dashboard/component/Notifications'),
        },
        {
          name: 'History',
          path: 'components/history',
          component: () => import('@/views/dashboard/component/History'),
        },
        {
          name: 'Files',
          path: 'files',
          component: () => () => import('@/views/dashboard/tables/RegularTables'),
        },
        {
          name: 'Document Details',
          path: 'files/:id',
          component: () => import('@/views/dashboard/component/FileDetail'),
        },
      ],
    },
  ],
})
router.beforeEach((to, from, next) => {
  if (to.meta.public) {
    return next()
  }
  const publicPages = ['/login', '/register', '/verify-otp']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = localStorage.getItem('user')
  const token = localStorage.getItem('token')
  if (authRequired && !token) {
    return next({
      path: '/login',
      query: { redirect: to.fullPath },
    })
  }
  if (authRequired && !loggedIn) {
    return next({
      path: '/login',
      query: { redirect: to.fullPath },
    })
  }
  next()
})

export default router
