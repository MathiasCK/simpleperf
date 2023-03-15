import client, server
from utils import utils

def Main():
    mode = utils.checkMode()
    if mode == "server":
        server.Main()
    elif mode == "client":
        client.Main()
    else:
        raise Exception("Not valid")
    

if __name__ == "__main__":
    Main()