from socket import socket, AF_INET, SOCK_STREAM
from utils import utils, responses
import time
import json

def sendDataWithIntervals(duration, interval, client_sd, format):
    while duration > interval:
            data = b"x" * 1000
            client_sd.sendall(data)
            client_sd.sendall(b"Interval finished")

            results = json.loads(client_sd.recv(1024).decode('utf-8'))
            utils.printResults(results, format)
            duration -= interval

def sendDataWithoutIntervals(duration, start_time, client_sd, format):
    while time.time() - start_time < duration:
        data = b"x" * 1000
        client_sd.sendall(data)
    
    client_sd.sendall(b"BYE")
    ack = client_sd.recv(1024).decode('utf-8')

    if ack == "ACK/BYE":
        results = json.loads(client_sd.recv(1024).decode('utf-8'))
        utils.printResults(results, format)
    else:
        responses.connectionError("Failed to recieve ACK from server")

    client_sd.close()

def Main():
    ip, port, duration, format, interval = utils.checkClientOpts()
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
        start_time = time.time()

        if interval > 0:
            return sendDataWithIntervals(duration, interval, client_sd, format)
        
        sendDataWithoutIntervals(duration, start_time, client_sd, format)
               
    except ConnectionAbortedError:
        responses.connectionAbortedError()
    except ConnectionError as err:
        responses.connectionError(err)
    except Exception as err:
        responses.err(err)

if __name__ == "__main__":
    Main()