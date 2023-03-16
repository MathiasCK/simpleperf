import client, server
from utils import utils

def Main():
    if utils.checkMode() == "server":
        return server.Main()
    client.Main()
    
if __name__ == "__main__":
    Main()