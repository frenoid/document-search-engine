<template>
  <div>
    <v-toolbar
      color="#4caf50"
    >
      <v-toolbar-title>Team 3</v-toolbar-title>
      <v-spacer />
      <v-btn
        icon
        to="Login"
        class="bth_transparent"
      >
        Login
      </v-btn>
    </v-toolbar>
    <v-container
      class="text-center"
    >
      <v-row class="text-center">
        <v-col cols="3" />
        <v-col
          cols="6"
        >
          <div
            style="position: relative;top: 200%;"
          >
            <v-otp-input
              ref="otpInput"
              input-classes="otp-input"
              separator="-"
              :num-inputs="6"
              :should-auto-focus="true"
              :is-input-num="true"
              @on-change="handleOnChange"
              @on-complete="handleOnComplete"
            />
            <v-card-actions>
              <v-btn
                color="#4caf50"
                block
              >
                Verify
              </v-btn>
            </v-card-actions>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    data () {
      return {
        submitted: false,
      }
    },
    computed: {
      ...mapState('account', ['status']),
    },
    created () {
      this.logout()
    },
    methods: {
      ...mapActions('account', ['login', 'logout', 'verifyOTP']),
      handleOnComplete (opt) {
        if (opt) {
          this.verifyOTP(opt)
        }
      },
      handleOnChange (value) {
        console.log('OTP changed: ', value)
      },
      handleClearInput () {
        this.$refs.otpInput.clearInput()
      },
    },
  }
</script>
<style>
  .bth_transparent{
    background-color:transparent !important
  }
  .otp-input {
    width: 50px;
    height: 50px;
    padding: 10px;
    margin: 0 20px;
    font-size: 20px;
    border-radius: 4px;
    border: 1px solid rgba(0, 0, 0, 0.3);
    textalign: "center";
  }
  .error {
    border: 1px solid red !important;
  }
</style>
