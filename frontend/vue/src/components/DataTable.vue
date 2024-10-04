<script setup>
import { ref, onMounted, computed } from 'vue'

const data = ref([])
const loading = ref(true)

// sensors api
//   "1048609": { // sensor ID
//   "metrics": { // sensor metrics
//   "1": { // metric ID (corresponds to metrics.json item ID)
//   "t": 1565155052, // timestamp
//   "v": 21.8 // value
//   }
//   },
//   "name": "Sensor 1", // sensor name
//   "type": 1, // sensor type (corresponds to sensorTypes.json)
//   "variant": 8 // sensor variant (corresponds to sensorTypes.json)
//   },

onMounted(async () => {
    const response = await fetch('http://localhost:8000/api/sensors/')
    const responseData = await response.json()
    data.value = responseData
    loading.value = false
})

const metrics = ref([])
const metricsLoading = ref(true)

onMounted(async () => {
    const response = await fetch('http://localhost:8000/api/metrics/')
    const responseData = await response.json()
    metrics.value = responseData
    metricsLoading.value = false
})

const sensorTypes = ref([])
const sensorTypesLoading = ref(true)

onMounted(async () => {
    const response = await fetch('http://localhost:8000/api/sensor-types/')
    const responseData = await response.json()
    sensorTypes.value = responseData
    sensorTypesLoading.value = false
})



// Required columns in the table:
// Sensor name from the sensors api call
// Columns of metric values. Column name metric name + active unit name from metric api and value is
// measurement value from sensor api
// It should be possible to sort records in ascending or descending order, by any column
// Must have a search input field to search for entries in the table by sensor name
// It should be possible to filter table entries by sensor type name
// It should be possible to show/disable the display of certain metric value columns
// The sensor may not have the correct name, the sensor type information in the sensorTypes api may be missing, etc. Handling of such cases will be evaluated
// in the program code

// sensors api
//   "1048609": { // sensor ID
//   "metrics": { // sensor metrics
//   "1": { // metric ID (corresponds to metrics.json item ID)
//   "t": 1565155052, // timestamp
//   "v": 21.8 // value
//   }
//   },
//   "name": "Sensor 1", // sensor name
//   "type": 1, // sensor type (corresponds to sensorTypes.json)
//   "variant": 8 // sensor variant (corresponds to sensorTypes.json)
//   },

// metrics api
//{
//   "data":{
//   "lang":"en",
//   "currentItemCount":1,
//   "items":[ // metrics list
//   {
//       "id":"1", // metrics ID
//       "name":"Temperature", // metrics name
//       "units":[ // metrics units of measurement
//           {
//               "id":"1", // measurement unit ID
//               "name":"°C", // measurement unit name
//               "precision":2,
//               "selected":true // default measurement unit
//           },
//   {
//   "id":"101",
//   "name":"°F",
//   "precision":2
//   },
//   {
//   "id":"102",
//   "name":"K",
//   "precision":2
//}
//]
//}
//]
//}
//}

// sensorTypes api
//{
//    "1":{ // sensor type
//    "8":{ // sensor variant
//    "name":"T/RH Sensor" // sensor type name
//    }
//    }
//}

// search
const search = ref('')

const filteredData = computed(() => {
    return data.value.filter((item) => {
        return item.name.toLowerCase().includes(search.value.toLowerCase())
    })
})

const sortColumn = ref('')
const sortDirection = ref('asc')
// sorting by column
const sortedData = computed(() => {
    if (sortColumn.value) {
        return filteredData.value.slice().sort((a, b) => {
            let result;
            if (sortColumn.value === 'name') {
                result = a[sortColumn.value].localeCompare(b[sortColumn.value]);
            } else {
                const aValue = a.metrics[sortColumn.value]?.v;
                const bValue = b.metrics[sortColumn.value]?.v;
                if (aValue == null) return 1; // Put 'N/A' at the bottom
                if (bValue == null) return -1; // Put 'N/A' at the bottom
                result = aValue - bValue;
            }
            return sortDirection.value === 'asc' ? result : -result;
        });
    } else {
        return filteredData.value;
    }
});

const handleSort = (column) => {
    if (sortColumn.value === column) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
    } else {
        sortColumn.value = column;
        sortDirection.value = 'asc';
    }
};

// select by sensor type
const selectedSensorType = ref(null)
const filteredByType = computed(() => {
    if (selectedSensorType.value) {
        // given an id for sensor type id get from the sensorType its type and variant
        const type = sensorTypes.value.find((sensorType) => sensorType.id === selectedSensorType.value)?.type;
        const variant = sensorTypes.value.find((sensorType) => sensorType.id === selectedSensorType.value)?.variant;
        return sortedData.value.filter((item) => {
            return item.type === type && item.variant === variant
        })
    } else {
        return sortedData.value
    }
});

// toggle columns
const handleToggleColumns = computed(() => {
    return (metric) => {
        const metricColumn = document.querySelector(`[column="${metric.id}"]`);
        console.log(metricColumn);
        if (metricColumn.style.display === 'none') {
            metricColumn.style.display = 'table-cell';
        } else {
            metricColumn.style.display = 'none';
        }
        // remove the values from the rows that are not displayed in the table
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach((row) => {
            const value = row.querySelector(`[value="${metric.id}"]`);
            if (metricColumn.style.display === 'none') {
                value.style.display = 'none';
            } else {
                value.style.display = 'table-cell';
            }
        });
    }
});


</script>

<template>
    <div>
        <label for="selectSensorType">Select sensor type:</label>
        <select id="selectSensorType" v-model="selectedSensorType" class="form-select">
            <option :value="null">All</option>
            <option v-for="sensorType in sensorTypes" :key="sensorType.id" :value="sensorType.id">
                {{ sensorType.name }}
            </option>
        </select>
    </div>
    <div id="toggleColumns" class="dropdown mt-3 p-1">
        <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">Toggle Columns</button>
        <ul class="dropdown-menu">
            <li v-for="metric in metrics" :key="metric.id" class="dropdown-item">
                <label>
                    <input type="checkbox" :value="metric.id" @change="handleToggleColumns(metric)" checked/>
                    {{ metric.name }}
                </label>
            </li>
        </ul>
    </div>
    <table class="table">
        <thead>
            <tr>
                <th scope="col"> 
                    <div style="display: flex; align-items: center;">
                        Name 
                        <input type="text" v-model="search" placeholder="Search by name" style="margin-left: 10px;">
                        <button class="btn btn-secondary" @click="handleSort('name')" style="margin-left: 10px;">Sort</button>
                    </div>
                </th>
                <th scope="col" v-for="metric in metrics" :column="metric.id" :key="metric.id">
                    <div style = "display: flex; align-items: center;">
                        {{ metric.name }} ({{ metric.units.find((unit) => unit.selected).name }})
                        <button class="btn btn-secondary" @click="handleSort(metric.id)">Sort</button>
                    </div>
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in filteredByType" :key="item.id">
                <th scope="row">{{ item.name }} ({{ item.type_variant_name }})</th>
                <td v-for="metric in metrics" :key="metric.id" :value="metric.id">
                    {{ item.metrics[metric.id] ? item.metrics[metric.id].v : 'N/A' }}
                </td>
            </tr>
        </tbody>        
    </table>
</template>