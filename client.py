from socket import socket, AF_INET, SOCK_STREAM
from utils import utils, responses, timer, data_handlers
import time

def execute(client_sd, num, interval, duration, format):
    try:
        global data
        data = b"x" * 1000
        start_time = time.time()
        
        if num is not None:
            bytes = data_handlers.handleNumFlag(num)
            data = b"x" * bytes

        if interval is not None:
            rt = timer.RepeatedTimer(interval, data_handlers.printItervalData, client_sd, format)
            try:
                data_handlers.sendData(data, interval, start_time, client_sd)
                time.sleep(duration)
            finally:
                rt.stop()
                data_handlers.sendIntervalACK(client_sd)
        else:
            data_handlers.sendData(data, duration, start_time, client_sd)
            data_handlers.sendACK(client_sd, format)
               
    except ConnectionAbortedError:
        responses.connectionAbortedError()
    except ConnectionError as err:
        responses.connectionError(err)
    except Exception as err:
        responses.err(err)

def handleParalellConnections(paralell, ip, port, num, interval, duration, format):

    client_sd1 = socket(AF_INET, SOCK_STREAM)
    handleConnection(client_sd1, ip, port, num, interval, duration, format)

    if 2 <= paralell:
        client_sd2 = socket(AF_INET, SOCK_STREAM)
        handleConnection(client_sd2, ip, port, num, interval, duration, format)
    if 3 <= paralell:
        client_sd3 = socket(AF_INET, SOCK_STREAM)
        handleConnection(client_sd3, ip, port, num, interval, duration, format)
    if 4 <= paralell:
        client_sd4 = socket(AF_INET, SOCK_STREAM)
        handleConnection(client_sd4, ip, port, num, interval, duration, format)
    if 5 == paralell:    
        client_sd5 = socket(AF_INET, SOCK_STREAM)
        handleConnection(client_sd5, ip, port, num, interval, duration, format)

def handleConnection(client_sd, ip, port, num, interval, duration, format):
    try:
        client_sd.connect((ip, int(port)))
        print("-------------------------------------------------------------")
        print(f"A simpleperf client connected to server {ip}, port {port}")
        print("-------------------------------------------------------------")
    except ConnectionRefusedError as err:
        responses.connectionRefused(err)
    except Exception as err:
        responses.err(err)
    
    execute(client_sd, num, interval, duration, format)

def Main():
    ip, port, duration, format, interval, paralell, num = utils.checkClientOpts()
    
    if paralell == 1:
        client_sd = socket(AF_INET, SOCK_STREAM)
        handleConnection(client_sd, ip, port, num, interval, duration, format)
    else:
        handleParalellConnections(paralell, ip, port, num, interval, duration, format)

if __name__ == "__main__":
    Main()