<template>
  <div>

    <div className="mb-4">
      <label for="metric" className="text-md font-semibold">Metric:</label>
      <select v-model="selectedMetric" id="metric" className="border mx-2 px-2 py-1 rounded">
        <option v-for="metric in metrics" :key="metric.id" :value="metric.value">{{ metric.text }}</option>
      </select>
    </div>

    <div className="mb-4">
      <label for="days" className="text-md font-semibold">Timespan:</label>
      <select v-model="selectedDays" id="days" className="border mx-2 px-2 py-1 rounded">
        <option value="7">Week</option>
        <option value="30">Month</option>
        <option value="90">Quarter</option>
        <option value="365">Year</option>
      </select>
    </div>

    <div className="mb-4">
      <label className="text-md font-semibold">Locations:</label>
      <div v-for="store in stores" :key="store.id" className="m-2">
        <input
            type="checkbox"
            :id="store.id"
            :value="store.id"
            v-model="selectedStores"
            className="mr-2 align-middle"
        />
        <label :for="store.id" className="align-middle">{{ store.name }}</label>
      </div>
    </div>

    <button @click="submitSelection" className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">Submit</button>
  </div>
</template>

<script>
import {dataMixin} from "@/mixins";

export default {
  name: 'ChartInputSelector',
  props: ['stores'],
  mixins: [dataMixin],
  data() {
    return {
      selectedDays: 7,
      selectedStores: [],
      selectedMetric: 'net_sales', // Default value
    };
  },
  methods: {
    submitSelection() {
      this.$emit('selection-changed', {
        days: this.selectedDays,
        stores: this.selectedStores,
        metric: this.selectedMetric // Emit the selected metric
      });
    }
  },
  created() {
    console.log('ChartInputSelector created')
    console.log('Stores:', this.stores)
    // Set the initial values
    this.selectedDays = 7; // Week
    this.selectedStores = [this.stores[0].id, this.stores[1].id, this.stores[2].id, this.stores[3].id]; // All stores
    this.selectedMetric = this.metrics[0].value; // First metric

    // Call submitSelection
    this.submitSelection();


  }
};
</script>

<style scoped>
/* No additional styles needed as we are using Tailwind CSS */
</style>
