from socket import socket, AF_INET, SOCK_STREAM
from utils import utils
from time import time

def Main():
    ip, port, duration = utils.checkClientOpts()
    client_sd = socket(AF_INET, SOCK_STREAM)

    try:
        client_sd.connect((ip, int(port)))
        print("-------------------------------------------------------------")
        print(f"A simpleperf client connected to server {ip}, port {port}")
        print("-------------------------------------------------------------")
    except Exception as err:
        print(f"Could not connect to server: {repr(err)}")
        exit()


    start_time = time()
    total_sent = 0

    while time() - start_time < duration:
        data = b"x" * 1000
        client_sd.sendall(data)
        total_sent += len(data)

    client_sd.sendall(b"BYE")

    response = client_sd.recv(1024).decode('utf-8')
    print(response)

    client_sd.close()

if __name__ == "__main__":
    Main()