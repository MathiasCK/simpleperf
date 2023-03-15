from utils import utils
from socket import socket, AF_INET, SOCK_STREAM

SERVER_SOCK = socket(AF_INET, SOCK_STREAM)

def handleRequest(sock):
    print("handleRequest()")

def Main():
    bind, port, format = utils.checkServerOpts()
    try:
        SERVER_SOCK.bind((bind, int(port)))
        print("---------------------------------------------")
        print(f"A simpleperf server is listening on port {str(port)}")
        print("---------------------------------------------")
        SERVER_SOCK.listen(1)
    except Exception as err:
        raise Exception(f"Bind failed: {repr(err)}")
    
    sock, addr = SERVER_SOCK.accept()

    handleRequest(sock)

    SERVER_SOCK.close()

if __name__ == "__main__":
    Main()