import { userService } from './services'
import router from './router'

const user = JSON.parse(localStorage.getItem('user'))
const state = user
    ? { status: { loggedIn: true }, user }
    : { status: {}, user: null }

const actions = {
    verifyOTP ({ dispatch, commit }, otp) {
      commit('loginRequest', { otp })
      console.log(otp)
      userService.verifyOTP(otp).then(
        opt => {
          if (opt) {
            commit('loginSuccess', opt)
            router.push('/')
          } else {
            const error = 'OTP verification failure'
            commit('otpFailure', error)
            dispatch('alert/error', error, { root: true })
          }
        },
        error => {
          commit('loginFailure', error)
          dispatch('alert/error', error, { root: true })
        })
    },
    login ({ dispatch, commit }, { username, password }) {
        commit('loginRequest', { username })
        userService.login(username, password)
            .then(
                user => {
                    if (user && !user.otp) {
                        commit('loginSuccess', user)
                        router.push('/setup-otp')
                    } else {
                        commit('verifySuccess', user)
                        router.push('/verify-otp')
                    }
                },
                error => {
                    commit('verifyFailure', error)
                    dispatch('alert/error', error, { root: true })
                },
            )
    },
    logout ({ commit }) {
        userService.logout()
        commit('logout')
    },
    register ({ dispatch, commit }, user) {
        commit('registerRequest', user)

        userService.register(user)
            .then(
                user => {
                    commit('registerSuccess', user)
                    router.push('/login')
                    setTimeout(() => {
                    // display success message after route change completes
                    dispatch('alert/success', 'Registration successful', { root: true })
                    })
                }).catch(
                error => {
                    commit('registerFailure', error)
                    dispatch('alert/error', error, { root: true })
                },
            )
    },
    setupOTP ({ dispatch, commit }) {
        commit('setupOTPRequest')

        userService.register(user)
            .then(
                user => {
                    commit('setupOTPSuccess', user)
                    router.push('/login')
                    setTimeout(() => {
                    dispatch('alert/success', 'Setup OTP successful', { root: true })
                    })
                }).catch(
                error => {
                    commit('setupOTPFailure', error)
                    dispatch('alert/error', error, { root: true })
                },
            )
    },
    confirmOTP ({ dispatch, commit }, id) {
        commit('confirmOTPRequest')
        userService.confirmOTP(user)
            .then(
                user => {
                    commit('confirmOTPSuccess', user)
                    router.push('/login')
                    setTimeout(() => {
                    dispatch('alert/success', 'Setup OTP successful', { root: true })
                    })
                }).catch(
                error => {
                    commit('setupOTPFailure', error)
                    dispatch('alert/error', error, { root: true })
                },
            )
    },
}

const mutations = {
    loginRequest (state, user) {
        state.status = { loggingIn: true }
        state.user = user
    },
    loginSuccess (state, user) {
        state.status = { loggedIn: true }
        state.user = user
    },
    loginFailure (state) {
        state.status = {}
        state.user = null
    },
    logout (state) {
        state.status = {}
        state.user = null
    },
    registerRequest (state, user) {
        state.status = { registering: true }
    },
    registerSuccess (state, user) {
        state.status = {}
    },
    registerFailure (state, error) {
        state.status = {}
    },
    setupOTPSuccess (state, user) {
        state.status = {}
    },
    setupOTPFailure (state, error) {
        state.status = {}
    },
    confirmOTPRequest (state, user) {
        state.status = { registering: true }
    },
}

export const account = {
    namespaced: true,
    state,
    actions,
    mutations,
}
