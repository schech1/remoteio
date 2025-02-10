#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteSupervisor
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName,getBit

from time import sleep
import logging
logger = logging.getLogger(__name__)

##################################################
# class Remote_MCP23017
##################################################

IODIRA=0x00
IODIRB=0x01
IPOLA=0x02
IPOLB=0x03
GPINTENA=0x04
GPINTENB=0x05
DEFVALA=0x06
DEFVALB=0x07
INTCONA=0x08
INTCONB=0x09
IOCON=0x0A
#IOCON=0x0B
GPPUA=0x0C
GPPUB=0x0D
INTFA=0x0E
INTFB=0x0F
INTCAPA=0x10
INTCAPB=0x11
GPIOA=0x12
GPIOB=0x13
OLATA=0x14
OLATB=0x15

class Remote_MCP23x17(RemoteDigitalDevice):
    MCPDICT={'i2c':'MCP23017','spi':'MCP23S17'}
    def __init__(self,remote_server,bus_type,*args,**kwargs):
        assert bus_type in ('i2c','spi'),f"bus_type {bus_type} not supported"
        
        if args!=():
            kwargs['args']=args  
        remote_name=Remote_MCP23x17.MCPDICT[bus_type]
        super().__init__(remote_server,remote_name, **kwargs)
       
        self.buttonList=[None for i in range(16)]    
        self.ledList=[None for i in range(16)]         
        self.reset()
    ############################################
    def reset(self):
        kwargs={}
        self.func_exec(getFunctionName(),**kwargs)

    def setRegister(self,register,daten):
        kwargs={'register':register, 'daten':daten}
        self.func_exec(getFunctionName(),**kwargs)

    def setRegisterBit(self,register,bitNr,flag): 
        kwargs={'register':register, 'bitNr':bitNr, 'flag':flag}
        self.func_exec(getFunctionName(),**kwargs)

    def set_hold_repeat(self,pinNr,wert):
        kwargs={'pinNr':pinNr, 'hold_repeat':wert}
        self.func_exec(getFunctionName(),**kwargs)

    def set_hold_time(self,pinNr,wert):
        kwargs={'pinNr':pinNr, 'hold_time':wert}
        self.func_exec(getFunctionName(),**kwargs)

    def set_value(self,pinNr,wert):
        kwargs={'pinNr':pinNr, 'val':wert}
        self.func_exec(getFunctionName(),**kwargs)

    def create_MCPButton(self,pinNr,bounce_time):
        kwargs={'pinNr':pinNr,'bounce_time':bounce_time}
        self.func_exec(getFunctionName(),**kwargs)
    
    def create_MCPLED(self,pinNr):
        kwargs={'pinNr':pinNr}
        self.func_exec(getFunctionName(),**kwargs)

    ####################################################
    def on(self,pinNr,**kwargs):
        kwargs={'pinNr':pinNr} | kwargs
        self.func_exec(getFunctionName(),**kwargs)
    def off(self,pinNr,**kwargs):
        kwargs={'pinNr':pinNr} | kwargs
        self.func_exec(getFunctionName(),**kwargs)
    def toggle(self,pinNr,**kwargs):
        kwargs={'pinNr':pinNr} | kwargs
        self.func_exec(getFunctionName(),**kwargs)
    def blink(self,pinNr,**kwargs):
        kwargs={'pinNr':pinNr} | kwargs
        self.func_exec(getFunctionName(),**kwargs) 
    ###################################################################################
    # the following properties furnish a 16-bit word for GPB7,...,0, GPA7,...,GPA0-Pins
    # value, values in superclass also 16-bit
    ###################################################################################
    @property
    def iodir(self):
        return self.getProperty(getFunctionName())
    @iodir.setter
    def iodir(self,wert):
        self.func_exec('set',iodir=wert)
    @property
    def ipol(self):
        return self.getProperty(getFunctionName())
    @ipol.setter
    def ipol(self,wert):
        self.func_exec('set',ipol=wert)
    @property
    def gpinten(self):
        return self.getProperty(getFunctionName())
    @gpinten.setter
    def gpinten(self,wert):
        self.func_exec('set',gpinten=wert)
    @property
    def defval(self):
        return self.getProperty(getFunctionName())
    @defval.setter
    def defval(self,wert):
        self.func_exec('set',defval=wert)
    @property
    def intcon(self):
        return self.getProperty(getFunctionName())
    @intcon.setter
    def intcon(self,wert):
        self.func_exec('set',intcon=wert)
    @property
    def iocon(self):
        return self.getProperty(getFunctionName())
    @iocon.setter
    def iocon(self,wert):
        self.func_exec('set',iocon=wert)
    @property
    def gppu(self):
        return self.getProperty(getFunctionName())
    @gppu.setter
    def gppu(self,wert):
        self.func_exec('set',gppu=wert)
    @property
    def intf(self):
        return self.getProperty(getFunctionName())
    @intf.setter
    def intf(self,wert):
        self.func_exec('set',intf=wert)
    @property
    def intcap(self):
        return self.getProperty(getFunctionName())
    @intcap.setter
    def intcap(self,wert):
        self.func_exec('set',intcap=wert)
    @property
    def gpio(self):
        return self.getProperty(getFunctionName())
    @gpio.setter
    def gpio(self,wert):
        self.func_exec('set',gpio=wert)
    @property
    def olat(self):
        return self.getProperty(getFunctionName())
    @olat.setter
    def olat(self,wert):
        self.func_exec('set',olat=wert)
    
    ##################################
    @property
    def is_held(self):
        return self.getProperty(getFunctionName())
    @property
    def hold_time(self):
        return self.getProperty(getFunctionName()) 
    @property
    def hold_repeat(self):
        return self.getProperty(getFunctionName())
    ######################################################
    ######################################################
    
    def close(self):
        for button in self.buttonList:
            if button!=None:
                RemoteSupervisor.delIdent(button.ident)
        for led in self.ledList:
            if led != None:
                RemoteSupervisor.delIdent(led.ident)
        self.buttonList=[None for i in range(16)]    
        self.ledList=[None for i in range(16)]         
        self.reset()
        # This is the call to the original close method of superclass
        RemoteDigitalDevice.close(self)
        
       
