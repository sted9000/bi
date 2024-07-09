<template>
  <div className="mx-5 mb-8">
    <div className="inline-block mb-4">
      <VueDatePicker
          v-model="date"
          :format="formatDate"
          :max-date="new Date()"
          auto-apply
          :enable-time-picker="false"
          :clearable="false"
          className="bg-white border border-gray-300 rounded-md shadow-sm px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
    <div v-if="stillLoading" className="text-center text-xl text-gray-600">Loading...</div>
    <div v-else-if="sales.length === 0" className="text-center text-xl text-gray-600">No data available for the selected date</div>
      <table v-else className="min-w-full table-auto">
        <thead className="bg-blue-600">
        <tr>
          <th className="px-4 py-2 text-white text-md"></th>
          <th className="px-4 py-2 text-white text-md">Net Sales ($)</th>
          <th className="px-4 py-2 text-white text-md">Customers (#)</th>
          <th className="px-4 py-2 text-white text-md">Labor (%)</th>
          <th className="px-4 py-2 text-white text-md">SPLH ($)</th>
          <th className="px-4 py-2 text-white text-md">Over/Short ($)</th>
          <th className="px-4 py-2 text-white text-md">Jolt Complete (%)</th>
          <th className="px-4 py-2 text-white text-md">HME Average (mm:ss)</th>
          <th className="px-4 py-2 text-white text-md">Donation (%)</th>
          <th className="px-4 py-2 text-white text-md">Refunds ($)</th>
          <th className="px-4 py-2 text-white text-md">Overnight Clock-ins (#)</th>
          <th className="px-4 py-2 text-white text-md">Unpaid Hours (#)</th>
        </tr>
        </thead>
        <tbody>
        <TableRow
            v-for="(store, index) in stores"
            :key="store.id"
            :store="store"
            :sales="sales"
            :jolt="jolt"
            :hme="hme"
            :till="till"
            :hourly="hourly"
            :break_time="break_time"
            :class="{ 'bg-gray-50': index % 2, 'hover:bg-gray-100': true }"
        />
        <tr className="bg-gray-100 font-semibold">
          <td className="border px-4 py-2 text-md">Total</td>
          <td className="border px-4 py-2 text-md">{{ calculateTotal('net_sales').toFixed(2) }}</td>
          <td className="border px-4 py-2 text-md">{{ calculateTotal('customer_count') }}</td>
        </tr>
        </tbody>
      </table>
    </div>
</template>

<script>
import {supabase} from "../supabase";
import TableRow from "@/components/TableRow";
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

export default {
  name: 'App',
  components: {TableRow, VueDatePicker},
  data() {
    return {
      stores: [],
      sales: null,
      jolt: null,
      hme: null,
      till: null,
      hourly: null,
      break_time: null,
      // set the default date to yesterday
      date: new Date(Date.now() - 86400000) // This ensures you start with a local date
    }
  },
  async created() {
    // Fetch the data when the component is created
    // However this is handled by the watcher below
  },
  computed: {
    stillLoading() {
      return this.sales === null || this.jolt === null || this.hme === null || this.till === null || this.hourly === null || this.break_time === null;
    }
  },
  methods: {
    calculateTotal(key) {
      if (!this.sales) return 0;
      return this.sales.reduce((acc, curr) => acc + (curr[key] || 0), 0);
    },

    formatDate(date) {
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();

      return `${month}/${day}/${year}`;
    },

    async fetchData() {
      this.sales = null;
      this.jolt = null;
      this.hme = null;
      this.till = null;
      this.hourly = null;
      this.break_time = null;

      let {data: stores, error: store_error} = await supabase.from('store').select('*');
      if (store_error) {
        console.error('Error: ', store_error);
      } else {
        this.stores = stores;
      }

      let selectedDate = this.date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });

      let {data: sales, error: sales_error} = await supabase.from('sales').select('*').eq('date', selectedDate);
      if (sales_error) {
        console.error('Error: ', sales_error);
      } else {
        this.sales = sales;
      }

      let {data: jolt, error: jolt_error} = await supabase.from('jolt').select('*').eq('date', selectedDate);
      if (jolt_error) {
        console.error('Error: ', jolt_error);
      } else {
        this.jolt = jolt;
      }

      let {data: hme, error: hme_error} = await supabase.from('hme').select('*').eq('date', selectedDate);
      if (hme_error) {
        console.error('Error: ', hme_error);
      } else {
        this.hme = hme;
      }

      let {data: till, error: till_error} = await supabase.from('till').select('*').eq('date', selectedDate);
      if (till_error) {
        console.error('Error: ', till_error);
      } else {
        this.till = till;
      }

      let {data: hourly, error: hourly_error} = await supabase.from('hourly').select('*').eq('date', selectedDate);
      if (hourly_error) {
        console.error('Error: ', hourly_error);
      } else {
        this.hourly = hourly;
      }

      let {
        data: break_time,
        error: break_time_error
      } = await supabase.from('break').select('*').eq('date', selectedDate);
      if (break_time_error) {
        console.error('Error: ', break_time_error);
      } else {
        this.break_time = break_time;
      }
    }
  },
  watch: {
    date: {
      handler: 'fetchData',
      immediate: true
    }
  }
}
</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
}
</style>
