<template>
  <v-container
    id="files-details"
    fluid
    tag="section"
  >
    <base-v-component
      heading=""
      link="components/simple-tables"
    />
    <base-material-card
      title="Document Details"
      class="px-5 py-3"
    >
      <v-container>
        <v-card elevation="2">
          <v-card-title>{{ file.topic }}</v-card-title>
          <v-card-text class="">
            {{ file.content }}
          </v-card-text>
        </v-card>
      </v-container>
    </base-material-card>
  </v-container>
</template>
<script>
  import {
    getFileDetails,
  } from '../../../services/files'

  export default {
    data () {
      return {
        loading: false,
        file: {
          topic: '',
          content: 'No content found',
        },
      }
    },
    created () {
      this.getFileDetails()
    },
    methods: {
      async getFileDetails () {
        try {
          const response = await getFileDetails(this.$route.params.id)
          this.file = response.response
        } catch (error) {
          this.files = []
        } finally {
          this.loading = false
        }
      },
    },
  }
</script>
