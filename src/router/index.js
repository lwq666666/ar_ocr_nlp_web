import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import exhibisionRouter from './modules/exhibision'
import sceneRouter from './modules/scene'

export const constantRouterMap = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: "login",
    component: () => import('@/views/login/index'),
  },
  {
    path: '/404',
    component: () => import('@/views/errorPage/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/errorPage/401'),
    hidden: true
  },
]

export default new Router({
  // mode: 'history', // require service support
  // scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})

export const asyncRouterMap = [
  {
    path: '/reset-password',
    name: 'reset',
    component: () => import('@/views/reset-password/index')
  },

  {
    path: '/layout',
    name: 'layout',
    component: () => import('@/views/layout/Layout'),
    redirect: { name: 'front' },
    children: [
      {
        path: '/front-page',
        name: 'front',
        component: () => import('@/views/front-page/index')
      },
      {
        path: '/console',
        name: 'console',
        component: () => import('@/views/console/index'),
      },
      sceneRouter,
      exhibisionRouter
    ]
  },
  { path: '*', redirect: '/404', hidden: true }


]