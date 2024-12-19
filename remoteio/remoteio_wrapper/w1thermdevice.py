#!/usr/bin/env python3
from w1thermsensor import W1ThermSensor,Sensor,Unit

from time import sleep
import logging
logger=logging.getLogger(__name__)

class W1ThermDevice(W1ThermSensor):
    '''
    Wrapper class of w1ThermSensor for the use with remoteio

    Parameter are those of class W1ThermSensor:

    2 positional parameter

    Parameters:
        sensor_type: Sensor | None = None,
        sensor_id: str | None = None,                         
        *
        offset: float = 0,
        offset_unit: Unit = Unit.DEGREES_C,
        calibration_data: CalibrationData | None = None
    '''
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs) 
    
    @property
    def value(self):
        '''
        returns:
            float: temperature in Unit.DEGREES_C
        '''
        return self.get_temperature()
    @property
    def resolution(self):
        '''
        returns:
            int: sensor resolution from 9 to 12 bits
        '''
        return self.get_resolution()
    @property
    def available_sensors(self):
        '''
        Returns all available sensors.

        Parameters
        types : list
        the type of the sensor to look for. If types is None it will search for all available types.

        Returns
        list
        a list of sensor instances
        '''
        return self.get_available_sensors()
   
if __name__=='__main__':
    import logging
    # instantiate logger
    logging.basicConfig(level=logging.INFO,style="{",format="{asctime} {name}: [{levelname:8}]{message}")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info('start')
    
    sensor=W1ThermDevice()
    sensor=W1ThermDevice(sensor_type=Sensor.DS18B20, sensor_id='00000cb6ad51')
    #print(getFunctions(sensor))
    #print(getReadOnlyProperties(sensor))
    #print(getWriteableProperties(sensor))
    print(sensor.get_available_sensors())
    print(f"Resolution: {sensor.resolution}")
    while True:
        temperature = sensor.value
        print("The temperature is %s celsius" % temperature)
        sleep(1)
##################################################################################################