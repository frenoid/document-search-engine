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
    >
      <template #item.actions="{ item }">
        <router-link
          :to="{ path: `files/${item.id}` }"
          :style="{ textDecoration: 'none', marginRight: '3px' }"
          appendx
        >
          <v-tooltip top>
            <template #activator="{ on }">
              <v-icon
                color="primary"
                class="mr-3"
                v-on="on"
              >
                mdi-eye
              </v-icon>
            </template>
            <span>View Details</span>
          </v-tooltip>
        </router-link>
        <v-tooltip top>
          <template #activator="{ on }">
            <v-icon
              small
              class="mr-3"
              color="primary"
              v-on="on"
            >
              mdi-thumb-up
            </v-icon>
          </template>
          <span>Oh yes...</span>
        </v-tooltip>
        <v-tooltip top>
          <template #activator="{ on }">
            <v-icon
              small
              color="primary"
              class="mr-3"
              v-on="on"
            >
              mdi-thumb-down
            </v-icon>
          </template>
          <span>No lah...</span>
        </v-tooltip>
      </template>
    </v-data-table>
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
          {
            text: 'Actions',
            value: 'actions',
            displayed: true,
            sortable: false,
            align: 'left',
            width: '200px',
          },
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
        }
      },
    },
  }
</script>
