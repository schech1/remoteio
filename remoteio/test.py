try:
    x="{'available_sensors' : ""[W1Device(sensor_type=Sensor.DS18B20, sensor_id='00000cb6ad51')]""}"
    x="{'available_sensors' : " + "[W1Device(sensor_type=Sensor.DS18B20, sensor_id='00000cb6ad51')]" + "}"
    print(x)
except Exception as e:
    print(e)