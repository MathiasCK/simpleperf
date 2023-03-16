from socket import socket, AF_INET, SOCK_STREAM
from utils import utils, responses, timer, data_handlers
import time

def Main():
    ip, port, duration, format, interval, paralell = utils.checkClientOpts()
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

        if interval is not None:
            print(True)
            rt = timer.RepeatedTimer(interval, data_handlers.printItervalData, client_sd, format)
            try:
                data_handlers.sendData(interval, start_time, client_sd)
                time.sleep(duration)
            finally:
                rt.stop()
                data_handlers.sendACK(client_sd, format)
        else:
            data_handlers.sendData(duration, start_time, client_sd)
            data_handlers.sendACK(client_sd, format)
               
    except ConnectionAbortedError:
        responses.connectionAbortedError()
    except ConnectionError as err:
        responses.connectionError(err)
    except Exception as err:
        responses.err(err)

if __name__ == "__main__":
    Main()