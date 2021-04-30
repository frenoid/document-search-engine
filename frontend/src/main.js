// =========================================================
// * Vuetify Material Dashboard - v2.1.0
// =========================================================
// * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/base'
import './plugins/chartist'
import './plugins/vee-validate'
import vuetify from './plugins/vuetify'
import i18n from './i18n'
import VueClipboard from 'vue-clipboard2'
import PortalVue from 'portal-vue'

Vue.config.productionTip = false
Vue.use(VueClipboard)
Vue.use(PortalVue)

new Vue(
  Vue.util.extend(
     { router, store, vuetify, i18n }, // router.js, store.js (if using module or Vuex)
     App,
  ),
).$mount('#app')
