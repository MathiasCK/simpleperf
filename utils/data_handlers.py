from utils import utils
import time
import json
from . import responses

# Send data to server
# @data -> bytes (default 1000 bytes)
# @duration -> Time data should be sent to server (default 10 seconds)
# @start_time -> Time since connection started
# @client_sd -> client socket connection
def sendData(data, duration, start_time, client_sd):
    while time.time() - start_time < duration:
        # Send data as long as duration valid
        client_sd.sendall(data)

# Send ACK to server indicating data transfer is done
# @client_sd -> client socket connection
# @format -> Format data should be printed
def sendACK(client_sd, format):
    # Send ACK
    client_sd.sendall(b"BYE")
    # Recieve ACK from server
    ack = client_sd.recv(1024).decode('utf-8')

    # If ACK is recieved print data
    if ack == "ACK/BYE":
        # See utils.printHeader()
        utils.printHeader()
        # Recieve data from server
        results = json.loads(client_sd.recv(1024).decode('utf-8'))
        # See -> utils printResults()
        utils.printResults(results, format)
    else:
        # ACK not valid error handling
        responses.connectionError("ACK could not be verified")

    # Close client connection
    client_sd.close()

# Send ACK indicating all intervals have completed to server
# @client_sd -> client socket connection
def sendIntervalACK(client_sd):
    # Send bytes to server
    client_sd.sendall(b"Interval finished")
    # Close connection
    client_sd.close()

# Handle data recieved from client
# @start_time -> time since transfer started
# @total_received -> Total amout of data recieved (bytes)
# @format -> Format data should be printed
# @client -> client socket connection
def handleClientData(start_time, total_received, addr, format, client):
    # See utils.printHeader()
    utils.printHeader()
    # Time since start of transer
    elapsed_time = time.time() - start_time
    # Calculate bandwidth
    bandwidth = "{:.2f}".format(int(total_received / elapsed_time / (1000 * 1000)))
    
    # Format elapsed_time
    elapsed_time = "{:.1f}".format(elapsed_time)
    # Make JSON object from data recieved
    results = { "ip": f"{addr[0]}:{addr[1]}", "interval": f"0.0 - {elapsed_time}", "recieved": total_received, "bandwidth": f"{bandwidth} Mbps" }

    # Print results on server -> see utils.printResults()
    utils.printResults(results, format)
    # Send ACK to client indicating data transfer is done
    client.sendall(b"ACK/BYE")
    # Send results to client
    client.sendall(json.dumps(results).encode('utf-8'))

# Handle data recieved from client in intervals
# @start_time -> time since transfer started
# @total_received -> Total amout of data recieved (bytes)
# @format -> Format data should be printed
# @client -> client socket connection
# @i -> start time in interval
# @diff -> end time in interval
def handleClientIntervalData(start_time, total_received, addr, format, client, i, diff):
    # Only print header if i = 0.0
    if i == 0.0:
        # See utils.printHeader()
        utils.printHeader()
    
    # Time since start of transer
    interval_time = time.time() - start_time - i
    # Calculate bandwidth
    bandwidth = "{:.2f}".format(int(total_received / interval_time / (1000 * 1000)))

    # Make JSON object from data recieved
    results = { "ip": f"{addr[0]}:{addr[1]}", "interval": f"{i} - {diff}", "recieved": total_received, "bandwidth": f"{bandwidth} Mbps" }

    # Print results on server -> see utils.printResults()
    utils.printResults(results, format)
    # Send results to client
    client.sendall(json.dumps(results).encode('utf-8'))
