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
                  Register
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
                  v-model="firstname"
                  :error-messages="firstNameErrors"
                  name="firstname"
                  label="Firstname"
                  @input="$v.firstname.$touch()"
                  @blur="$v.firstname.$touch()"
                />
                <v-text-field
                  v-model="lastname"
                  :error-messages="lastNameErrors"
                  required
                  name="lastname"
                  label="Lastname"
                  @input="$v.lastname.$touch()"
                  @blur="$v.lastname.$touch()"
                />
                <v-text-field
                  v-model="password1"
                  :error-messages="password1Errors"
                  required
                  name="password1"
                  label="Password 1"
                  type="password"
                  @input="$v.password1.$touch()"
                  @blur="$v.password1.$touch()"
                />
                <v-text-field
                  v-model="password2"
                  :error-messages="password2Errors"
                  required
                  name="password2"
                  label="Password 2"
                  type="password"
                  @input="$v.password2.$touch()"
                  @blur="$v.password2.$touch()"
                />
                <v-card-actions>
                  <v-btn
                    :disabled="shouldDisableRegisterButton"
                    color="#4caf50"
                    large
                    block
                    @click="handleSubmit"
                  >
                    Register
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
  import { containsUppercase, containsLowercase, containsNumber, containsSpecial } from '../../../helpers'
  import { validationMixin } from 'vuelidate'
  import { required, maxLength, minLength, sameAs, email } from 'vuelidate/lib/validators'
  import { mapState, mapActions } from 'vuex'
  export default {
    mixins: [validationMixin],
    validations: {
      password1: {
        required,
        maxLength: maxLength(18),
        minLength: minLength(10),
        containsUppercase,
        containsLowercase,
        containsNumber,
        containsSpecial,
      },
      password2: { required, sameAsPassword: sameAs('password1') },
      email: { required, email },
      firstname: { required, maxLength: maxLength(20) },
      lastname: { required, maxLength: maxLength(20) },
    },
    data () {
      return {
        email: '',
        password1: '',
        password2: '',
        firstname: '',
        lastname: '',
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
        !this.$v.email.email && errors.push('Must be valid e-mail')
        !this.$v.email.required && errors.push('E-mail is required')
        return errors
      },
      firstNameErrors () {
        if (this.firstname === '') {
          return []
        }
        const errors = []
        if (!this.$v.lastname.$dirty) return errors
        !this.$v.firstname.required && errors.push('First name is required')
        !this.$v.firstname.maxLength && errors.push('First name must be at most 20 characters long')
        return errors
      },
      lastNameErrors () {
        if (this.lastname === '') {
          return []
        }
        const errors = []
        if (!this.$v.lastname.$dirty) return errors
        !this.$v.lastname.required && errors.push('Last name is required')
        !this.$v.lastname.maxLength && errors.push('Last name must be at most 20 characters long')
        return errors
      },
      password1Errors () {
        if (this.password1 === '') {
          return []
        }
        const errors = []
        if (!this.$v.password1.$dirty) return errors
        !this.$v.password1.maxLength && errors.push('Password must be at most 18 characters long')
        !this.$v.password1.minLength && errors.push('Password must be at least 10 characters long')
        !this.$v.password1.containsUppercase && errors.push('Password should include at least one upper case character')
        !this.$v.password1.containsLowercase && errors.push('Password should include at least one lower case character')
        !this.$v.password1.containsNumber && errors.push('Password should include at least one number')
        !this.$v.password1.containsSpecial && errors.push('Password should include at least one special character')
        !this.$v.password1.required && errors.push('Password is required')
        return errors
      },
      password2Errors () {
        if (this.password2 === '') {
          return []
        }
        const errors = []
        if (!this.$v.password2.$dirty) return errors
        !this.$v.password2.sameAsPassword && errors.push('Passwords must be identical')
        !this.$v.password2.required && errors.push('Password is required')
        return errors
      },
      hasErrors () {
        return [...this.emailErrors, ...this.lastNameErrors, ...this.password1Errors, ...this.password2Errors].length !== 0
      },
      hasBlanks () {
        return (
          this.email === '' ||
          this.password1 === '' ||
          this.password2 === '' ||
          this.firstname === '' ||
          this.lastname === ''
        )
      },
      shouldDisableRegisterButton () {
        return this.hasErrors || this.hasBlanks
      },
    },
    created () {
      this.logout()
    },
    methods: {
      ...mapActions('account', ['logout', 'register']),
      handleSubmit (e) {
        this.submitted = true
        const { email, firstname, lastname, password1 } = this
        // if(email && password1 && password2 & lastname) {
        var password = password1
        // }
        this.register({
          email, firstname, lastname, password,
        })
      },
      clear () {
        this.$v.$reset()
        this.password2 = ''
        this.email = ''
        this.password1 = ''
        this.firstname = ''
        this.lastname = ''
      },
    },
  }
</script>
<style scoped>
.bth_transparent{
    background-color:transparent !important
}
</style>>
