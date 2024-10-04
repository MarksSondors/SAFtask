from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from json import loads

# sensors.json
#   "1048609": { // sensor ID
#   "metrics": { // sensor metrics
#   "1": { // metric ID (corresponds to metrics.json item ID)
#   "t": 1565155052, // timestamp
#   "v": 21.8 // value
#   }
#   },
#   "name": "Sensor 1", // sensor name
#   "type": 1, // sensor type (corresponds to sensorTypes.json)
#   "variant": 8 // sensor variant (corresponds to sensorTypes.json)
#   },

# metrics.json
#{
#   "data":{
#   "lang":"en",
#   "currentItemCount":1,
#   "items":[ // metrics list
#   {
#       "id":"1", // metrics ID
#       "name":"Temperature", // metrics name
#       "units":[ // metrics units of measurement
#           {
#               "id":"1", // measurement unit ID
#               "name":"°C", // measurement unit name
#               "precision":2,
#               "selected":true // default measurement unit
#           },
#   {
#   "id":"101",
#   "name":"°F",
#   "precision":2
#   },
#   {
#   "id":"102",
#   "name":"K",
#   "precision":2
#}
#]
#}
#]
#}
#}

# sensorTypes.json
#{
#    "1":{ // sensor type
#    "8":{ // sensor variant
#    "name":"T/RH Sensor" // sensor type name
#    }
#    }
#}

class SensorList(APIView):
    def get(self, request):
        with open('data/sensors.json') as f:
            sensors = loads(f.read())
        with open('data/sensorTypes.json') as f:
            sensorTypes = loads(f.read())
        
        sensors_list = []
        for sensor_id, sensor_data in sensors.items():
            sensor_data['id'] = sensor_id
            sensor_data['type'] = str(sensor_data['type'])
            sensor_data['variant'] = str(sensor_data['variant'])
            if sensor_data['name'] != 'Sensor ' + str(len(sensors_list) + 1):
                sensor_data['name'] = 'Sensor ' + str(int(sensors_list[-1]['name'].split(' ')[1]) + 1)
            # get name of sensor type variant name
            if str(sensor_data['type']) in sensorTypes and str(sensor_data['variant']) in sensorTypes[str(sensor_data['type'])]:
                sensor_data['type_variant_name'] = sensorTypes[str(sensor_data['type'])][str(sensor_data['variant'])]['name']
            else:
                sensor_data['type_variant_name'] = 'Unknown'
            sensors_list.append(sensor_data)
        
        return Response(sensors_list)

class MetricsList(APIView):
    def get(self, request):
        with open('data/metrics.json') as f:
            metrics = loads(f.read())
        
        metrics_list = []
        for metric in metrics['data']['items']:
            metric['id'] = metric['id']
            metrics_list.append(metric)
        return Response(metrics_list)

class SensorTypesList(APIView):
    def get(self, request):
        with open('data/sensorTypes.json') as f:
            sensorTypes = loads(f.read())
        
        sensorTypes_list = []
        for sensorType in sensorTypes:
            for sensorVariant in sensorTypes[sensorType]:
                sensorTypes_list.append({
                    'id': str(len(sensorTypes_list) + 1),
                    'type': sensorType,
                    'variant': sensorVariant,
                    'name': sensorTypes[sensorType][sensorVariant]['name']
                })
            
        return Response(sensorTypes_list)