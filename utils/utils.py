from sys import argv
from getopt import getopt
import re

opts, args = getopt(argv[1:], "scI:t:i:P:n:b:p:f:", ["server", "client", "bind=", "port=", "format=", "serverip=", "time=", "interval=", "parallel", "num="])

def checkMode():
    for opt, arg in opts:
      if opt in ('-s', '--server'):
          return "server"
      if opt in ('-c', '--client'):
          return "client"
      
def isValidIP(ip):
    if str(ip) == 'localhost':
       return
    isValid = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip)
    if str(isValid) == "None":
       raise SyntaxError("Please provide a valid IP address")
    
def isValidPort(port):
   if not int(port) >= 1024 and int(port) <= 65535:
      raise SyntaxError("Please provide a valid port (range 1024 -> 65535)")
   
def isValidFormat(format):
   isValid = re.match(r"^(?:MB|KB|B)$", format, re.IGNORECASE)
   if str(isValid) == "None":
       raise SyntaxError("Please provide a valid format (MB/KB/B)")
        
   
      
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
        format = arg

    return bind, port, format


def checkClientOpts():
    global ip
    ip = "localhost"
    global port
    port = "8088"
    global time
    time = 10

    for opt, arg in opts:
      if opt in ('-I', '--serverip'):
          isValidIP(arg)
          ip = arg
      if opt in ('-p', '--port'):
          isValidPort(arg)
          port = int(arg)
    

    return ip, port, time


def printResults(results):
    print("{:<20} {:<15} {:<15} {:<15}".format('ID','Interval','Recieved','Rate'))
    print("{:<20} {:<15} {:<15} {:<15}".format(results.get("ip"),results.get("interval"),results.get("recieved"),results.get("bandwidth")))