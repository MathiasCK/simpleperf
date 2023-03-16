from utils import utils, responses
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading
import time
import json

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

def handleData(start_time, total_received, addr, format, client):
    elapsed_time = time.time() - start_time
    bandwidth = "{:.2f}".format(int(total_received / elapsed_time / (1000 * 1000)))
    recieved = "{:.2f}".format(total_received)

    results = { "ip": f"{addr[0]}:{addr[1]}", "interval": "0.0 - 10.0", "recieved": recieved, "bandwidth": f"{bandwidth} Mbps" }

    utils.printResults(results, format)

    client.sendall(b"ACK/BYE")
    client.sendall(json.dumps(results).encode('utf-8'))

def handleRequest(client, addr, format):
    try:
        start_time = time.time()
        total_received = 0
        
        while True:
            data = client.recv(1000)
            if not data or data == b"BYE":
                break
            total_received += len(data)

        handleData(start_time, total_received, addr, format, client)
        
        
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

            threading.Thread(target=handleRequest, args=(client, addr, format)).start()
    except KeyboardInterrupt:
        responses.keyBoardInterrupt()
    except Exception as err:
        responses.err(err)
    finally:
        if server:
            server.close()

if __name__ == "__main__":
    Main()