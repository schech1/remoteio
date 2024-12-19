#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteSupervisor

from time import sleep
import logging
logger = logging.getLogger(__name__)

class Remote_LEDCompositum():
    '''
    class Remote_LEDCompositum(
        *components:RemoteDigitalDevice|Remote_Compositum
    )
    Has no own access to server side, 
    is a tree or list of RemoteDigitalDevice objects and Remote_Compositum objects
    with the attributes on, off, toggle, blink, value.
    using derivates of remoteio_extensions like RMCPLED of Remote_MCP23S17, this derivate
    must have additonally the attributes getClientIdent and setClientIdent to be used by Remote_Compositum
    '''
    def __init__(self,*args):
        self._childs=[]
        self._value={}
        self._basis_elements=[]
        self.addComponent(*args)
        self.ident=RemoteSupervisor.genServerIdent()
        self.setClientIdent(self.ident)

    def getClientIdent(self):
        return RemoteSupervisor._ident_dict[self.ident]
    def setClientIdent(self,ident):
        RemoteSupervisor.setClientIdent(self.ident,ident)

    def addComponent(self,*compTuple):
        for comp in compTuple:
            if  hasattr(comp,'on')      and \
                hasattr(comp,'off')     and \
                hasattr(comp,'toggle')  and \
                hasattr(comp,'blink')   and \
                hasattr(comp,'value')   and \
                not comp in self._childs:
                if isinstance(comp,Remote_LEDCompositum):
                    for x in comp._basis_elements:
                        if x in self._basis_elements:
                           raise ValueError(f"{comp.getClientIdent()}: {x.getClientIdent()} is already related to " + 
                                             "{self.getClientIdent()}")
                    self._basis_elements     +=comp._basis_elements     
                else:
                    if not comp in self._basis_elements:
                        self._basis_elements.append(comp)
                    else:
                        raise ValueError(f"{comp.getClientIdent()} is already related to {self.getClientIdent()}")
                self._childs.append(comp)
            else:
                raise ValueError(f"{comp.getClientIdent()} is not a valid Component")
                        
    def popComponent(self,comp):
        if comp in self._childs:
            self.pop(comp)
        
    def getChild(self,index):
        if 0 <= index < len(self._childs):
            return self._childs[index]
        else:
            return None
        
    def close(self):
        for child in self._childs:
            if hasattr(child,'close'):
                child.close()


    def on(self,*args,**kwargs):
        for index in args:
            self._childs[index].on(**kwargs)
        if args==():
            for child in self._childs:
                child.on(**kwargs)

            
    def off(self,*args):
        for index in args:
            self._childs[index].off()
        if args==():
            for child in self._childs:
                child.off()

    def toggle(self,*args):
        for index in args:
            self._childs[index].toggle()
        if args==():
            for child in self._childs:
                child.toggle()


    def blink(self,*args,**kwargs):
        for index in args:
            self._childs[index].blink(**kwargs)
        if args==():
            for child in self._childs:
                child.blink(**kwargs)

    def pulse(self,*args, **kwargs):
        for index in args:
            if hasattr(self._childs[index],'pulse'):
                self._childs[index].pulse(**kwargs)
        if args==():
            for child in self._childs:
                if hasattr(child,'pulse'):
                    child.pulse(**kwargs)

    @property
    def value(self):
        self._value={}
        for child in self._childs:
            self._value[child.getClientIdent()] = child.value
        return self._value
    @value.setter
    def value(self,wert):
         for child in self._childs:
            child.value=wert[child.getClientIdent()]

if __name__=='__main__':
    
    try:  
        from signal import pause
        from time import sleep

        import logging
        logging.basicConfig(level=logging.INFO,style="{",format="{asctime}{name} {lineno}:[{levelname:8}]{message}")
        logger = logging.getLogger(name="remoteio_ledcompositum")
        logger.setLevel(logging.INFO)

        from remoteio.remoteio_client import RemoteServer
        from remoteio.remoteio_devices.remote_rgbled import Remote_RGBLED
        from remoteio.remoteio_devices.remote_pwmled import Remote_PWMLED
        from remoteio.remoteio_extensions.remote_mcp23x17 import RMCPLED
        from remoteio.remoteio_extensions.remote_mcp23x17 import Remote_MCP23S17

        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)
    
        rl1=Remote_RGBLED(rs,16,18,20,pwm=True)
        #rl2=Remote_PWMLED(rs,22)
        rmcp=Remote_MCP23S17(rs)
        rl2=RMCPLED(rmcp,0)
        rl3=Remote_PWMLED(rs,21)
        
        rc=Remote_LEDCompositum(rl1,rl2)
        rc1=Remote_LEDCompositum(rc,rl3)
        rl1.setClientIdent('rs.rl1')
        rl2.setClientIdent('rs.rl2')
        rl3.setClientIdent('rs.rl3') 
        rc.setClientIdent('__.rc')
        rc1.setClientIdent('__.rc1') 
        print(rl1.getClientIdent())
        print(rl2.getClientIdent())  
        print(rl3.getClientIdent())
        print(rc.getClientIdent())
        print(rc1.getClientIdent())
        print(list(RemoteSupervisor._ident_dict.keys()))
        print(rc1._childs)
        print(rc1._basis_elements)
        
        rl1.on(on_time=4)
        rl2.on()
        rl3.on()
        sleep(5)
        print(rl1.value)
        print(rl2.value)
        print(rl3.value)
        rc1.off()
        print(rc1.value)
        rc1.on(-1)
    
        print(rc1.value)
        sleep(5)
        rc1.off(-2,-1)
        print(rc1.value)
        sleep(5)
        
        rc1.toggle(0,1)
        print(rc1.value)
        sleep(5)
    
        rc1.value={rc.getClientIdent(): {rl1.getClientIdent(): (1,1,0), rl2.getClientIdent(): 1}, rl3.getClientIdent(): 1}
        print(rc1.value)
        sleep(5)
        rc1.pulse()
        sleep(15)
        rc1.blink()
        sleep(5)
        rc1.close()
        rmcp.close()
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")