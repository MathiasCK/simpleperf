from sys import argv
from getopt import getopt
from . import responses, validators

opts, args = getopt(argv[1:], "scI:t:i:P:n:b:p:f:", ["server", "client", "bind=", "port=", "format=", "serverip=", "time=", "interval=", "parallel", "num="])

def checkMode():
    for opt, arg in opts:
      if opt in ('-s', '--server'):
          return "server"
      if opt in ('-c', '--client'):
          return "client"  
    responses.syntaxError("You must run either in server or client mode")

def checkServerOpts():
    global bind
    bind = "localhost"
    global port
    port = "8088"
    global format
    format = "MB"

    for opt, arg in opts:
      if opt in ('-b', '--bind'):
          validators.isValidIP(arg)
          bind = arg
      if opt in ('-p', '--port'):
          validators.isValidPort(arg)
          port = int(arg)
      if opt in ('-f', '--format'):
        validators.isValidFormat(arg)
        format = arg.upper()

    return bind, port, format

def checkClientOpts():
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

    for opt, arg in opts:
        if opt in ('-I', '--serverip'):
          validators.isValidIP(arg)
          ip = arg
        if opt in ('-p', '--port'):
            arg = int(arg)
            validators.isValidPort(arg)
            port = arg
        if opt in ('-f', '--format'):
            validators.isValidFormat(arg)
            format = arg.upper()
        if opt in ('-i', '--interval'):
            arg = int(arg)
            validators.isValidInterval(arg, time)
            interval = arg
        if opt in ('-P', '--parallel'):
            validators.isValidParallel(arg)
            parallel = arg

    return ip, port, time, format, interval, parallel

def handleFormat(format, recieved):
    if format == 'MB':
         return f"{float(recieved) / 1000000} MB"
    if format == "KB":
       return f"{float(recieved) / 1000} KB"
    if format == "B":
       return f"{recieved} B"

def printResults(results, format):
    recieved = handleFormat(format, results.get("recieved"))

    print("{:<20} {:<15} {:<15} {:<15}".format('ID','Interval','Recieved','Rate'))
    print("{:<20} {:<15} {:<15} {:<15}".format(results.get("ip"), results.get("interval"), recieved, results.get("bandwidth")))