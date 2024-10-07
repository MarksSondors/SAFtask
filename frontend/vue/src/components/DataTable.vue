<script setup>
import { ref, onMounted, computed } from 'vue'

const data = ref([])
const loading = ref(true)

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