from sys import argv
from getopt import getopt
from . import responses, validators

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
    global ip
    ip = "localhost"
    global port
    port = "8088"
    global time
    time = 10
    global format
    format = "MB"
    global interval
    interval = None
    global parallel
    parallel = 1

    # Check default values should be overwritten
    for opt, arg in opts:
        if opt in ('-I', '--serverip'):
          # Validate ip address
          validators.isValidIP(arg)
          ip = arg
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
            validators.isValidParallel(arg)
            parallel = arg

    return ip, port, time, format, interval, parallel

# Format total amount of data recieved
# @format -> MB/KB/B
# @recieved -> Total data recieved (default MB)
def handleFormat(format, recieved):
    if format == 'MB':
         return f"{float(recieved) / 1000000} MB"
    if format == "KB":
       return f"{float(recieved) / 1000} KB"
    if format == "B":
       return f"{recieved} B"

# Print results
# @results -> JSON object containing, ip address, interval, recieved data, and bandwidth
def printResults(results, format):
    # See handleFormat()
    recieved = handleFormat(format, results.get("recieved"))

    # Print header
    print("{:<20} {:<15} {:<15} {:<15}".format('ID','Interval','Recieved','Rate'))
    # Print values
    print("{:<20} {:<15} {:<15} {:<15}".format(results.get("ip"), results.get("interval"), recieved, results.get("bandwidth")))