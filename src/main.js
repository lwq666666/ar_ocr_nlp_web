import Vue from 'vue'

Vue.config.productionTip = false

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import '@/styles/index.scss' // global css

import App from './App.vue'
import router from './router'
import store from './store'

import './permission' // permission control

import axios from 'axios'
import global_ from './config/Global.vue'
Vue.prototype.GLOBAL = global_;
axios.defaults.baseURL = global_.BASE_URL;
axios.defaults.withCredentials = true
Vue.prototype.$ajax = axios

import './icons'


Vue.prototype.GLOBAL = global_;

Vue.prototype.$ajax = axios

Vue.use(ElementUI)

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})