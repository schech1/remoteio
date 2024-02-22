import socket
from gpiozero import LED
import threading
import time
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="remoteio")

PIN_NUMBERINGS=['b', 'g'] # b: Board numbering, g = GPIO numbering
PORT = 8509

# Dictionary to store LED instances for each pin number
led_dict = {}

# Create gpiozero LED objects based on numbering system
def create_led(numbering, pin_number):
    if numbering.lower() == 'b':
        return LED("BOARD" + str(pin_number))
    elif numbering.lower() == 'g':
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
            numbering, pin, status, time_ms = map(str.strip, data.split())

            # Create or retrieve LED instance for the specified pin number
            if pin not in led_dict:
                led_dict[pin] = create_led(numbering, pin)
            led = led_dict[pin]

            logger.info(f"Pin: {pin}, State: {status}, Time: {time_ms}")

            if status == "on":
                led.on()

                if float(time_ms) > 0:
                    time_ms = float(time_ms) / 1000.0
                    time.sleep(time_ms)
                    led.off()
                    logger.debug(f"Pin {pin} ({numbering}) switched off")

            elif status == "off":
                led.off()
            else:
                logger.error("Invalid status, please use 'on' or 'off'")
                continue
 
        except ValueError as e:
            logger.error(e)
        except Exception as e:
            logger.error(f"Error: {e}")
    conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(5)
    logger.info(f"Server started, listening on port {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        logger.info(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(conn,))
        client_handler.start()

if __name__ == "__main__":
    main()


