from socket import socket, AF_INET, SOCK_STREAM
from utils import utils, responses
from time import time
import json

def Main():
    ip, port, duration, format = utils.checkClientOpts()
    client_sd = socket(AF_INET, SOCK_STREAM)

    try:
        client_sd.connect((ip, int(port)))
        print("-------------------------------------------------------------")
        print(f"A simpleperf client connected to server {ip}, port {port}")
        print("-------------------------------------------------------------")
    except ConnectionRefusedError as err:
        responses.connectionRefused(err)
    except Exception as err:
        responses.err(err)

    try:
        start_time = time()
        total_sent = 0

        while time() - start_time < duration:
            data = b"x" * 1000
            client_sd.sendall(data)
            total_sent += len(data)

        client_sd.sendall(b"BYE")
        ack = client_sd.recv(1024).decode('utf-8')

        if ack == b"ACK/BYE":
            results = json.loads(client_sd.recv(1024).decode('utf-8'))
            utils.printResults(results, format)
        else:
            responses.connectionError("Failed to recieve ACK from server")

        client_sd.close()
    except ConnectionAbortedError:
        responses.connectionAbortedError()
    except ConnectionError as err:
        responses.connectionError(err)
    except Exception as err:
        responses.err(err)

if __name__ == "__main__":
    Main()