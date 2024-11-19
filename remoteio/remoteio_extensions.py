#!/usr/bin/env python3

from remoteio import RemoteDigitalDevice
from remoteio import RemoteServer
from remoteio import getFunctionName,shortestWay,map_bg,getName
from remoteio import getFunctions,getReadOnlyProperties,getWriteableProperties
from gpiozero import *
from signal import pause
from time import sleep
import logging
logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")
logger.setLevel(logging.INFO)
#################################################################################################################
# 
from w1thermsensor import Sensor    # hidden in eval of avalable_sensors
class Remote_W1Device(RemoteDigitalDevice):
    '''
    class W1ThermSensor(
        sensor_type: Sensor | None = None,
        sensor_id: str | None = None,
        offset: float = 0,
        offset_unit: Unit = Unit.DEGREES_C,
        calibration_data: CalibrationData | None = None
    )'''
    def __init__(self, remote_server,*args,**kwargs):
        if args!=():
            kwargs['args']=args
        super().__init__(remote_server,'W1Device', **kwargs)

        self._source_delay=0.01
        
    ######################################################
    ## the generator 'values' is defined in the super class
    ## value is read only, therefore the value attribute 
    ## from superclass is here overwritten
    @property
    def value(self):
        return RemoteDigitalDevice.value.fget(self)
    #######################################################   
    @property
    def resolution(self):
        return self.getProperty(getFunctionName())
    #######################################################
    def fas(self,**kwargs):
        return tuple(kwargs.values())
    @property
    def available_sensors(self):
        x= self.getProperty(getFunctionName())
        x=x.replace('W1Device','self.fas')
        x=eval(x)
        return x
    #########################################################      
if __name__=='__main__':
    #from w1thermsensor import Sensor 

    server_ip = "192.168.178.136"
    server_port = 8509
    # Create instance of remote Raspberry Pi
    rs = RemoteServer(server_ip, server_port)
    sensor=Remote_W1Device(rs)
    print(sensor.available_sensors)

    sensor=Remote_W1Device(rs,sensor_type='Sensor.DS18B20', sensor_id="'00000cb6ad51'")
    #print(getFunctions(sensor))
    #print(getReadOnlyProperties(sensor))
    #print(getWriteableProperties(sensor))
    
    print(f"Resolution: {sensor.resolution}")
    print(f"available_sensors: {sensor.available_sensors}")
    while True:
        temperature = sensor.value
        print("The temperature is %s celsius" % temperature)
        sleep(1)   