##############################################################
# class MCP23017
##############################################################    
class Remote_MCP23017(Remote_MCP23x17):
    def __init__(self,remote_server,*args,**kwargs):
        super().__init__(remote_server,'i2c',*args,**kwargs)
##############################################################
# class MCP23017
############################################################## 
class Remote_MCP23S17(Remote_MCP23x17):
    def __init__(self,remote_server,*args,**kwargs):
        super().__init__(remote_server,'spi',*args,**kwargs)
##################################################
# class RMCPLED
##################################################
from time import sleep
from threading import Thread
from multiprocessing import Lock,Event
from typing import Generator
from inspect import isgeneratorfunction, signature, isfunction,ismethod
class RMCPLED:
    def __init__(self,rmcp:Remote_MCP23x17,pinNr:int):
        self._mcp=rmcp
        self._pinNr=pinNr
        if self._mcp.buttonList[self._pinNr]!= None or \
            self._mcp.ledList[self._pinNr]!= None:
            raise ValueError(f"Pin {self._pinNr} of Remote_MCP23017 {self._mcp} is busy")
        
        self._mcp.create_MCPLED(self._pinNr)
        self.ident=RemoteSupervisor.genServerIdent()
        self.setClientIdent(self.ident)
        
        self._mcp.setRegisterBit(GPPUA+self._pinNr//8,self._pinNr%8,0)
        self._mcp.setRegisterBit(IODIRA+self._pinNr//8,self._pinNr%8,0)
        self._mcp.ledList[pinNr] = self
        self._source_delay=0.001
        self._source=None
        self._sourceEvent=Event()
        self._sourceThread=None

    def getClientIdent(self):
        return RemoteSupervisor._ident_dict[self.ident]
    def setClientIdent(self,ident):
        RemoteSupervisor.setClientIdent(self.ident,ident)
####################################################################
## property source
####################################################################
    @property
    def source(self):
       ## time needed for aborting source_function-thread
        #sleep(0.002)
        return self._source
    @source.setter
    def source(self, quelle): 
        if self._sourceThread !=None:
            #soft kill of thread
            self._sourceEvent.set()
            while self._sourceEvent.is_set():
                pass
            self._source=None
            self._sourceThread = None
        if quelle==None:   
            return
        self._sourceThread=Thread(target=self.source_function, args=(quelle,self._sourceEvent),)
        self._sourceThread.start() 
        self._source=quelle
        

    def source_function(self,quelle,ev):
        ## infinite generator expected
        try:
            old_value=None    
            xxx=None           
            if isinstance(quelle,Generator):
                    xxx=quelle
            if isgeneratorfunction(quelle):
                        xxx=quelle()
            if xxx==None:
                xxx=quelle.values
                    
            for wert in xxx:
                if self._mcp.ledList[self._pinNr]==None:
                    return
                if wert!=old_value:
                    if wert!= None:
                        self.value=wert
                        old_value=wert
                    else:
                        logger.info(f"RMCPLED: source furnishes value None")
                if ev.is_set():
                    break
                    
        except Exception as e:
            logger.error(str(e))
        finally:
            ev.clear()
            logger.info("source thread terminated")

    ##############################################
    @property
    def values(self):
        """
        #nfinite generator for use of rMCPButton as source
        """
        while True:
            try:
                sleep(self._source_delay)
                yield self.value
            except:
                break
    ###############################################        
    @property
    def value(self):
        daten=self._mcp.value
        if daten!=None:
            if self._pinNr>=8:
                daten=(daten>>8) & 0xFF
            else:
                daten=daten & 0xFF
            return getBit(self._pinNr%8,daten) 
        else:
            return None
    @value.setter
    def value(self,wert):
        assert wert in (0,1), f"'value': only 0,1 allowed but not {wert}" 
        self._mcp.set_value(self._pinNr,wert)
    
    ###############################################        
    @property
    def iodir(self):
        daten=self._mcp.iodir
        if daten==None: return None
        if self._pinNr>=8:
            daten=(daten>>8) & 0xFF
        else:
            daten=daten & 0xFF
        return getBit(self._pinNr%8,daten) 
    @iodir.setter
    def iodir(self,wert):
        assert wert in (0,1), "'iodir': only 0,1 allowed" 
        register=0x00 + self._pinNr//8
        bitNr=self._pinNr%8
        self._mcp.setRegisterBit(register,bitNr,wert) 
        ###############################################        
    @property
    def gppu(self):
        daten=self._mcp.gppu
        if daten==None: return None
        if self._pinNr>=8:
            daten=(daten>>8) & 0xFF
        else:
            daten=daten & 0xFF
        return getBit(self._pinNr%8,daten) 
    @gppu.setter
    def gppu(self,wert):
        assert wert in (0,1), "'gppu': only 0,1 allowed" 
        register=0x00 + self._pinNr//8
        bitNr=self._pinNr%8
        self._mcp.setRegisterBit(register,bitNr,wert) 

    @property
    def is_active(self):
        return self.value==1


    def blink(self,**kwargs):
        self._mcp.blink(self._pinNr,**kwargs)
    def on(self,**kwargs):
        self._mcp.on(self._pinNr,**kwargs)
    def off(self,**kwargs):
        self._mcp.off(self._pinNr,**kwargs)
    def toggle(self,**kwargs):
        self._mcp.toggle(self._pinNr,**kwargs)
    
##################################################
# class RMCPButton
##################################################
from threading import Thread
from inspect import signature 
class RMCPButton:
    def __init__(self,rmcp:Remote_MCP23x17,pinNr:int,bounce_time:float=None):
        self._mcp=rmcp
        self._pinNr=pinNr
        self._bounce_time=bounce_time
        if self._mcp.buttonList[self._pinNr]!= None or \
            self._mcp.ledList[self._pinNr]!= None:
            raise ValueError(f"Pin {self._pinNr} of Remote_MCP23017 {self._mcp} is busy")
        
        self._mcp.create_MCPButton(self._pinNr,bounce_time)
        self.ident=RemoteSupervisor.genServerIdent()
        self.setClientIdent(self.ident)

        self._when_released=None
        self._when_pressed=None
        self._when_held=None
        self._stop_when_released=False
        self._stop_when_pressed=False
        self._stop_when_held=False
        self._hold_time=0
        self._hold_repeat=False
        self._source_delay=0.001
        self.gen_wait_delay=0.001
        self.gen_when_delay=0.001   
        self._mcp.buttonList[self._pinNr] = self
        ## start of threads
        twh=Thread(target=self.when_held_function, args=(),)
        self.twh=twh
        twh.start()
        twr=Thread(target=self.when_released_function, args=(),)
        self.twr=twr
        twr.start()
        twp=Thread(target=self.when_pressed_function, args=(),)
        self.twp=twp
        twp.start()


    def getClientIdent(self):
        return RemoteSupervisor._ident_dict[self.ident]
    def setClientIdent(self,ident):
        RemoteSupervisor.setClientIdent(self.ident,ident)
    ###############################################################
    ## wait_for... functions
    ################################################################  
         
    def wait_for_press(self,timeout=None):
        import time
        start=None
        if timeout!=None and timeout>0:
            start = time.perf_counter()
        while self.value==0:
            if start!=None:
                end=time.perf_counter()
                if end - start > timeout:
                    return
            sleep(self.gen_wait_delay)
            pass
        else:
            return
  
    def wait_for_release(self,timeout=None):
        import time
        start=None
        if timeout!=None and timeout>0:
            start = time.perf_counter()
        while self.value==1:
            if start!=None:
                end=time.perf_counter()
                if end - start > timeout:
                    return
            sleep(self.gen_wait_delay)
            pass
        else:
            return

    ##############################################
    @property
    def values(self):
        """
        #nfinite generator for use of rMCPButton as source
        """
        while True:
            try:
                sleep(self._source_delay)
                yield self.value
            except:
                break
    ###############################################        
    @property
    def value(self):
        daten=self._mcp.value
        if daten!=None:
            if self._pinNr>=8:
                daten=(daten>>8) & 0xFF
            else:
                daten=daten & 0xFF
            return getBit(self._pinNr%8,daten) 
        else:
            return None
    ###############################################        
    @property
    def iodir(self):
        daten=self._mcp.iodir
        if daten==None: return None
        if self._pinNr>=8:
            daten=(daten>>8) & 0xFF
        else:
            daten=daten & 0xFF
        return getBit(self._pinNr%8,daten) 
    @iodir.setter
    def iodir(self,wert):
        assert wert in (0,1), "'iodir': only 0,1 allowed" 
        register=IODIRA + self._pinNr//8
        bitNr=self._pinNr%8
        self._mcp.setRegisterBit(register,bitNr,wert) 
        ###############################################        
    @property
    def gppu(self):
        daten=self._mcp.gppu
        if daten==None: return None
        if self._pinNr>=8:
            daten=(daten>>8) & 0xFF
        else:
            daten=daten & 0xFF
        return getBit(self._pinNr%8,daten) 
    @gppu.setter
    def gppu(self,wert):
        assert wert in (0,1), "'gppu': only 0,1 allowed" 
        register=GPPUA + self._pinNr//8
        bitNr=self._pinNr%8
        self._mcp.setRegisterBit(register,bitNr,wert) 
    
    @property
    def ipol(self):
        daten=self._mcp.ipol
        if daten==None: return None
        if self._pinNr>=8:
            daten=(daten>>8) & 0xFF
        else:
            daten=daten & 0xFF
        return getBit(self._pinNr%8,daten) 
    @ipol.setter
    def ipol(self,wert):
        assert wert in (0,1), "'ipol': only 0,1 allowed" 
        register=IPOLA + self._pinNr//8
        bitNr=self._pinNr%8
        self._mcp.setRegisterBit(register,bitNr,wert) 
    
    ############################################################
    @property
    def held_time(self):
        x=self._mcp.getProperty(getFunctionName())
        if type(x)!=str:
            assert type(x)==str, f"'held_time': {x} ??" 
        liste = eval(x) 
        return liste[self._pinNr]
    #############################################################    
    @property
    def hold_repeat(self):
        return self._hold_repeat
    @hold_repeat.setter
    def hold_repeat(self,wert): 
        self._hold_repeat=wert   
    #############################################################    
    @property
    def hold_time(self):
        return self._hold_time
    @hold_time.setter
    def hold_time(self,wert): 
        self._hold_time=wert
        self._mcp.set_hold_time(self._pinNr,wert) 
    #######################################################
    @property
    def is_held(self):
        x=self._mcp.getProperty(getFunctionName())
        if type(x)!=str:
            assert type(x)==str, f"'is_held': {x} ??" 
        liste = eval(x) 
        return bool(liste[self._pinNr])
    #######################################################
    @property
    def is_pressed(self):
        return self.value==1
    @property
    def is_released(self):
        return self.value==0
    ###########################################################
    @property
    def when_pressed(self):
        return self._when_pressed
    @when_pressed.setter
    def when_pressed(self, wert):
        self._when_pressed=wert
    #############################################################
    @property
    def when_released(self):
        return self._when_released
    @when_released.setter
    def when_released(self, wert):
        self._when_released=wert
    #############################################################
    @property
    def when_held(self):
        return self._when_held
    @when_held.setter
    def when_held(self, wert):
        self._when_held=wert  
    #############################################################

    #############################################################
    ### The following generator is used in the super class.
    ### The _when_thread_function asks, whether the yields give True as response 
    #############################################################                            
    def gen_when(self,text):
        """
        A generator function
        An infinite iterator of values read from :attr:`value`, 'is_held'.
        """
        while True:
            try:                
                sleep(self.gen_when_delay)
                if text=='when_pressed':
                    yield self.is_pressed
                if text=='when_released':
                    yield self.is_released
                if text=='when_held':
                    yield self.is_held  
            except:
                break 

#######################################################################

    def when_released_function(self):
        try:
            while self._stop_when_released==False:
                if self._when_released!=None:
                    old_value = None
                    if self._mcp.buttonList[self._pinNr]==None:
                            return
                    for val in self.gen_when('when_released'):
                        if self._mcp.buttonList[self._pinNr]==None:
                            return
                        if self._stop_when_released==True:
                            return
                        if old_value==None: 
                            old_value=val
                            continue
                        if val!= old_value:
                            old_value=val
                            if val == True:
                                if self._when_released!=None:
                                    func=self._when_released
                                    if func !=None:
                                        wh=0
                                        sig = signature(func)
                                        for name, param in sig.parameters.items():
                                            if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                                wh=+1
                                                break 
                                        if wh == 0:
                                            func()
                                        else:
                                            func(self)
                                else:
                                    return

                sleep(0.001)
            else:
                return
        except Exception as e:
                logger.error(f"{str(e)}")
        finally:
            self._when_released=None
            logger.info(f"when_released_Thread terminated")
    
    def when_pressed_function(self):
        try:
            while self._stop_when_pressed==False:
                if self._when_pressed!=None:
                    old_value = None
                    if self._mcp.buttonList[self._pinNr]==None:
                            return
                    for val in self.gen_when('when_pressed'):
                        if self._mcp.buttonList[self._pinNr]==None:
                            return
                        if self._stop_when_pressed==True:
                            return
                        if old_value==None: 
                            old_value=val
                            continue
                        if val!= old_value:
                            old_value=val
                            if val==True:
                                if self._when_pressed!=None:
                                    func=self._when_pressed
                                    if func !=None:
                                        wh=0
                                        sig = signature(func)
                                        for name, param in sig.parameters.items():
                                            if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                                wh=+1
                                                break 
                                        if wh == 0:
                                            func()
                                        else:
                                            func(self)
                                else:
                                    return
                sleep(0.001)
            else:
                return
        except Exception as e:
                logger.error(f"{str(e)}")
        finally:
            self._when_pressed=None
            logger.info(f"when_pressed_Thread terminated")                

    def when_held_function(self):
        try:
            while self._stop_when_held==False:
                if self._when_held!=None:
                    old_value = None
                    if self._mcp.buttonList[self._pinNr]==None:
                            return
                    for val in self.gen_when('when_held'):
                        if self._mcp.buttonList[self._pinNr]==None:
                            return
                        if self._stop_when_held==True:
                            return
                        if old_value==None: 
                            old_value=val
                            continue
                        if val!= old_value:
                            old_value=val
                            if val==True:
                                if self._when_held!=None:
                                    func=self._when_held
                                    if func !=None:
                                        wh=0
                                        sig = signature(func)
                                        for name, param in sig.parameters.items():
                                            if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                                wh=+1
                                                break 
                                        while self.hold_repeat:
                                            if self._stop_when_held==True:
                                                return
                                            if self._when_held==None:
                                                return
                                            if wh==0:
                                                func()
                                            else:
                                                func(self)
                                            sleep(self._hold_time)
                                        else:
                                            if self._stop_when_held==False and self._when_held!=None:    
                                                if wh==0:
                                                    func()
                                                else:
                                                    func(self)
                                                while self.value!=0:
                                                    if self._stop_when_held==True:
                                                        return
                                                    sleep(self.gen_wait_delay)

                sleep(self.gen_when_delay*2)
            else:
                return
        except Exception as e:
                logger.error(f"{str(e)}")
        finally:
            self._when_held=None
            logger.info(f"when_held_Thread terminated")


if __name__ =='__main__':
    from signal import pause
    from time import sleep

    import logging
    logging.basicConfig(level=logging.INFO,style="{",format="{asctime}{name}{lineno}:{levelname:8}]{message}")
    logger = logging.getLogger(name="remoteio")
    logger.setLevel(logging.INFO)

    from multiprocessing import active_children
    import sys

    try:
        from remoteio.remoteio_client import RemoteServer
        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)



        def xwr(x):
            print('wr')
        def xwp(x):
            print('wp')
        def xwh(x):
            print('wh')


        #x=Remote_PWMLED(rs,21)
        rm=Remote_MCP23S17(rs)
        l=RMCPLED(rm,0)
        l1=RMCPLED(rm,1)
        #while True:
        #    rm.olat=0x3
        #    sleep(0.5)
        #    rm.olat=0
        #    sleep(0.5)
        
        l1.source=l
        l.on(on_time=5)
        sleep(6)
        #l.off()
        #sleep(6)
        #l.blink()
        b=RMCPButton(rm,2,bounce_time=0.2)
                   
        print(hex(rm.iodir))
        print(hex(rm.ipol))
        print(hex(rm.gppu))
        print(hex(rm.gpio))
        print(hex(rm.iocon))

        l.blink()
        sleep(5)
        #pause()
        l1.source=None
        l1.off()
        sleep(5)
        l1.on()
        sleep(5)
        #b.hold_time=2
        #b.hold_repeat=True
        #b.when_pressed=xwp
        #b.when_released=xwr
        #b.when_held=xwh
        #sleep(10)
        #b.when_pressed=None
        #b.when_released=xwr
        #b.when_held=xwh
        #b.hold_repeat=False
        b.wait_for_press()
        print('B')
        sleep(5)
        b.wait_for_release()
        print('A')
        
        #sleep(10)
        #b.hold_repeat=False
        #while True:
        #    rm.olat=0x3FF
        #    sleep(0.001)
        #    rm.olat=0
        #    sleep(0.001)
        
        rm.close()
        sleep(5)
        rm.open()
        b=RMCPButton(rm,2)
        b.hold_time=0.2
        b.when_pressed=xwp
        b.when_released=xwr
        b.when_held=xwh
        l=RMCPLED(rm,0)
        l1=RMCPLED(rm,1)
        l1.source=l
        l.blink()
        pause()
    
    except KeyboardInterrupt as e:  
        logger.error(e)      
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")
    finally:
         # get all active child processes
            active = active_children()
            logger.info(f'Active Children: {len(active)}')
            # terminate all active children
            for child in active:
                child.terminate()
            # block until all children have closed
            for child in active:
                child.join()
            # report active children
            active = active_children()
            logger.info(f'Active Children: {len(active)}')
            sys.exit()