from utils import utils
import time
import json
from . import responses
import re

def printItervalData(client_sd, format):
    client_sd.sendall(b"Interval")
    results = json.loads(client_sd.recv(1024).decode('utf-8'))
    utils.printResults(results, format)

def sendData(data, duration, start_time, client_sd):
    while time.time() - start_time < duration:
        client_sd.sendall(data)
    
def sendACK(client_sd, format):
    client_sd.sendall(b"BYE")
    ack = client_sd.recv(1024).decode('utf-8')

    if ack == "ACK/BYE":
        results = json.loads(client_sd.recv(1024).decode('utf-8'))
        utils.printResults(results, format)
    else:
        responses.connectionError("ACK could not be verified")

    client_sd.close()

def sendIntervalACK(client_sd):
    client_sd.sendall(b"Interval finished")
    client_sd.close()

def handleClientData(start_time, total_received, addr, format, client):
    elapsed_time = time.time() - start_time
    bandwidth = "{:.2f}".format(int(total_received / elapsed_time / (1000 * 1000)))
    recieved = "{:.2f}".format(total_received)
    
    elapsed_time = "{:.1f}".format(elapsed_time)
    results = { "ip": f"{addr[0]}:{addr[1]}", "interval": f"0.0 - {elapsed_time}", "recieved": recieved, "bandwidth": f"{bandwidth} Mbps" }

    utils.printResults(results, format)
    client.sendall(b"ACK/BYE")
    client.sendall(json.dumps(results).encode('utf-8'))

def handleClientIntervalData(start_time, total_received, addr, format, client, i, diff):
    elapsed_time = time.time() - start_time
    bandwidth = "{:.2f}".format(int(total_received / elapsed_time / (1000 * 1000)))
    recieved = "{:.2f}".format(total_received)
    results = { "ip": f"{addr[0]}:{addr[1]}", "interval": f"{i} - {diff}", "recieved": recieved, "bandwidth": f"{bandwidth} Mbps" }

    utils.printResults(results, format)
    client.sendall(json.dumps(results).encode('utf-8'))

def handleNumFlag(num):
    match = re.match(r"([0-999999]+)((?:MB|KB|B)$)", num, re.I)
    if match:
        items = match.groups()
    num = int(items[0])
    numFormat = items[1]
    
    if numFormat == 'MB':
        return num * 1000000

    if numFormat == 'KB':
        return num * 1000
    
    return num
