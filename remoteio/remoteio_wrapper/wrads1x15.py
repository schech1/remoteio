##################################################################################################
import board
import busio
from Adafruit_ADS1x15.ADS1x15 import ADS1x15_DEFAULT_ADDRESS
import adafruit_ads1x15.ads1115 as ads
from adafruit_ads1x15.analog_in import AnalogIn

from time import sleep
import logging
logger=logging.getLogger(__name__)

class WRADS1115(ads.ADS1115):
    """
    The ADS1115 a/d-converter has 4 channels 0,1,2,3
    The library of adafruit is used here.

    Results:
    ret(list): (value,voltage) and (None,None)

    """
    def __init__(self,*channelNr,**kwargs):
        '''
        class ADS1115(
        i2c: ADS1115.I2C,
        *,
        gain: float = 1,
        data_rate: ADS1115.Optional[int] = None,
        mode: int = ADS1115.Mode.SINGLE,
        address: int = ADS1115._ADS1X15_DEFAULT_ADDRESS,
        ):
        '''
        self._address=None
        if 'address' in kwargs.keys():
            self._address=kwargs['address']
        else:
            self._address= ADS1x15_DEFAULT_ADDRESS  

        i2c=busio.I2C(board.SCL,board.SDA)
        super().__init__(i2c,**kwargs)  
        # Define the analog input channel
        self.channel = AnalogIn(self,*channelNr)
        
        ## time for initializing ADS115, necessary
        sleep(0.001)

    @property
    def value(self):  
        return (self.channel.value,self.channel.voltage)
    @property
    def address(self):  
        return self._address

####################################################


if __name__=='__main__':
    from signal import pause

    from time import sleep 
    import logging
    # instantiate logger
    logging.basicConfig(level=logging.INFO,style="{",format="{asctime} {name}: [{levelname:8}]{message}")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info('start')

    try:
        ## *channels as positonal parameter, one channel for single mode, two channels for differential mode
        ads0=WRADS1115(0,address=int(0x48))
        ads1=WRADS1115(0,1,address=int(0x48))
        ads2=WRADS1115(2,address=int(0x48))
        #print(hex(ads0.address))
        i=0
        while True:
            print(ads0.value)
            print(ads1.value)
            print(ads2.value)
            #if i==10:ads1.close()
            sleep(0.5)
            i=i+1
        #pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")

