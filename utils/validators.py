import re
from . import responses

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

def isValidInterval(interval, time):
    if interval > time:
      return responses.syntaxError("Interval cannot be greater than -t flag (default 10 seconds)")