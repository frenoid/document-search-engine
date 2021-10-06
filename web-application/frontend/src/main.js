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
import VueQRCodeComponent from 'vue-qrcode-component'
import OtpInput from '@bachdgvn/vue-otp-input'
Vue.config.productionTip = false
Vue.use(VueClipboard)
Vue.use(PortalVue)
Vue.component('qr-code', VueQRCodeComponent)
Vue.component('v-otp-input', OtpInput)

new Vue(
  Vue.util.extend(
     { router, store, vuetify, i18n }, // router.js, store.js (if using module or Vuex)
     App,
  ),
).$mount('#app')
