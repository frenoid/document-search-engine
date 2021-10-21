<template>
  <div>
    <v-toolbar
      color="#4caf50"
    >
      <v-toolbar-title>Team 3</v-toolbar-title>
      <v-spacer />
      <v-btn
        icon
        to="register"
        class="bth_transparent"
      >
        Register
      </v-btn>
    </v-toolbar>
    <v-container>
      <v-row class="text-center">
        <v-col cols="3" />
        <v-col
          cols="6"
        >
          <v-container
            style="position: relative;top: 13%;"
            class="text-center"
          >
            <v-card flat>
              <v-card-title
                primary-title
              >
                <h4>
                  Login
                </h4>
              </v-card-title>
              <form>
                <v-text-field
                  v-model="email"
                  :error-messages="emailErrors"
                  required
                  name="email"
                  label="Email"
                  @input="$v.email.$touch()"
                  @blur="$v.email.$touch()"
                />
                <v-text-field
                  v-model="password"
                  :error-messages="passwordErrors"
                  required
                  name="password"
                  label="Password"
                  type="password"
                  @input="$v.password.$touch()"
                  @blur="$v.password.$touch()"
                />
                <v-card-actions>
                  <v-btn
                  :disabled="shouldDisableLoginButton"
                    color="#4caf50"
                    large
                    block
                    @click="handleSubmit"
                  >
                    Login
                  </v-btn>
                </v-card-actions>
              </form>
            </v-card>
          </v-container>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
  import { validationMixin } from 'vuelidate'
  import { required } from 'vuelidate/lib/validators'
  import { mapState, mapActions } from 'vuex'

  export default {
    mixins: [validationMixin],

    validations: {
      password: { required },
      email: { required },
    },
    data () {
      return {
        email: '',
        password: '',
        submitted: false,
      }
    },
    computed: {
      ...mapState('account', ['status']),
      emailErrors () {
        if (this.email === '') {
          return []
        }
        const errors = []
        if (!this.$v.email.$dirty) return errors
        !this.$v.email.required && errors.push('E-mail is required')
        return errors
      },
      passwordErrors () {
        if (this.password === '') {
          return []
        }
        const errors = []
        if (!this.$v.password.$dirty) return errors
        !this.$v.password.required && errors.push('Password is required.')
        return errors
      },
      hasErrors () {
        return [...this.emailErrors, ...this.passwordErrors].length !== 0
      },
      hasBlanks () {
        return this.email === '' || this.password === ''
      },
      shouldDisableLoginButton () {
        return this.hasErrors || this.hasBlanks
      },
    },
    created () {
    },
    methods: {
      ...mapActions('account', ['login', 'logout', 'verifyOTP']),
      handleSubmit (e) {
        const { email, password } = this
        if (email && password) {
          this.submitted = true
          this.login({ username: email, password: password })
        }
      },
      clear () {
        this.$v.$reset()
        this.password = ''
        this.email = ''
      },
      handleOnComplete (opt) {
        console.log('OTP completed: ', opt)
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
    width: 40px;
    height: 40px;
    padding: 5px;
    margin: 0 10px;
    font-size: 20px;
    border-radius: 4px;
    border: 1px solid rgba(0, 0, 0, 0.3);
    textalign: "center";
  }
  .error {
    border: 1px solid red !important;
  }
</style>
