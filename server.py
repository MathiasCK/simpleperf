from utils import utils, responses
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading
import time
from utils import data_handlers

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

def handleClient(client, addr, format):
    try:
        start_time = time.time()
        total_received = 0
        global i
        i = 0.0

        while True:
            data = client.recv(1000)
            if not data or data == b"BYE":
                data_handlers.handleClientData(start_time, total_received, addr, format, client)
                break
            if data == b"Interval finished":
                break
            total_received += len(data)
            if data == b"Interval":
                current_time = time.time()
                diff = float("{:.1f}".format(current_time - start_time))
                data_handlers.handleClientIntervalData(start_time, total_received, addr, format, client, i, diff)
                i += (diff - i)
        
        client.close()
    except ConnectionAbortedError:
        responses.connectionAbortedError()
    except ConnectionError as err:
        responses.connectionError(err)
    except Exception as err:
        responses.err(err)

def Main():
    bind, port, format = utils.checkServerOpts()
    try:
        server.bind((bind, int(port)))
        print("---------------------------------------------")
        print(f"A simpleperf server is listening on port {str(port)}")
        print("---------------------------------------------")
        server.listen(1)
    except ConnectionRefusedError as err:
        responses.connectionRefused(err)
    except Exception as err:
        responses.err(err)
    
    try:
        while True:
            client, addr = server.accept()
            print(f"A simpleperf client <{addr[0]}:{addr[1]}> is connected with <{bind}:{port}>")

            threading.Thread(target=handleClient, args=(client, addr, format)).start()
    except KeyboardInterrupt:
        responses.keyBoardInterrupt()
    except Exception as err:
        responses.err(err)
    finally:
        if server:
            server.close()

if __name__ == "__main__":
    Main()