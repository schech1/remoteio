import time
from remoteio.remoteio_helper import *
from w1thermsensor import W1ThermSensor, Unit,Sensor
class W1Device(W1ThermSensor):
    '''
    class W1ThermSensor(
        sensor_type: Sensor | None = None,
        sensor_id: str | None = None,
        *                                          # 2 positional parameter therefore * added to show this
        offset: float = 0,
        offset_unit: Unit = Unit.DEGREES_C,
        calibration_data: CalibrationData | None = None
    )'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    @property
    def value(self):
        return self.get_temperature()
    @property
    def resolution(self):
        return self.get_resolution()
    @property
    def available_sensors(self):
        return self.get_available_sensors()
   
   
         
if __name__=='__main__':
    sensor=W1Device()
#    sensor=W1Device(sensor_type=Sensor.DS18B20, sensor_id='00000cb6ad51')
#    print(getFunctions(sensor))
#    print(getReadOnlyProperties(sensor))
#    print(getWriteableProperties(sensor))
    print(sensor.get_available_sensors())
    print(f"Resolution: {sensor.resolution}")
#    while True:
#        temperature = sensor.value
#        print("The temperature is %s celsius" % temperature)
#        time.sleep(1)