from utils import utils
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading
import time
import math

server = socket(AF_INET, SOCK_STREAM)

def handleRequest(client, addr):
    start_time = time.time()
    total_received = 0
    
    while True:
        data = client.recv(1000)
        if not data or data == b"BYE":
            break
        total_received += len(data)

    elapsed_time = time.time() - start_time
    bandwidth = "{:.2f}".format(int(total_received / elapsed_time / (1000 * 1000)))
    recieved = "{:.2f}".format(total_received / (1000 * 1000))

    print(f"{addr[0]}:{addr[1]}")
    print(recieved, bandwidth)

    result = [ f"{addr[0]}:{addr[1]}", "0.0 - 10.0", recieved, bandwidth ]

    print("{:<20} {:<15} {:<15} {:<15}".format('ID','Interval','Recieved','Rate'))
    print("{:<20} {:<15} {:<15} {:<15}".format(f"{addr[0]}:{addr[1]}",'0.0 - 10.0',f"{recieved} MB",f"{bandwidth} Mbps"))
    


    client.sendall(str(result).encode('utf-8'))
    client.close()

def Main():
    bind, port, format = utils.checkServerOpts()
    try:
        server.bind((bind, int(port)))
        print("---------------------------------------------")
        print(f"A simpleperf server is listening on port {str(port)}")
        print("---------------------------------------------")
        server.listen(1)
    except Exception as err:
        raise Exception(f"Bind failed: {repr(err)}")
    
    try:
        while True:
            client, addr = server.accept()
            print(f"A simpleperf client <{addr[0]}:{addr[1]}> is connected with <{bind}:{port}>")

            threading.Thread(target=handleRequest, args=(client, addr)).start()
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        if server:
            server.close()

if __name__ == "__main__":
    Main()