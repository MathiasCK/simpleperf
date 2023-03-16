import re
from . import responses

# Checks if IP address provided by -I flag is valid with regex
# @ip -> string 
def isValidIP(ip):
    if str(ip) == 'localhost':
       return
    isValid = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip)
    if str(isValid) == "None":
       responses.syntaxError("Please provide a valid IP address")

# Checks if port provided by -p flag is valid within the range 1024 - 65535
# @port -> number 
def isValidPort(port):
   if not int(port) >= 1024 and int(port) <= 65535:
      responses.syntaxError("Please provide a valid port (range 1024 -> 65535)")

# Checks if format provided by -f flag is valid with regex
# @format -> string 
def isValidFormat(format):
   isValid = re.match(r"^(?:MB|KB|B)$", format, re.IGNORECASE)
   if str(isValid) == "None":
       responses.syntaxError("Please provide a valid format (MB/KB/B)")

# Checks if interval provided by -i flag is valid greater than the total time
# @interval -> number
# @time -> number (total time client should send data to client) 
def isValidInterval(interval, time):
    if interval > time:
      responses.syntaxError("Interval cannot be greater than -t flag (default 10 seconds)")

# Checks if paralell provided by -p flag is larger than 1 and less than 0
# @value -> number
def isValidParallel(value):
   if value < 1 or value > 5:
      responses.syntaxError("Parallel value must be in the rage 1-5")

# Checks if bytenumber provided by -n flag is valid
# @value -> string
def isValidByteNum(value):
   isValid = re.match(r"^[0-999999]+(?:MB|KB|B)$", value, re.IGNORECASE)
   if str(isValid) == "None":
       responses.syntaxError("Number (0-999999) followed by a valid format (MB/KB/B)")