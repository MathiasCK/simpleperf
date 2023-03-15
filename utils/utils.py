from sys import argv
from getopt import getopt

opts, args = getopt(argv[1:], "scb:p:f:", ["server", "client", "bind=", "port=", "format="])

def checkMode():
    for opt, arg in opts:
      if opt in ('-s', '--server'):
          return "server"
      if opt in ('-c', '--client'):
          return "client"
      
def checkServerOpts():
    global bind
    bind = "localhost"
    global port
    port = "8000"
    global format
    format = "MB"

    for opt, arg in opts:
      if opt in ('-b', '--bind'):
          bind = arg
      if opt in ('-p', '--port'):
          print("ARG", arg)
          print("OPT", opt)
          port = arg
          print("PORT", port)
      if opt in ('-f', '--format'):
        format = arg

    return bind, port, format