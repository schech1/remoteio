#!/usr/bin/env python3
from inspect import getmembers,stack
from types import FunctionType

def getFunctionName()->str:
    """
    Returns:
        the name of the method that invokes getFunctionName()
    """
    import traceback
    return traceback.extract_stack(None, 2)[0][2]

def getProperties(obj):
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

def getFunctions(obj):
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

def isFunction(obj,func:str):
    if func in getFunctions(obj):
        return True
    else:
        return False

def isProperty(obj,prop:str):
    if prop in getProperties(obj):
        return True
    else:
        return False

def isReadOnly(o:object,attr):
  if attr in getProperties(o):
    v=getattr(o,attr)
  try:
    setattr(o,attr,v)
    return False
  except Exception as e:
    return True

def getWriteableProperties(o:object):
    return [attr for attr in getProperties(o) if not isReadOnly(o,attr)]

def getReadOnlyProperties(o:object):
    return [attr for attr in getProperties(o) if isReadOnly(o,attr)]

## cyclic way 0,..., max,..,-max,..., ckockwise
## cyclic way 0,...,-max,..,max,..., counter_clockwise
def shortestWay(a,b,max):
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
