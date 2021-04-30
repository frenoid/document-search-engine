<template>
  <v-app>
    <v-container>
      <login />
      <v-content>
        <transition mode="out-in">
          <router-view />
        </transition>
      </v-content>
    </v-container>
  </v-app>
</template>

<script>
  import Login from './pages/Login.vue'
  export default {
    name: 'Auth',
    components: {
      Login,
    },
    data: () => ({
      expandOnHover: false,
    }),
  }
</script>
