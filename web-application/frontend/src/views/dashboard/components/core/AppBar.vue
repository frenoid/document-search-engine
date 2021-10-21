<template>
  <v-app-bar
    id="app-bar"
    absolute
    app
    color="transparent"
    flat
    height="75"
  >
    <v-btn
      class="mr-3"
      elevation="1"
      fab
      small
      @click="setDrawer(!drawer)"
    >
      <v-icon v-if="value">
        mdi-view-quilt
      </v-icon>

      <v-icon v-else>
        mdi-dots-vertical
      </v-icon>
    </v-btn>

    <v-toolbar-title
      class="hidden-sm-and-down font-weight-light"
      v-text="$route.name"
    />

    <v-spacer />
    <div class="mx-3" />
    <v-btn
      class="ml-2"
      min-width="0"
      text
      to="pages/user"
    >
      <v-icon>mdi-account</v-icon>
      {{ name }}
    </v-btn>
    <div class="mx-3" />
    <v-btn
      class="ml-2"
      min-width="0"
      text
      type="button"
      @click="handleLogout"
    >
      Logout
    </v-btn>
  </v-app-bar>
</template>

<script>
  // Components
  // import { VHover, VListItem } from 'vuetify/lib'

  // Utilities
  import { mapState, mapMutations, mapActions } from 'vuex'

  export default {
    name: 'DashboardCoreAppBar',
    props: {
      value: {
        type: Boolean,
        default: false,
      },
    },

    data: () => ({
      notifications: [],
      name: 'Tony Aizize',
    }),
    computed: {
      ...mapState(['drawer']),
    },
    methods: {
      ...mapActions('account', ['logout']),
      ...mapMutations({
        setDrawer: 'SET_DRAWER',
      }),
      handleLogout (e) {
        e.preventDefault()
        console.log('logout clicked')
        this.logout()
      },
    },
  }
</script>
