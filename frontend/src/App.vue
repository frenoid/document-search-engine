<template>
   <main>
      <transition mode="out-in">
        <router-view></router-view>
      </transition>
   </main>
  <!-- <v-app>
    <router-view />
  </v-app> -->
</template>

<script>
  import { mapState, mapActions } from 'vuex'
  export default {
    name: 'App',
    computed: {
      ...mapState({
        alert: state => state.alert,
      }),
    },
    watch: {
      $route (to, from) {
        // clear alert on location change
        this.clearAlert()
      },
    },
    methods: {
      ...mapActions({
        clearAlert: 'alert/clear',
      }),
    },
  }
</script>
