from socket import socket, AF_INET, SOCK_STREAM
from utils import utils, responses, data_handlers
import time

# Send and recieve data from server
# @client_sd -> single client socket
# @num -> --num flag (custom number of bytes to send)
# @interval -> --interval flag (custom number of seconds to print data recieved from server)
# @duration -> total time socket should send data to server (default 10)
# @format -> format data should print (default MB)
def execute(client_sd, num, interval, duration, format):
    try:
        # Default data
        global data
        data = b"x" * 1000 # 1000 bytes at a time
        
        # If --num flag is provided
        if num is not None:
            # see data_handlers.handleNumFlag()
            bytes = utils.handleNumFlag(num)
            # Overwirte default data
            data = b"x" * bytes

        # If --interval flag is provided
        if interval is not None:
            # Start timer which executes data_handlers.printIntervalData every @interval
            # @client_sd -> client socket
            # @format -> format data should be rintet 
            # Send "Interval" to server indicating interval
            client_sd.send(b"Interval")
            ack = client_sd.recv(1024).decode('utf-8')
            # Check server response ACK
            if ack == 'Interval ACK':
                # See data_handlers.sendIntervalData()
                data_handlers.sendIntervalData(data, interval, duration, client_sd, format)

        #If --interval flag is not provided
        else:
            # See data_handlers.sendData()
            data_handlers.sendData(data, duration, client_sd, format)
    
    # ConnectionAbortedError handling
    except ConnectionAbortedError:
        responses.connectionAbortedError()
    # ConnectionError handling
    except ConnectionError as err:
        responses.connectionError(err)
    # Internal server error handling
    except Exception as err:
        responses.err(err)

# handle client connection(s)
# For arguments see utils.py -> checkClientOpts
def handleConnection(paralell, ip, port, num, interval, duration, format):

    # Create client socket
    client_sd1 = socket(AF_INET, SOCK_STREAM)
    # See connect()
    connect(client_sd1, ip, port, num, interval, duration, format)

    # Run multiple connections paralell if --paralell flag is greater than 1
    if 2 <= paralell:
        # Create second client socket
        client_sd2 = socket(AF_INET, SOCK_STREAM)
        connect(client_sd2, ip, port, num, interval, duration, format)
    if 3 <= paralell:
        # Create third client socket
        client_sd3 = socket(AF_INET, SOCK_STREAM)
        connect(client_sd3, ip, port, num, interval, duration, format)
    if 4 <= paralell:
        # Create fourth client socket
        client_sd4 = socket(AF_INET, SOCK_STREAM)
        connect(client_sd4, ip, port, num, interval, duration, format)
    if 5 == paralell:
        # Create fifth client socket  
        client_sd5 = socket(AF_INET, SOCK_STREAM)
        connect(client_sd5, ip, port, num, interval, duration, format)

# handle single client connection
# For arguments see utils.py -> checkClientOpts
def connect(client_sd, ip, port, num, interval, duration, format):
    try:
        # Connect client socket to server
        # @ip -> ip address of server (default -> localhost)
        # @port -> port of server (default -> 8088)
        client_sd.connect((ip, int(port)))
        # Print success message
        print("-------------------------------------------------------------")
        print(f"A simpleperf client connected to server {ip}, port {port}")
        print("-------------------------------------------------------------")
    # ConnectionRefusesError handling
    except ConnectionRefusedError as err:
        responses.connectionRefused(err)
    # Internal server error handling
    except Exception as err:
        responses.err(err)
    
    # see execute()
    execute(client_sd, num, interval, duration, format)

def Main():
    # Get client optional arguments (see utils.py -> checkClientOpts)
    ip, port, duration, format, interval, paralell, num = utils.checkClientOpts()
    
    # see handleConnection()
    handleConnection(paralell, ip, port, num, interval, duration, format)

# Code execution starts here
if __name__ == "__main__":
    Main()