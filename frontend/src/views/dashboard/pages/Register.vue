<template>
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
                :error-messages="emailErrors"
                required
                name="firstname"
                label="Firstname"
                @input="$v.firstname.$touch()"
                @blur="$v.firstname.$touch()"
              />
              <v-text-field
                v-model="lastname"
                :error-messages="emailErrors"
                required
                name="lastname"
                label="Lastname"
                @input="$v.lastname.$touch()"
                @blur="$v.lastname.$touch()"
              />
              <v-text-field
                v-model="password1"
                :error-messages="password2Errors"
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
                  primary
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
</template>
<script>
  import { validationMixin } from 'vuelidate'
  import { required, maxLength, email } from 'vuelidate/lib/validators'
  import { mapState, mapActions } from 'vuex'
  export default {
    mixins: [validationMixin],

    validations: {
      password2: { required, maxLength: maxLength(10) },
      password1: { required, maxLength: maxLength(10) },
      email: { required, email },
      lastname: { required,  maxLength: maxLength(20)},
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
        const errors = []
        if (!this.$v.email.$dirty) return errors
        !this.$v.email.email && errors.push('Must be valid e-mail')
        !this.$v.email.required && errors.push('E-mail is required')
        return errors
      },
      password1Errors () {
        const errors = []
        if (!this.$v.password1.$dirty) return errors
        !this.$v.password1.maxLength && errors.push('password must be at most 10 characters long')
        !this.$v.password1.required && errors.push('password is required.')
        return errors
      },
      password2Errors () {
        const errors = []
        if (!this.$v.password2.$dirty) return errors
        !this.$v.password2.maxLength && errors.push('password must be at most 10 characters long')
        !this.$v.password2.required && errors.push('password is required.')
        return errors
      },
    },
    created () {
      this.logout()
    },
    methods: {
     ...mapActions('account', ['logout', 'register']),
     handleSubmit (e) {
        this.submitted = true
        const { email, password2, firstname, lastname, password1 } = this
        // if(email && password1 && password2 & lastname) {
          
        // }
        this.register({
            email, firstname, lastname, password1, password2
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
