<template>
  <v-container
    id="dashboard"
    fluid
    tag="section"
  >
    <v-row>
      <v-col cols="12">
        <div>
          <data-table />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'DashboardDashboard',
    components: {
      DataTable: () => import('./component/DataTable'),
    },
    data () {
      return { }
    },
  }
</script>
