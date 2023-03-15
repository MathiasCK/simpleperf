from sys import argv
from getopt import getopt

opts, args = getopt(argv[1:], "scb:p:f:", ["server", "client"])

def checkMode():
    for opt, arg in opts:
      if opt == "-s":
          return "server"
      if opt == "-c":
          return "client"