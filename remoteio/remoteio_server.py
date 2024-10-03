import socket
from gpiozero import PWMLED
import threading
import time
import logging

from remoteio import PORT      


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="remoteio")

PIN_NUMBERINGS=['b', 'g'] # b: Board numbering, g = GPIO numbering


# Dictionary to store LED instances for each pin number
led_dict = {}
#list of leds in process
led_list=[]
# Define a dictionary to map status to LED actions
process_command = {
    "on": lambda led, time_ms:     threading.Thread(target=handle_timer, args=(led,'on',time_ms)).start(),
    "blink": lambda led, time_ms:  threading.Thread(target=handle_timer, args=(led,'blink',time_ms)).start(),
    "pulse": lambda led, time_ms:  threading.Thread(target=handle_timer, args=(led,'pulse',time_ms)).start(),
    
}

def handle_timer(led, state, time_ms):
    time_ms = float(time_ms) / 1000.0
 
    match state:
        case 'on':
            led.on()
        case 'blink':
            led.blink()
        case 'pulse':
            led.pulse()

    if time_ms > 0.:
        time.sleep(time_ms)
        led.off()
    led_list.remove(led)
    
    



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
        while True:
            #protection against to fast proceeding of the client
            while len(led_list)>0:
                pass
            # client asks for sending of next task (execute-function)
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            if data=='?':
                conn.send('!'.encode())
            else:
                raise RuntimeError('synchronisation with client fails')
            
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
                    logger.info(f"Pin: {pin}({numbering}), State: {command}, Time: {time_ms}")

                    # Check if status is valid
                    if command not in process_command:
                        logger.error("Invalid command")
                        continue

                    # Execute gpio action 
                    led_list.append(led)
                    process_command[command](led, time_ms)

            except ValueError as e:
                logger.error(e)
                break                       
            except Exception as e:
                logger.error(f"Error: {e}")
                break                      

    finally:
        # Cleanup actions on disconnect
        logger.info(f"Disconnected from client")
        
        # Close all pin instances in led_dict
        for pin, led in led_dict.items():
            led.close()
            logger.info(f"Released pin {pin}")
        led_dict.clear()
        conn.close()


def run_server(port=PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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


