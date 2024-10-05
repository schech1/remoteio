import socket
from gpiozero import PWMLED
import threading
import time
import logging
from queue import Queue
"""
    Queue_exceptions sind
    Queue.Empty, Queue.Full
    try:
        raise Queue.Full("Text")
    except Queue.Full:
        print("Full")
        pass
"""

from remoteio import PORT      

logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")

PIN_NUMBERINGS=['b', 'g'] # b: Board numbering, g = GPIO numbering


# Dictionary to store LED instances for each pin number
led_dict = {}
led_que_dict={}

# target task function
def led_off(led):
    led.off()
   
 
def handle_timer(led):
    try:
        qu=led_que_dict[led]

        while True:
            while qu.empty():
                pass

            # letzten Befehl in der Schlange ausführen
            while not qu.empty():
                numbering, pin, command, time_ms=qu.get()                
           

            time_ms = float(time_ms) / 1000.0
            time_thr=time_ms
            try:
                func=getattr(led,command)
                func()
            except:
                logger.info('command not known: ' + command)
                return

            if time_ms > 0.:
                t=threading.Timer(time_thr,led_off,[led])
                t.start()
                while t.is_alive():
                    if qu.empty():
                        pass
                    else:
                        t.cancel()
                        break
    # an exception occurs only by crash of the main program or led used by anoher one
    except Exception:
        pass        
        
      

# Create gpiozero LED objects based on numbering system
def create_led(numbering, pin_number):
    if numbering.lower() == 'b':
        return PWMLED("BOARD" + str(pin_number))
    elif numbering.lower() == 'g':
        return PWMLED(pin_number, pin_factory=None)
    else:
        logger.error(f"Invalid numbering system. Use {PIN_NUMBERINGS}")

# preparation of a map to a list of lists of 4 elements                                         
def map_to_list(m:map)->list:                                                                   
    from math import fmod
    try:
        m_list=list(m)
        if fmod(len(m_list),4) != 0:
            for i in range(0,len(m_list)):
                logger.info(m_list[i])
            raise ValueError("length of map not a multiple of 4")
        
        n_list=[]
        for i in range(0,len(m_list),4):
            n_list.append([m_list[i],m_list[i+1],m_list[i+2],m_list[i+3]])
        ret=n_list
    except Exception as e:
        logger.error(f"Error: {e}")
        ret=None
    finally:
        return ret
########################################################################################################################
#     
# Handle client requests
def handle_client(conn):
    try:
        #  Close all pin instances in led_dict and led_que_dict
        led_dict.clear()
        led_que_dict.clear()
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            try:
                logger.debug(data)
                liste = map_to_list(map(str.strip, data.split()))
                if liste == None:
                    raise ValueError("transformation of map to list did not succeed")
                for [numbering, pin, command, time_ms] in liste:
                    # Create or retrieve LED instance for the specified pin number
                    if pin not in led_dict:
                        led_dict[pin] = create_led(numbering, pin)
                        led = led_dict[pin]
                        led_que_dict[led]=Queue(maxsize=100)
                        threading.Thread(target=handle_timer, args=(led,)).start()

                    led = led_dict[pin]
                    

                    logger.info(f"Pin: {pin}({numbering}), State: {command}, Time: {time_ms}")

                    # Execute gpio action 
                    led_que_dict[led].put([numbering,pin,command,time_ms])
                    
            except ValueError as e:
                logger.error(e)
                break                       
            except RuntimeError as e:
                logger.error(e)
                break                       
    except Exception as e:
        logger.error(e)
    finally:
        # Cleanup actions on disconnect
        logger.info(f"Disconnected from client")
        if conn:
            conn.close()
        # System closes leds. Do not make yourself. Furnishes exceptions with traces.
        for pin, led in led_dict.items():
            if not led.closed:
                led.close()
                logger.info(f"Released pin {pin}")
                
     

        


def run_server(port=PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))          
    server_socket.listen(5)

    logger.info(f"remoteio listening on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        logger.info(f"Connection from {addr}")
        client_handler=threading.Thread(target=handle_client, args=(conn,))
        client_handler.start()
    
    

if __name__ == "__main__":
    run_server()


