<template>
  <div class="mx-5 mb-8">
    <div class="flex flex-col md:flex-row">
      <ChartInputSelector v-if="stores.length > 1" @selection-changed="handleSelectionChanged" class="mb-4 md:mb-0" :stores="stores"/>
      <div class="flex-grow max-w-full overflow-auto bg-white p-4 rounded-lg">
        <Line
            v-if="labels.length > 0 && datasets.length > 0"
            id="my-chart-id"
            :options="chartOptions"
            :data="{labels, datasets}"
        />
      </div>
    </div>
  </div>
</template>


<script>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import {supabase} from "@/supabase";
import ChartInputSelector from "@/components/ChartInputSelector";
import {dataMixin} from "@/mixins";
import _ from 'lodash'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

// const colorOptions = [{ borderColor: '#36A2EB', backgroundColor: '#9BD0F5' }, { borderColor: '#FFCE56', backgroundColor: '#FFCE56' }]

export default {
  name: 'TrendsComponent',
  mixins: [dataMixin],
  components: { ChartInputSelector, Line },
  data: () => ({
    labels: [],
    datasets: [],
    chartOptions: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Date'
          }
        },
        y: {
          title: {
            display: true,
            text: ''
          }
        }
      }
    },
    stores: [],
  }),
  methods: {
    handleSelectionChanged(selection) {

      // build the query
      const query = supabase
          .from(`${this.tables[selection.metric]}`)
          // select the correct metric
          .select(`date, ${selection.metric}, store_id`)
          // filter by location
          .in('store_id', selection.stores)
          // filter by date (needs to be in iso format)
          .gte('date', new Date(new Date().setDate(new Date().getDate() - selection.days)).toISOString())
          // order by date
          .order('date', {ascending: true})

      // fetch the data
      query.then(({data, error}) => {
        if (error) {
          console.error('Error fetching data:', error)
          return
        }
        // transform the data (no duplicates)
        this.labels = [...new Set(data.map(d => d.date))]

        // first split by store_id
        const splitData = data.reduce((acc, curr) => {
          if (!acc[curr.store_id]) {
            acc[curr.store_id] = []
          }
          acc[curr.store_id].push(curr)
          return acc
        }, {})

        // create the datasets
        this.datasets = Object.keys(splitData).map((key) => {
          // store
          const store = this.stores.find(store => store.id.toString() === key)
          return {
            label: `${store.name}`,
            data: splitData[key].map(d => d[selection.metric]),
            borderColor: `${store.borderColor}`,
            backgroundColor: `${store.backgroundColor}`,
          }
        })

        // update the y-axis title (use metrics from the mixin)
        const yTitle = this.metrics.find(m => m.value === selection.metric).text
        this.chartOptions = _.cloneDeep(this.chartOptions)
        this.chartOptions.scales.y.title.text = yTitle

      })
    },
    async getStores() {
      const {data: stores, error} = await supabase.from('store').select('*')
      if (error) {
        console.error('Error fetching stores:', error)
        return
      }
      // add the colors form the mixin
      // the colors are in an object with the store id as key
      this.stores = stores.map(store => {
        const color = this.storeProperties[store.id]
        return {
          ...store,
          borderColor: color.borderColor,
          backgroundColor: color.backgroundColor
        }
      })
    }
  },
  created() {
    this.getStores()
  }
}
</script>
