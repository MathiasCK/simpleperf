from socket import socket, AF_INET, SOCK_STREAM
from utils import utils

def Main():
    ip, port, time = utils.checkClientOpts()
    client_sd = socket(AF_INET, SOCK_STREAM)

    try:
        client_sd.connect((ip, int(port)))
        print("---------------------------------------------")
        print(f"A simpleperf client connected to server {ip}, port {port}")
        print("---------------------------------------------")
    except Exception as err:
        print(f"Could not connect to server: {repr(err)}")
        exit()

if __name__ == "__main__":
    Main()