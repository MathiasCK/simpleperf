from utils import utils
import time
import json
from . import responses
from math import floor

# Send data to server
# @data -> bytes (default 1000 bytes)
# @duration -> Time data should be sent to server (default 10 seconds)
# @client_sd -> client socket connection
# @format -> Format data print
def sendData(data, duration, client_sd, format):
    t_end = time.time() + duration
    while time.time() < t_end:
        # Send data as long as duration valid
        client_sd.send(data)
    # See sendACK()
    sendACK(client_sd, format)

# Send data to server in interval
# @data -> bytes (default 1000 bytes)
# @interval -> Time in intervals data should be sent
# @duration -> Total time data should be sent (in intervals)
# @client_sd -> client socket connection
# @format -> Format data print
def sendIntervalData(data, interval, duration, client_sd, format):
    # See utils.printHeader()
    utils.printHeader()
    # As long as the total time is above interval
    while duration >= interval:
        # Total interval time
        t_end = time.time() + interval
        # As long as time is within interval
        while time.time() < t_end:
            # Send data to client
            client_sd.sendall(data)
        # Send print request to server after interval has ran out
        intervalCount = b"i" * interval
     
        client_sd.sendall(intervalCount)
        # Print data received from server on the client
        utils.printItervalData(client_sd, format)
        # Decrement duration
        duration -= interval
    # After duration is finished, send ACK indicating interval is finished
    # See -> sendIntervalACK()
    sendIntervalACK(client_sd)

# Send ACK to server indicating data transfer is done
# @client_sd -> client socket connection
# @format -> Format data should be printed
def sendACK(client_sd, format):
    # Send ACK
    client_sd.send(b"BYE")
    
    # Recieve ACK from server
    results = json.loads(client_sd.recv(1024).decode('utf-8'))

    # If ACK is recieved print data
    if results.get('ack') == "ACK/BYE":
        # See utils.printHeader()
        utils.printHeader()
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
    bandwidth = "{:.2f}".format(float(total_received / elapsed_time / (1000 * 1000)))
    
    # Format elapsed_time
    elapsed_time = "{:.1f}".format(floor(elapsed_time))
    
    # Format interval
    interval = f"0.0 - {elapsed_time}"
    
    # See utils.makeJSONObj
    results = utils.makeJSONObj(addr, interval, total_received, bandwidth)

    # Print results on server -> see utils.printResults()
    utils.printResults(results, format)
    # Send results to client
    client.sendall(json.dumps(results).encode('utf-8'))

# Print data recieved from client in intervals
# @start_time -> time since transfer started
# @total_received -> Total amout of data recieved (bytes)
# @format -> Format data should be printed
# @client -> client socket connection
# @i -> start time in interval
# @diff -> end time in interval
def printClientIntervalData(start_time, total_received, addr, format, client, interval_start, interval_end):
    # Only print header if interval_start = 0.0
    if interval_start == 0.0:
        # See utils.printHeader()
        utils.printHeader()

    # Interval total time since start of transer
    interval_time = time.time() - start_time - interval_start
    # Calculate bandwidth
    bandwidth = "{:.2f}".format(int(total_received / interval_time / (1000 * 1000)))

    # Format interval 
    interval = f"{interval_start} - {interval_end}"

    # See utils.makeJSONObj
    results = utils.makeJSONObj(addr, interval, total_received, bandwidth)

    # Print results on server -> see utils.printResults()
    utils.printResults(results, format)
    # Send results to client
    client.sendall(json.dumps(results).encode('utf-8'))

# Handle data recieved from client in intervals
# @client -> client conection
# @addr -> client ip address & port
# @format -> format to print data
def handleClientIntervalData(addr, format, client):
    # Global counter for end interval value
    global interval_end
    interval_end = 0.0
    # Global counter for start interval value
    global interval_start
    interval_start = 0.0
    # Global value for interval
    global interval
    interval = 0.0
    # Start of data transfer
    start_time = time.time()
    # Total data received
    total_received = 0
    # Send Interval ACK to client
    client.sendall(b"Interval ACK")

    while True:
        # Recieve data from client
        data = client.recv(1000)
        # Break if interval is finished
        if data == b"Interval finished":
            break
        # Add lenght of data to total recieved data
        total_received += len(data)
        # If client sends bytes containing x amount of i values = interval is finished
        if b"i" in data:
            # Only set interval value on first interval
            # Interval end value is total number of "i" bytes sent
            if interval_start == 0.0:
                interval = float(str(data).count('i'))
                interval_end = float(str(data).count('i'))    
            
            # See printClientIntervalData()
            printClientIntervalData(start_time, total_received, addr, format, client, interval_start, interval_end)

            # Update start & end
            interval_start += interval
            interval_end += interval

            # Reset total_received after interval
            total_received = 0