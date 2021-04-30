import Vue from 'vue'
import Router from 'vue-router'
// import { loadPage } from './util'
Vue.use(Router)

const router = new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/register',
      component: () => import('@/views/dashboard/pages/Register'),
      meta: {
        public: true,
      },
    },
    {
      path: '/login',
      component: () => import('@/views/dashboard/pages/Login'),
      meta: {
        public: true,
      },
    },
    {
      path: '',
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
        // Tables
        {
          name: 'Files',
          path: 'tables/files',
          component: () => import('@/views/dashboard/tables/RegularTables'),
        },
      ],
    },
  ],
})
router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  if (to.meta.public) {
    return next()
  }
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = localStorage.getItem('user')

  if (authRequired && !loggedIn) {
    return next('/login')
  }
  next()
})

export default router
