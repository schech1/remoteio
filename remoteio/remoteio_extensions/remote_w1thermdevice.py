#!/usr/bin/env python3
from w1thermsensor import Sensor    # hidden in x=eval(x) of avalable_sensors

from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)


class Remote_W1ThermDevice(RemoteDigitalDevice):
    '''
    class Remote_W1ThermDevice(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class W1ThermDevice(
        sensor_type: Sensor | None = None,
        sensor_id: str | None = None,
        offset: float = 0,
        offset_unit: Unit = Unit.DEGREES_C,
        calibration_data: CalibrationData | None = None
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            kwargs['args']=args
        super().__init__(remote_server,'W1ThermDevice', **kwargs)

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
        x=x.replace('W1ThermDevice','self.fas')
        x=eval(x)
        return x
    
if __name__=='__main__':
    
    #from remoteio import getFunctions,getReadOnlyProperties,getWriteableProperties
    #print(getFunctions(sensor))
    #print(getReadOnlyProperties(sensor))
    #print(getWriteableProperties(sensor))

    try:
        from signal import pause
        from time import sleep

        import logging
        logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
        logger = logging.getLogger(name="remoteio")
        logger.setLevel(logging.INFO)

        from remoteio import RemoteServer,Remote_LED
        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)

        sensor=Remote_W1ThermDevice(rs)
        print(sensor.available_sensors)
        sensor=Remote_W1ThermDevice(rs,sensor_type='Sensor.DS18B20', sensor_id="'00000cb6ad51'")
        
        
        print(f"Resolution: {sensor.resolution}")
        print(f"available_sensors: {sensor.available_sensors}")
        #while True:
        #    temperature = sensor.value
        #    print(type(temperature))
        #    print("The temperature is %s celsius" % temperature)
        #    sleep(1) 
        # 
        RLED=Remote_LED(rs,21)
        temp_gen_delay=0.5
        def temp_gen():
            while True:
                try:
                    sleep(temp_gen_delay)
                    if sensor.value>30:
                        yield 1
                    else:
                        yield 0
                except:
                    break

        RLED.source=temp_gen 
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")