from remoteio import RemoteServer
import time
import logging

    
try:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name="remoteio")
    raspi1='raspy5' 
    # erstellt virtuelle Pins auf 2 verschiedenen Raspberry Pis
    remote_pi=None
    remote_pi=RemoteServer(raspi1)
    # 'g ': BCM -B e z e i c h n u n g ( G P I O 2 1 )
    remote_pin=remote_pi.pin(21,'g')
    remote_pin1=remote_pi.pin(20,'g')
    remote_pin2=remote_pi.pin(16,'g')


    

    remote_pin.on(time_ms=10000)
    remote_pin1.pulse(time_ms=10000)
    remote_pin2.blink(time_ms=10000)
    remote_pi.execute()
    time.sleep(15.0)

    
    remote_pin.on(time_ms=20000)
    remote_pi.execute()
    while True:
        pass
except Exception as e:
    logger.info(str(e))
finally:
    if remote_pi:
        remote_pi.close()