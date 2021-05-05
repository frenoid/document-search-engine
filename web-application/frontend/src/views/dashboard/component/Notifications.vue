<template>
  <v-container
    id="alerts"
    fluid
    tag="section"
  >
    <base-v-component
      heading=""
      link="components/alerts"
    />

    <v-row>
      <v-col
        cols="12"
      >
        <v-card>
          <v-card-text>
            <base-subheading subheading="Notifications" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <base-material-snackbar
      v-model="snackbar"
      :type="color"
      v-bind="{
        [parsedDirection[0]]: true,
        [parsedDirection[1]]: true
      }"
    />

    <v-dialog
      v-model="dialog"
      max-width="500"
    >
      <v-card class="text-center">
        <v-card-title>
          Dialog Title

          <v-spacer />

          <v-icon
            aria-label="Close"
            @click="dialog = false"
          >
            mdi-close
          </v-icon>
        </v-card-title>

        <v-card-text>
          Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar.
        </v-card-text>

        <v-card-actions>
          <v-spacer />

          <v-btn
            color="error"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="dialog2"
      max-width="500"
    >
      <v-card>
        <v-card-title>
          How do you become an affiliate?

          <v-spacer />

          <v-icon
            aria-label="Close"
            @click="dialog2 = false"
          >
            mdi-close
          </v-icon>
        </v-card-title>

        <v-card-text class="text-body-1 text-center">
          <v-row />

          <v-btn
            class="mt-6"
            color="info"
            depressed
            default
            rounded
            @click="dialog2 = false"
          >
            Sounds good
          </v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="dialog3"
      max-width="300"
    >
      <v-card>
        <v-card-title>
          Are you sure?

          <v-spacer />

          <v-icon
            aria-label="Close"
            @click="dialog3 = false"
          >
            mdi-close
          </v-icon>
        </v-card-title>

        <v-card-text class="pb-6 pt-12 text-center">
          <v-btn
            class="mr-3"
            text
            @click="dialog3 = false"
          >
            Nevermind
          </v-btn>

          <v-btn
            color="success"
            text
            @click="dialog3 = false"
          >
            Yes
          </v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
  export default {
    name: 'DashboardNotifications',

    data: () => ({
      color: 'info',
      colors: [],
      dialog: false,
      dialog2: false,
      dialog3: false,
      direction: 'top center',
      directions: [
        'top left',
        'top center',
        'top right',
        'bottom left',
        'bottom center',
        'bottom right',
      ],
      snackbar: false,
    }),

    computed: {
      parsedDirection () {
        return this.direction.split(' ')
      },
    },

    methods: {
      randomColor () {
        this.color = this.colors[Math.floor(Math.random() * this.colors.length)]
      },
    },
  }
</script>
