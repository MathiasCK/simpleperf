from sys import argv
from getopt import getopt
import re
from . import responses

opts, args = getopt(argv[1:], "scI:t:i:P:n:b:p:f:", ["server", "client", "bind=", "port=", "format=", "serverip=", "time=", "interval=", "parallel", "num="])

def checkMode():
    for opt, arg in opts:
      if opt in ('-s', '--server'):
          return "server"
      if opt in ('-c', '--client'):
          return "client"  
    responses.syntaxError("You must run either in server or client mode")
      
      
def isValidIP(ip):
    if str(ip) == 'localhost':
       return
    isValid = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip)
    if str(isValid) == "None":
       responses.syntaxError("Please provide a valid IP address")
    
def isValidPort(port):
   if not int(port) >= 1024 and int(port) <= 65535:
      responses.syntaxError("Please provide a valid port (range 1024 -> 65535)")
   
def isValidFormat(format):
   isValid = re.match(r"^(?:MB|KB|B)$", format, re.IGNORECASE)
   if str(isValid) == "None":
       responses.syntaxError("Please provide a valid format (MB/KB/B)")
      
def checkServerOpts():
    global bind
    bind = "localhost"
    global port
    port = "8088"
    global format
    format = "MB"

    for opt, arg in opts:
      if opt in ('-b', '--bind'):
          isValidIP(arg)
          bind = arg
      if opt in ('-p', '--port'):
          isValidPort(arg)
          port = int(arg)
      if opt in ('-f', '--format'):
        isValidFormat(arg)
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

    for opt, arg in opts:
      if opt in ('-I', '--serverip'):
          isValidIP(arg)
          ip = arg
      if opt in ('-p', '--port'):
          isValidPort(arg)
          port = int(arg)
      if opt in ('-f', '--format'):
         isValidFormat(arg)
         format = arg.upper()
    

    return ip, port, time, format

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