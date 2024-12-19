#!/usr/bin/env python3
 
from multiprocessing import active_children                       
import sys

from remoteio.remoteio_server import run_server

from time import sleep
import logging
# instantiate logger
logging.basicConfig(level=logging.INFO,style="{",format="{asctime} {name} {lineno}: [{levelname:8}]{message}")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info('start run_server')
    
try:
    run_server()

except Exception as e:
    logger.error(f"{e.__class__}: {str(e)}")
finally:
    #get all active child processes
    active = active_children()
    logger.info(f'Active Children: {len(active)}')
    #terminate all active children
    for child in active:
        child.terminate()
    # block until all children have closed
    for child in active:
        child.join()
    # report active children
    active = active_children()
    logger.info(f'Active Children: {len(active)}')
    sys.exit(0)
            

