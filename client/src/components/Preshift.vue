<template>
  <div class="mx-4 mb-8">
    <h1 class="text-blue-500 text-2xl mb-2">Pre-Shift Plan</h1>
    <table class="min-w-full divide-y divide-gray-200">
      <thead>
        <tr>
          <th/>
          <th class="px-6 py-3 text-center text-sm font-medium text-gray-500 uppercase tracking-wider">Speed of Service</th>
          <th class="px-6 py-3 text-center text-sm font-medium text-gray-500 uppercase tracking-wider">Fan Feedback</th>
          <th class="px-6 py-3 text-center text-sm font-medium text-gray-500 uppercase tracking-wider" colspan="2">Round Up</th>
        </tr>
        <tr class="bg-gray-50">
          <th/>
          <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">14 Day Rolling Avg</th>
          <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Month to Date Responses</th>
          <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">MTD %</th>
          <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">MTD $</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="store in stores" :key="store.id">
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ store.name }}</td>
          <td class="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-500">{{
              speeds && speeds.length > 0
                  ? (speeds.find(s => s.store_id === store.id) || {}).goal
                  : 'No Data'
            }}</td>
          <td class="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-500">{{
              responses && responses.length > 0
                  ? (responses.find(r => r.store_id === store.id) || {}).feedback_count
                  : 'No Data'
            }}</td>
          <td class="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-500">{{
              roundup_percent && roundup_percent.length > 0
                  ? (roundup_percent.find(r => r.store_id === store.id) || {}).roundup_percent + '%'
                  : 'No Data'
            }}</td>
          <td class="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-500">{{
              roundup_amount && roundup_amount.length > 0
                  ? '$' + (roundup_amount.find(r => r.store_id === store.id) || {}).roundup_amount
                  : 'No Data'
            }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {createClient} from "@supabase/supabase-js";

export default {
  name: 'PreshiftComponent',
  data() {
    return {
      stores: [],
      speeds: [{"store_id": 1, "goal": '3:57'}, {"store_id": 2, "goal": "3:57"}, {"store_id": 3, "goal": "3:57"}, {"store_id": 4, "goal": "3:57"}],
      responses: [{"store_id": 1, "feedback_count": 10}, {"store_id": 2, "feedback_count": 10}, {"store_id": 3, "feedback_count": 10}, {"store_id": 4, "feedback_count": 10}],
      roundup_percent: [{"store_id": 1, "roundup_percent": 50}, {"store_id": 2, "roundup_percent": 50}, {"store_id": 3, "roundup_percent": 50}, {"store_id": 4, "roundup_percent": 50}],
      roundup_amount: [{"store_id": 1, "roundup_amount": 100}, {"store_id": 2, "roundup_amount": 100}, {"store_id": 3, "roundup_amount": 100}, {"store_id": 4, "roundup_amount": 100}],
    };
  },
  async created() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      // Fetch data from the server
      const supabaseUrl = 'https://kujnrwxiutypfwkucykt.supabase.co'
      const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt1am5yd3hpdXR5cGZ3a3VjeWt0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwODgxNDgsImV4cCI6MjAzMjY2NDE0OH0.8OIYDcMTA5tRnTKg41cunrI_T2lkLLEwA6IyL7VjAuA'
      const supabase = createClient(supabaseUrl, supabaseKey)

      // get the data from the store table
      let {data: stores, store_error} = await supabase.from('store').select('*')
      if (store_error) {
        console.error('Error: ', store_error)
      } else {
        console.log('Data: ', stores)
        this.stores = stores
      }
    },
  },
};
</script>
