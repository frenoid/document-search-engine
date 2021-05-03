<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
        @change="fetchFiles"
      />
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="files"
      :search="search"
      :loading="loadTable"
      loading-text="Loading... Please wait"
    />
  </v-card>
</template>
<script>
  import {
    searchFiles,
  } from '../../../services/files'
  export default {
    name: 'DataTable',
    data () {
      return {
        loadTable: false,
        search: '',
        headers: [
          {
            text: 'ID',
            align: 'start',
            filterable: false,
            value: 'id',
          },
          { text: 'Topic', value: 'topic' },
          { text: 'Score', value: 'score' },
        ],
        files: [],
        tableOptions: {
          page: 1,
          itemsPerPage: 10,
          toWatch: true,
        },
        serverItemsLength: undefined,
      }
    },
    watch: {
      tableOptions (newVal) {
        this.fetchFiles(newVal)
      },
    },
    methods: {
      async fetchFiles (options) {
        this.loadTable = true
        // this.files = []
        const search = this.search.trim()
        const params = { search }
        params.items_per_page = this.tableOptions.itemsPerPage
        params.page = this.tableOptions.page
        try {
          const response = await searchFiles(params)
          this.files = response.response
        } catch (error) {
          this.files = []
        } finally {
          this.loadTable = false
          console.log(this.files)
        }
      },
    },
  }
</script>
