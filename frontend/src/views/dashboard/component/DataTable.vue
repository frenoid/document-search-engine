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
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="files"
      :search="search"
      :loading="loadTable"
      loading-text="Loading... Please wait"
    ></v-data-table>
  </v-card>
</template>
<script>
    import {
        searchFiles
    } from '../../../services/files';
  export default {
    name: 'DataTable',
    data () {
      return {
        loadTable: false,
        search: '',
        headers: [
          {
            text: 'Name',
            align: 'start',
            filterable: false,
            value: 'name',
          },
          { text: 'type', value: 'Type' },
          { text: 'Category', value: 'category' },
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
    methods: {
        async fetchFiles(options){
            this.loadTable = true
            this.files = []
            const search = this.search.trim();
            let params = { search }
            params.items_per_page = this.tableOptions.itemsPerPage;
            params.page = this.tableOptions.page;
            try {
                const response = await searchFiles(params)
            } catch (error){
                console.log(error)
                this.files = []
            } finally{
                this.loadTable = false
            } 
        }
    },
    watch: {
    tableOptions(newVal) {
      this.fetchFiles(newVal);
    },
    created() {
        this.fetchFiles();
    },
  },
  }
</script>