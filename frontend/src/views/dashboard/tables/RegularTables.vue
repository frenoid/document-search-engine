<template>
  <v-container
    id="files"
    fluid
    tag="section"
  >
    <base-v-component
      heading=""
      link="components/simple-tables"
    />

    <base-material-card
      title=""
      class="px-5 py-3"
    >
      <data-table />
    </base-material-card>
  </v-container>
</template>
<script>
export default {
  components: { 
    DataTable: () => import('../component/DataTable')
  },
}
</script>