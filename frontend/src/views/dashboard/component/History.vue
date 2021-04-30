<template>
  <v-container
    id="history"
    fluid
    tag="section"
  >
    <base-v-component
      heading="History"
      link="styles/history"
    />

    <v-row
      align="center"
      justify="center"
    >
      <v-col cols="12">
        <base-material-card
          color="green"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    data: () => {},
  }
</script>

<style lang="scss">
  .tim-note {
    bottom: 10px;
    color: #c0c1c2;
    display: block;
    font-weight: 400;
    font-size: 13px;
    line-height: 13px;
    left: 0;
    margin-left: 20px;
    width: 260px;
  }
</style>
