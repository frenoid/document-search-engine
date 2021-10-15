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
                :text="token"
                color="#e74c3c"
              >
              </qr-code>
            </div>
           <v-card-actions>
              <v-btn
                color="#4caf50"
                block
                to="verify-otp"
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
      console.log('ssssssss', qrcode)
      if (qrcode) {
        this.token = qrcode
      }
    },
  }
</script>
<style scoped>
.bth_transparent{
    background-color:transparent !important
}
</style>>
