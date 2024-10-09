import sys
import socket
from gpiozero import PWMLED
from multiprocessing import Process, Queue, Event, Lock
import time
import logging
from remoteio import PORT      
#from queue import Queue

logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")

# target task function
def led_off(led):
    led.off()
   


    

def handle_led(pin,qu,ev,lo,h_list,l_dict):

    led=None

    with lo:
       h_list.append(pin)

    try:
        while True: 
            ende=False  
            while qu.empty():
                if ev.is_set():
                    ende=True
                    break
            if ende==True:
                break

            # perform all tasks in queue
            numbering, pin, command, time_ms, arg1, arg2 = qu.get() 

            # the precedent led-process to the same led is perhaps alive. Waiting until it is destroyed  
            generated=False          
            while led==None:
                try:
                    led = PWMLED("BOARD"+pin,pin_factory=None)
                    generated=True
                    break
                except Exception as e:
                    pass
            if generated==True:
                generated=False
                logger.info('led for ' + pin + '(b) generated')

            time_ms = float(time_ms) / 1000.0
            #time_thr=time_ms
            try:   
                match command:
                    case 'value':
                        led.value=float(arg1)                        
                    case 'blink':
                        led.blink(float(arg1),float(arg2))
                    case _:
                        func=getattr(led,command)
                        func()
            except:
                logger.info('command error: ' + command)
                continue
    
            if time_ms > 0.:
                time.sleep(time_ms)
                if qu.empty:
                    led.off()

                #t=threading.Timer(time_thr,led_off,[led])
                #t.start()
                #while t.is_alive():
                #    if qu.empty():
                #        pass                        
                #    else:
                #        t.cancel()
                #        break
            logger.info(f"Pin: {pin}({numbering}), State: {command}, Time: {time_ms}, Arg1: {arg1}. Arg2: {arg2}")    
   
    
    except Exception as e:
        if led is None:
            logger.error(f"{pin} is busy")
        else:
            logger.error(e)
            logger.error(f"Pin: {pin}({numbering}), State: {command}, Time: {time_ms}, Arg1: {arg1}. Arg2: {arg2}") 
    finally:
        if not (led is None):
            led.off()
            led.close() 
            logger.info(f"Released pin {pin}")
        with lo:
            h_list.remove(pin) 
        logger.info(f"Handle_led of {pin} (b) terminated")        
    
########################################################################################################################
#     
# Handle client requests
def handle_client(conn,addr,client_port,process_lock,h_led_list):

    led_dict={}
    data1=''
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            data1+=data
            while data1.count(' ') >= 6:                
                numbering,sep, datan = data1.partition(' ')
                pin,sep, datap= datan.partition(' ')
                command,sep, datac= datap.partition(' ')
                time_ms,sep, datat = datac.partition(' ')
                arg1, sep,dataa = datat.partition(' ')
                arg2, sep,data1 = dataa.partition(' ')

                on_queue=False
                # Create or retrieve LED instance for the specified pin number
                if pin not in led_dict:
                    pin_ev=Event()
                    pin_qu=Queue(maxsize=1024)                        
                    pin_proc=Process(target=handle_led, args=(pin,pin_qu,pin_ev,process_lock,h_led_list,led_dict)) 
                    pin_proc_started=False
                    led_dict[pin]=[pin_qu,pin_ev,pin_proc,pin_proc_started]
                    led_dict[pin][0].put([numbering,pin,command,time_ms,arg1,arg2])
                    on_queue=True

                    
                if (pin not in h_led_list):
                    if (not led_dict[pin][3]):
                        led_dict[pin][2].start()
                        led_dict[pin][3]=True

                # Execute gpio action 
                if not on_queue:
                    if led_dict[pin][0].full():
                        raise RuntimeError(pin + ' ' + 'queue full')
                    led_dict[pin][0].put([numbering,pin,command,time_ms,arg1,arg2])  

    except ValueError as e:
        logger.error(e)                     
    except RuntimeError as e:
        logger.error(e)                     
    except Exception as e:
        logger.error(e)
    finally:
        # Cleanup actions on disconnect
        if conn:
            conn.close()
        for pi,[qu,ev,proc,proc_state] in led_dict.items():
            ev.set()
        logger.info(f"Disconnected from client (" + str(addr)+ '), client_port = ' + str(client_port))

def run_server(port=PORT):
    lock=Lock()
    handle_led_list=[]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', port))          
        server_socket.listen(5)

        logger.info(f"remoteio listening on port {port}...")

        while True:
            conn, addr = server_socket.accept()
            logger.info(f"Connection from {addr}")
            client_handler=Process(target=handle_client, args=(conn,addr,port,lock,handle_led_list))
            client_handler.start()
    

if __name__ == "__main__":
    try:
        server_8509=Process(target=run_server, args=(8509,))
        server_8509.start()
        server_8510=Process(target=run_server, args=(8510,))
        server_8510.start()
            


    except Exception as e:
        logger.error(e)
        sys.exit()

    
