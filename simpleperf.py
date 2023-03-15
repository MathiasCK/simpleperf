import client, server
from utils import utils

def Main():
    mode = utils.checkMode()
    if mode == "server":
        server.Main()
    elif mode == "client":
        client.Main()
    else:
        raise Exception("Error: you must run either in server or client mode")
    

if __name__ == "__main__":
    Main()