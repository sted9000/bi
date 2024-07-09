<template>
  <tr :class="{ 'bg-gray-50': index % 2, 'hover:bg-gray-100': true }">
    <td class="border px-4 py-2 text-md font-semibold">{{ store.name }}</td>
    <td class="border px-4 py-2 text-md">
      {{
        sales && sales.length > 0
            ? (sales.find(s => s.store_id === store.id) || {}).net_sales.toFixed(2)
            : 'No Data'
      }}
    </td>
    <td class="border px-4 py-2 text-md">
      {{
        sales && sales.length > 0
            ? (sales.find(s => s.store_id === store.id) || {}).customer_count
            : 'No Data'
      }}
    </td>
    <td class="border px-4 py-2 text-md">
      {{
        sales && sales.length > 0
            ? (sales.find(s => s.store_id === store.id) || {}).labor_percent
            : 'No Data'
      }}
    </td>
    <td class="border px-4 py-2 text-md">
      {{
        sales && sales.length > 0
            ? (sales.find(s => s.store_id === store.id) || {}).sales_per_labor_hour
            : 'No Data'
      }}
    </td>
    <td class="border px-4 py-2 text-md">
      {{
        till && till.length > 0
            ? (till.find(t => t.store_id === store.id) || {}).over_short
            : 'No Data'
      }}
    </td>
    <td class="border px-4 py-2 text-md">
      {{
        jolt && jolt.length > 0
            ? (jolt.find(j => j.store_id === store.id) || {}).complete_percent
            : 'No Data'
      }}
    </td>
    <td class="border px-4 py-2 text-md">
      {{
        hme && hme.length > 0
            ? secondsToMMSS(
                (hme.find(h => h.store_id === store.id) || {}).average_time
            )
            : 'No Data'
      }}
    </td>
    <td class="border px-4 py-2 text-md">
      {{ calculateDonationPercent(store) }}%
    </td>
    <td class="border px-4 py-2 text-md">
      {{
        sales && sales.length > 0
            ? (sales.find(s => s.store_id === store.id) || {}).refunds
            : 'No Data'
      }}
    </td>
    <td class="border px-4 py-2 text-md">
      {{
        hourly && hourly.length > 0
            ? (hourly.find(s => s.store_id === store.id) || {}).overnight_clockins
            : 'No Data'
      }}
    </td>
    <td class="border px-4 py-2 text-md">
      {{
        break_time && break_time.length > 0
            ? (break_time.find(s => s.store_id === store.id) || {}).total
            : 'No Data'
      }}
    </td>
  </tr>
</template>

<script>
export default {
  name: 'TableRow',
  props: {
    store: Object,
    sales: Array,
    jolt: Array,
    hme: Array,
    till: Array,
    hourly: Array,
    break_time: Array
  },
  methods: {
    secondsToMMSS(seconds) {
      if (seconds) {
        const date = new Date(null)
        date.setSeconds(seconds)
        return date.toISOString().substr(14, 5)
      }
      return 'No Data'
    },
    calculateDonationPercent(store) {
      if (this.sales && this.sales.length > 0) {
        const salesData = this.sales.find(s => s.store_id === store.id) || {}
        let donation_percent = (salesData.donation_count / salesData.customer_count) * 100
        return donation_percent.toFixed(0)
      }
      return 'No Data'
    }
  }
}
</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
}
</style>
```
