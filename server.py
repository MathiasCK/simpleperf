from utils import utils, responses
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading
import time
from utils import data_handlers

# Create server socket
server = socket(AF_INET, SOCK_STREAM)
# Accept reuse of port after closing
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Handle incomming client connections
# @client -> client conection
# @addr -> client ip address & port
# @format -> format to print data
def handleClient(client, addr, format):
    try:
        # Keep track of start time
        start_time = time.time()
        # Data recieved (default 0)
        total_received = 0

        # Global counter for interval connections
        global i
        i = 0.0

        while True:
            # Recieve data from client
            data = client.recv(1000)

            # If no data or ACK is sent from client
            if not data or data == b"BYE":
                # See data_handlers.handleClientData()
                data_handlers.handleClientData(start_time, total_received, addr, format, client)
                break
            # Break out when all intervals have completed
            if data == b"Interval finished":
                break
            # Add lenght of data to total recieved data
            total_received += len(data)
            # If client connects via interval
            if data == b"Interval":
                # Current time
                current_time = time.time()
                # Difference start
                diff = float("{:.1f}".format(current_time - start_time))
                # See datahandlers.handleClientIntervalData()
                data_handlers.handleClientIntervalData(start_time, total_received, addr, format, client, i, diff)
                # Increase counter
                i += (diff - i)
        
        # Close client connection
        client.close()
    # ConnectionAbortedError handling
    except ConnectionAbortedError:
        responses.connectionAbortedError()
    # ConnectionError handling
    except ConnectionError as err:
        responses.connectionError(err)
    # Exception handling
    except Exception as err:
        responses.err(err)

def Main():
    # Retrieve optional arguments from server
    # For arguments see -> utils.checkServerOpts()
    bind, port, format = utils.checkServerOpts()
    try:
        # Start server ip address @bind on port @port
        server.bind((bind, int(port)))
        # Print success message
        print("---------------------------------------------")
        print(f"A simpleperf server is listening on port {str(port)}")
        print("---------------------------------------------")
        server.listen(1)
    # ConnectionRefusedError handling
    except ConnectionRefusedError as err:
        responses.connectionRefused(err)
    # Internal server error handling
    except Exception as err:
        responses.err(err)
    
    try:
        while True:
            # Wait for incomming client connections
            client, addr = server.accept()

            # Custom message when client connects
            print(f"A simpleperf client <{addr[0]}:{addr[1]}> is connected with <{bind}:{port}>")

            # Start connection thread
            # See -> handleClient
            threading.Thread(target=handleClient, args=(client, addr, format)).start()
    # KeyboardInterrupt handling
    except KeyboardInterrupt:
        responses.keyBoardInterrupt()
    # Internal server error handling
    except Exception as err:
        responses.err(err)
    finally:
        # Close server after connection closes
        if server:
            server.close()

# Code execution starts here
if __name__ == "__main__":
    Main()