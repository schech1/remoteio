import socket
from gpiozero import PWMLED
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
    """    Handle a timer for turning on and off an LED.

    This function takes an LED object and a time in milliseconds, converts the time to seconds, turns on the LED, waits for the specified time, and then turns off the LED.

    Args:
        led: An object representing the LED.
        time_ms (int): The time in milliseconds for which the LED should remain on.
    """

    time_ms = float(time_ms) / 1000.0
    led.on()
    time.sleep(time_ms)
    led.off()


# Create gpiozero LED objects based on numbering system
def create_led(numbering, pin_number):
    """    Create gpiozero LED objects based on the numbering system.

    Args:
        numbering (str): The numbering system to be used. It can be 'b' for BOARD or 'g' for BCM.
        pin_number (int): The pin number to be used.

    Returns:
        PWMLED: The gpiozero PWMLED object based on the specified numbering system and pin number.

    Raises:
        ValueError: If the input numbering system is not 'b' or 'g'.
    """

    if numbering.lower() == 'b':
        return PWMLED("BOARD" + str(pin_number))
    elif numbering.lower() == 'g':
        return PWMLED(pin_number, pin_factory=None)
    else:
        logger.error(f"Invalid numbering system. Use {PIN_NUMBERINGS}")

# Handle client requests
def handle_client(conn):
    """    Handle client requests.

    This function handles client requests by receiving data from the connection, processing the data, and executing
    corresponding actions based on the received commands. It also performs cleanup actions upon disconnection.

    Args:
        conn (socket): The connection object for communicating with the client.


    Raises:
        ValueError: If the data cannot be parsed into the required format.
        Exception: If any other unexpected error occurs during data processing or action execution.
    """

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
    """    Run a server to handle incoming connections.

    This function creates a server socket and listens for incoming connections. When a connection is established, it spawns a new thread to handle the client.
    """

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


