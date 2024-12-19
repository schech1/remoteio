#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)

class Remote_WRADS1115(RemoteDigitalDevice):
    '''
    class Remote_WRADS1115(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class WRADS115(
        *channelNr,
        **kwargs
    )
    class ADS1115(
        i2c: ADS1115.I2C,
        *,
        gain: float = 1,
        data_rate: ADS1115.Optional[int] = None,
        mode: int = ADS1115.Mode.SINGLE,
        address: int = ADS1115._ADS1X15_DEFAULT_ADDRESS,
        ):
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            kwargs['args']=args
        super().__init__(remote_server,'WRADS1115', **kwargs)

        self._source_delay=0.01
        self._genVoltage_delay=0.01

    @property
    def value(self):
        try:
            return eval(self.getProperty(getFunctionName()))
        except:
            return (None,None)
    @property
    def address(self):
        return self.getProperty(getFunctionName())
    ######################################################
    ## the generator 'values' is defined in the super class
    ## also value 
    #######################################################
    def genVoltage(self):
        ## only for positive volt
        from time import sleep
        while True:
            try:
                sleep(self._genVoltage_delay)
                yield max(min(self.value[1]/3.3, 1),0)
            except:
                break

if __name__ == '__main__':
    try:
        from signal import pause
        from time import sleep

        import logging
        logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
        logger = logging.getLogger(name="remoteio")
        logger.setLevel(logging.INFO)

        from remoteio.remoteio_client import RemoteServer
        from remoteio.remoteio_devices.remote_pwmled import Remote_PWMLED
        from remoteio.remoteio_extensions.remote_kontext import Remote_Kontext
        from remoteio.remoteio_extensions.remote_mcp49xx import Remote_MCP4811
        
        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)


        rads=Remote_WRADS1115(rs,0,address=0x48,gain=1)
        rads1=Remote_WRADS1115(rs,0,1,address=0x48)
        rmcp=Remote_MCP4811(rs,device=1,max_speed_hz=250000)  # used instead of a potentiometer
        rmcp.gain=1 
    
     
    
        #pause()
        print(rads.value[1])
        print(rads.address)
        print(rads1.value)
        rl=Remote_PWMLED(rs,21)
        #l=PWMLED(21)  # client side !!
        rads._genVoltage_delay=0.1
        rl.source=rads.genVoltage  #  rl.source=rads.genVoltage is possible too for remote device rl
        #l.source=rads.gen_Voltage()   #  l.source=rads.genVoltage is not possible for client device l
        rst=Remote_Kontext(rl,rads,rads1)
        rl.setClientIdent('rl')
        rads.setClientIdent('rads')
        rads1.setClientIdent('rads1')

        ## by evoquing rst.value the values of all children are calculated and are
        ## memorized in rst._value as actual state of rst
        


        while True:
            sleep(0.5)
            rmcp.value=0
            print(rst.value)
            sleep(0.5)
            rmcp.value=1023
            print(rst.value)
            
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")