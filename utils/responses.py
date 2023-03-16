def err(err):
    print(f"Error: {repr(err)}")
    exit()

def connectionRefused(err):
    print(f"Feiled to connect: {repr(err)}")
    exit()

def connectionError(err):
    print(f"Connection error: {repr(err)}")
    exit()

def keyBoardInterrupt():
    print("Stopped by Ctrl+C")
    exit()

def connectionAbortedError():
    print("Connection aborted")
    exit()