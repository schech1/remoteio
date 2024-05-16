import socket
from gpiozero import PWMLED
import threading
import time
import logging
import remoteio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="remoteio")

# Define the initial selected host and port
selected_host = "192.168.0.90"  # Default host
selected_port = 8509  # Default port

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
def create_led(numbering, pin_number):
    if numbering.lower() == 'b':
        return PWMLED("BOARD" + str(pin_number))
    elif numbering.lower() == 'g':
        return PWMLED(pin_number, pin_factory=None)
    else:
        logger.error("Invalid numbering system.")

# Handle client requests
def handle_client(conn):
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            logger.info(data)
            if not data:
                break
            try:
                logger.debug(data)
                numbering, pin, command, time_ms = map(str.strip, data.split())

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
                process_command[command](led, time_ms)

            except ValueError as e:
                logger.error(e)
            except Exception as e:
                logger.error(f"Error: {e}")
    finally:
        # Cleanup actions on disconnect
        logger.info(f"Disconnected from client")
        
        # Close all pin instances in led_dict
        for pin, led in led_dict.items():
            led.close()
            logger.info(f"Released pin {pin}")
        led_dict.clear()
        conn.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', selected_port))
    server_socket.listen(5)
    logger.info(f"remoteio listening on port {selected_port}...")

    while True:
        conn, addr = server_socket.accept()
        logger.info(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(conn,))
        client_handler.start()

if __name__ == "__main__":
    run_server()
