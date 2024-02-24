import socket
from gpiozero import LED, PWMLED
import threading
import time
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="remoteio")

PIN_NUMBERINGS=['b', 'g'] # b: Board numbering, g = GPIO numbering
PORT = 8509

# Dictionary to store LED instances for each pin number
led_dict = {}

# Define a dictionary to map status to LED actions
process_command = {
    "on": lambda led, time_ms: led.on() if int(time_ms) <= 0 else handle_timer(led, time_ms),
    "off": lambda led, time_ms: led.off(),
    "blink": lambda led, time_ms: led.blink(),
    "pulse": lambda led, time_ms: led.pulse(),
}

def handle_timer(led, time_ms):
    time_ms = float(time_ms) / 1000.0
    led.on()
    time.sleep(time_ms)
    led.off()


# Create gpiozero LED objects based on numbering system
def create_led(numbering, pin_number, command):
    if numbering.lower() == 'b':
        if command == "pulse": 
            return PWMLED("BOARD" + str(pin_number)) 
        else:
            return LED("BOARD" + str(pin_number))  
    elif numbering.lower() == 'g':
        if command == "pulse":
            return PWMLED(pin_number, pin_factory=None)
        else:
            return LED(pin_number, pin_factory=None)
    else:
        logger.error(f"Invalid numbering system. Use {PIN_NUMBERINGS}")

# Handle client requests
def handle_client(conn):
    while True:
        data = conn.recv(1024).decode().strip()

        if not data:
            break
        try:
            logger.debug(data)
            numbering, pin, command, time_ms = map(str.strip, data.split())

            # Create or retrieve LED instance for the specified pin number
            if pin not in led_dict:
                led_dict[pin] = create_led(numbering, pin, command)
            led = led_dict[pin]

            logger.info(f"Pin: {pin}({numbering}), State: {command}, Time: {time_ms}")

            # Check if status is valid
            if command not in process_command:
                logger.error("Invalid command")
                continue

            # Execute gpio action 
            process_command[command](led, time_ms)
 
        except ValueError as e:
            logger.error(e)
        except Exception as e:
            logger.error(f"Error: {e}")
    conn.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(5)
    logger.info(f"remoteio listening on port {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        logger.info(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(conn,))
        client_handler.start()

if __name__ == "__main__":
    run_server()


