from sys import argv
from getopt import getopt
from . import responses, validators
import re
import json

# Optional argumens provided on startup
opts, args = getopt(argv[1:], "scI:t:i:P:n:b:p:f:", ["server", "client", "bind=", "port=", "format=", "serverip=", "time=", "interval=", "parallel", "num="])

# Check what mode the process should be ran in
def checkMode():
    for opt, arg in opts:
      if opt in ('-s', '--server'):
          return "server"
      if opt in ('-c', '--client'):
          return "client"  
    # Raise exception if neither -c or -s flag is provided
    responses.syntaxError("You must run either in server or client mode")

# Check for optional arguments for server startup
def checkServerOpts():
    # Default values for bind, port and format
    global bind
    bind = "localhost"
    global port
    port = "8088"
    global format
    format = "MB"

    # Check default values should be overwritten
    for opt, arg in opts:
      if opt in ('-b', '--bind'):
          # Validate ip address
          validators.isValidIP(arg)
          bind = arg
      if opt in ('-p', '--port'):
          # Validate port number
          validators.isValidPort(arg)
          port = int(arg)
      if opt in ('-f', '--format'):
        # Validate format
        validators.isValidFormat(arg)
        format = arg.upper()

    return bind, port, format

# Check for optional arguments for client startup
def checkClientOpts():
    # Default values for ip, port, time, format, interval, parallel and num
    global ip # server IP addres (default localhost)
    ip = "localhost"
    global port # server port (default 8088)
    port = "8088"
    global time # total amount of time for data transfer (default 10 seconds)
    time = 10
    global format
    format = "MB" # format data should print (default MB)
    global interval # total amount of data transfer intervals (default None = 1 interval)
    interval = None
    global parallel # total amount of paralell connections (default 1)
    parallel = 1
    global num # total amount of data (default None = 1000bytes)
    num = None

    # Check default values should be overwritten
    for opt, arg in opts:
        if opt in ('-I', '--serverip'):
          # Validate ip address
          validators.isValidIP(arg)
          ip = arg
        if opt in ('-t', '--time'):
          # Validate ip address
          #validators.isValidIP(arg)
          time = int(arg)
        if opt in ('-p', '--port'):
            # Validate port
            arg = int(arg)
            validators.isValidPort(arg)
            port = arg
        if opt in ('-f', '--format'):
            # Validate format
            validators.isValidFormat(arg)
            format = arg.upper()
        if opt in ('-i', '--interval'):
            # Validate interval
            arg = int(arg)
            validators.isValidInterval(arg, time)
            interval = arg
        if opt in ('-P', '--parallel'):
            # Validate parallel
            arg = int(arg)
            validators.isValidParallel(arg)
            parallel = arg
        if opt in ('-n', '--num'):
            # Validate num
            validators.isValidByteNum(arg)
            num = arg


    return ip, port, time, format, interval, parallel, num

# Format total amount of data recieved
# @format -> MB/KB/B
# @recieved -> Total data recieved in bytes
def handleFormat(format, recieved):
    if format == 'MB':
        recieved = "{:.2f}".format(float(recieved / 1000000))
        return f"{float(recieved)} MB"
    if format == "KB":
       recieved = "{:.2f}".format(float(recieved / 1000))
       return f"{float(recieved)} KB"
    
    recieved = "{:.2f}".format(float(recieved))
    return f"{recieved} B"

# Handle --num flag if provided
# @num -> string (valid format ex. 1000MB)
def handleNumFlag(num):
    # Split num value into array with -> [number, value]
    match = re.match(r"([0-999999]+)((?:MB|KB|B)$)", num, re.I)
    if match:
        items = match.groups()

    # First part of string -> number
    num = int(items[0])
    # Second part of string -> string (MB/KB/B)
    numFormat = items[1]
    
    # If format is MB divide by 1000000 to get bytes
    if numFormat == 'MB':
        return num * 1000000

    # If format is KB divide by 1000 to get bytes
    if numFormat == 'KB':
        return num * 1000
    
    # Return bytes
    return num

# Print data header
def printHeader():
    # Print header
    print("{:<20} {:<15} {:<15} {:<15}".format('ID','Interval','Recieved','Rate'))

# Print results
# @results -> JSON object containing, ip address, interval, recieved data, and bandwidth
def printResults(results, format):
    # See handleFormat()
    recieved = handleFormat(format, results.get("recieved"))
    # Print values
    print("{:<20} {:<15} {:<15} {:<15}".format(results.get("ip"), results.get("interval"), recieved, results.get("bandwidth")))

# Print data in intervals
# @client_sd -> client socket
# @format -> format to print data
def printItervalData(client_sd, format):
    # Print data recieved from server
    results = json.loads(client_sd.recv(1024).decode('utf-8'))
    # See printResults
    printResults(results, format)

# Make JSON object from data recieved
# @addr -> client ip address & port
# @interval -> Total interval time
# @total_received -> total amount of data received in bytes
# @bandwidth -> calculated bandwidth
def makeJSONObj(addr, interval, total_received, bandwidth):
    return { "ack": "ACK/BYE", "ip": f"{addr[0]}:{addr[1]}", "interval": interval, "recieved": total_received, "bandwidth": f"{bandwidth} Mbps" }