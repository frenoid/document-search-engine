import Vue from 'vue'
import Vuex from 'vuex'

import { alert } from './alert.module'
import { account } from './account.module'
import { users } from './users.module'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    barColor: 'rgba(0, 0, 0, .8), rgba(0, 0, 0, .8)',
    barImage: './assets/img/sidebar-1.jpg',
    drawer: null,
  },
  mutations: {
    SET_BAR_IMAGE (state, payload) {
      state.barImage = payload
    },
    SET_DRAWER (state, payload) {
      state.drawer = payload
    },
  },
  actions: {

  },
  modules: {
    alert,
    account,
    users,
  },
})
