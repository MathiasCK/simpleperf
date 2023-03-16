from utils import utils
import time
import json

global data
data = b"x" * 1000

def printItervalData(client_sd, format):
    client_sd.sendall(b"Interval finished")
    results = json.loads(client_sd.recv(1024).decode('utf-8'))
    utils.printResults(results, format)

def sendData(duration, start_time, client_sd):
    while time.time() - start_time < duration:
        client_sd.sendall(data)
    
def sendACK(client_sd, format):
    client_sd.sendall(b"BYE")
    results = json.loads(client_sd.recv(1024).decode('utf-8'))
    utils.printResults(results, format)

    client_sd.close()

def handleClientData(start_time, total_received, addr, format, client):
    elapsed_time = time.time() - start_time
    bandwidth = "{:.2f}".format(int(total_received / elapsed_time / (1000 * 1000)))
    recieved = "{:.2f}".format(total_received)
    results = { "ip": f"{addr[0]}:{addr[1]}", "interval": "0.0 - 10.0", "recieved": recieved, "bandwidth": f"{bandwidth} Mbps" }

    utils.printResults(results, format)
    client.sendall(json.dumps(results).encode('utf-8'))