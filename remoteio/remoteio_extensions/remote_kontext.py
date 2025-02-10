#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteSupervisor

from time import sleep
import logging
logger = logging.getLogger(__name__)


class Remote_Kontext:
    '''
    class Remote_Kontext(
        *components:RemoteDigitalDevice|Remote_Kontext
    )
    Has no own access to server side, 
    is a tree or list of RemoteDigitalDevice objects and Remote_Kontext objects
    with the attribute value.
    using derivates of remoteio_extensions like RMCPLED of Remote_MCP23S17, this derivate
    must have additonally the attributes getClientIdent and setClientIdent to be used by Remote_Kontext
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
            if  hasattr(comp,'value')   and \
                not comp in self._childs:
                if isinstance(comp,Remote_Kontext):
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
        
    ## self._value represents the state of the Kontext
    @property
    def value(self):
        self._value={}
        for child in self._childs:
            self._value[child.getClientIdent()] = child.value
        return self._value
    
if __name__=='__main__':
    
    try:  
        from signal import pause
        from time import sleep

        import logging
        logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
        logger = logging.getLogger(name="remoteio")
        logger.setLevel(logging.INFO)

        from remoteio.remoteio_client import RemoteServer
        from remoteio.remoteio_devices.remote_led import Remote_LED
        from remoteio.remoteio_devices.remote_motor import Remote_Motor
        from remoteio.remoteio_extensions import Remote_W1ThermDevice
        
        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)

        rl=Remote_LED(rs,16)
        mo=Remote_Motor(rs,20,21)
        w1=Remote_W1ThermDevice(rs)
        st=Remote_Kontext(rl,mo,w1)
        rl.on()
        mo.backward(speed=0.5)
        ## read values of remote devices only one time, then work with result x
        rl.setClientIdent('rl')
        mo.setClientIdent('mo')
        w1.setClientIdent('w1')
        x=st.value
        print(st._value['rl'])
        print(st._value['mo'])
        print(st._value['w1'])
        rl.off()
        mo.forward(speed=1)
        x=st.value
        print(st._value['rl'])
        print(st._value['mo'])
        print(st._value['w1'])
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")