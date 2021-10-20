<template>
  <div>
    <v-toolbar
      color="#4caf50"
    >
      <v-toolbar-title>Team 3</v-toolbar-title>
      <v-spacer />
      <v-btn
        icon
        to="login"
        class="bth_transparent"
      >
        Login
      </v-btn>
    </v-toolbar>
    <v-container>
      <v-row>
        <v-col cols="4" />
        <v-col>
          <v-card
            class="mx-auto"
            max-width="344"
          >
            <div style="padding:35px;">
              <qr-code
                text="otpauth://totp/tony12%40abuduaini.com?secret=EZ3HBRWHOXNQEEKSSCF45RMN2QL7WFPF&algorithm=SHA1&digits=6&period=30"
                color="#e74c3c"
              />
            </div>
            <v-card-actions>
              <v-btn
                color="#4caf50"
                block
                @click="handleSubmit"
              >
                Confirm
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
  import { mapActions } from 'vuex'
  import VueQRCodeComponent from 'vue-qrcode-component'
  export default {
    components: {
      'qr-code': VueQRCodeComponent,
    },
    data: () => ({
      show: false,
      token: null,
    }),
    created () {
      const qrcode = localStorage.getItem('qrcode')
      if (qrcode) {
        this.token = qrcode
      }
    },
    methods: {
      ...mapActions('account', ['confirmOTP']),
      handleSubmit (e) {
        const user = localStorage.getItem('user')
        if (user) {
          this.confirmOTP(user.id)
        }
      },
    },
  }
</script>
<style scoped>
.bth_transparent{
    background-color:transparent !important
}
</style>>
