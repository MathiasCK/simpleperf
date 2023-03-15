from utils import utils
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, Lock

server = socket(AF_INET, SOCK_STREAM)

clients = set()
clients_lock = Lock()

def handleRequest(client, addr, bind, port):
    print(f"A simpleperf client <{addr[0]}:{addr[1]}> is connected with <{bind}:{port}>")

def Main():
    bind, port, format = utils.checkServerOpts()
    try:
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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

            with clients_lock:
                clients.add(client)
    
            thread = Thread(
                target=handleRequest, args=(client, addr, bind, port))
            thread.start()
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        # Close server connection
        if server:
            server.close()

if __name__ == "__main__":
    Main()