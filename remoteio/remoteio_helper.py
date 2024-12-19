#!/usr/bin/env python3




from time import sleep
import logging
logger = logging.getLogger(__name__)
##########################################
##########################################
def getFunctionName()->str:
    """
    Returns:
        the name of the method that invokes getFunctionName()
    """
    import traceback
    return traceback.extract_stack(None, 2)[0][2]
###########################################
def getProperties(obj):
    from inspect import getmembers
    from types import FunctionType
    disallowed_names = [
      name for name, value in getmembers(type(obj)) 
        if isinstance(value, FunctionType)]
    for name in dir(obj):
        try:
          getattr(obj,name)
        except:
          disallowed_names.append(name)
    return [name
      for name in dir(obj) 
        if name[0] != '_' and name not in disallowed_names and hasattr(obj, name)]
############################################
def getFunctions(obj):
    from inspect import getmembers
    from types import FunctionType
    allowed_names = [
      name for name, value in getmembers(type(obj)) 
        if isinstance(value, FunctionType)]
    for name in dir(obj):
        try:
          getattr(obj,name)
        except:
          if name in allowed_names:
            allowed_names.pop(name)
    return [name
      for name in dir(obj) 
        if name[0] != '_' and name in allowed_names and hasattr(obj, name)]
############################################
def isFunction(obj,func:str):
    if func in getFunctions(obj):
        return True
    else:
        return False
#############################################
def isProperty(obj,prop:str):
    if prop in getProperties(obj):
        return True
    else:
        return False
#############################################
def isReadOnly(o:object,attr):
  if attr in getProperties(o):
    v=getattr(o,attr)
  try:
    setattr(o,attr,v)
    return False
  except Exception as e:
    return True
##########################################
def getWriteableProperties(o:object):
    return [attr for attr in getProperties(o) if not isReadOnly(o,attr)]
############################################
def getReadOnlyProperties(o:object):
    return [attr for attr in getProperties(o) if isReadOnly(o,attr)]
############################################

def shortestWay(a:int,b:int,max:int):
    '''
    finds the shortest way from a to b in the cyclic range (-max, ..., max)

    compares clockwise and counterclockwise way

    of interest for counting the position of a rotary encoder

    Parameters:
      a:int 
      b:int 
      max:int 
    '''
    if a<b:
      x= abs(a-b)<= abs(b-max) + 1 + abs((-max)-a)
      if x==True:
         return b-a
      else:
         return  -(abs((-max)-a) + 1 + abs(b-max))
      
    if a>b: 
        x=abs(b-a) <= abs(max-a) + 1 + abs((-max)-b) 
        if x==True:
          return b-a
        else:
          return +(abs(max-a) + 1 + abs((-max)-b))
    
    if a==b: return 0

########################################
def map_bg(pin_number:int,numbering:str)->int:
    '''
    maps a pinNumber to the corresponding GPIO-pinNumber

    numbering may be 'b' or 'g'

    '''
    from remoteio.remoteio_constants import PIN_MAP_bg
    
    if numbering=='b':
        if pin_number in PIN_MAP_bg.keys():
            return PIN_MAP_bg[pin_number]
        else:
            raise ValueError('((b), ' + str(pin_number) + ') false')    
    if numbering == 'g':
        if pin_number in PIN_MAP_bg.values():
            return pin_number
        else:
            raise ValueError('((g), ' + str(pin_number) + ') false')
######################################        
def getBusyGpioPins():
  '''
  returns busy GPIO Pins
  usefull to see at the beginning of a project, which GPIO-pins may be used
  '''
  from gpiozero import LED
  liste=[]
  for pin in range(0,28):
    try:
        l=LED(pin)
        l.close()
    except Exception as e:
        liste.append(f"Pin{pin}: {e.__class__} {str(e)}")
    
  return liste

###################################
def getName(var:object)->str:
    from inspect import currentframe
    '''
    example: getName(led) returns 'led', if led is an existing object
    '''
    callers_local_vars = currentframe().f_back.f_locals.items()
    list_entry= [var_name for var_name, var_val in callers_local_vars if var_val is var][0]
    return list_entry
#######################################
def i2cDetect(busId:int=1)->list[str]:
    """
    gives a list of all addresses of I2C-bus which are used
    busID = 1 is default.
    """
    import os

    liste=[]
    string = os.popen('sudo i2cdetect -y ' + str(busId)).read()
    lst = string.split('\n')

    for i in range(1,9):
        for j in range(0,16):
            x = lst[i][j*3+4:j*3+6]
            if  x != '--' and x != '  ':
                y= int(x,16)
                liste.append(y)
                 
    return liste
  ######################################  
def ReverseBits(byte):
  byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
  byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
  byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
  return byte

def bytesToHex(Bytes:bytearray|list)->str:
  return ''.join(["0x%02X " % x for x in Bytes]).strip()

def getBit(nr:int,b:int):
  return (b>>nr) & 0x01

def setBit(nr:int,b:int):
  wert=1
  maske = 2**nr
  return (b | maske)


def resetBit(nr:int,b:int):
  wert=0
  maske = ~(2**nr)
  return  b & maske 
#####################################################
