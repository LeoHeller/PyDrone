class Signals:
    # comunicational commands
    OK          = (0).to_bytes(1,"big")
    QUIT        = (1).to_bytes(1,"big")

    # Postional commands
    LEFT        = (3).to_bytes(1,"big")
    RIGHT       = (4).to_bytes(1,"big")
    UP          = (5).to_bytes(1,"big")
    DOWN        = (6).to_bytes(1,"big")
    HOME        = (7).to_bytes(1,"big")

    # special commands
    PWD_REQUEST = (8).to_bytes(1,"big")
    WRONG_PWD   = (9).to_bytes(1,"big")
    RIGHT_PWD   = (10).to_bytes(1,"big")
    
class Bcolors:
    OKBLUE = '\x1b[2;34m'
    OKGREEN = '\x1b[2;32m'
    WARNING = '\x1b[2;31m'
    FAIL = '\x1b[2;41m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[2:1m'
    UNDERLINE = '\x1b[4;m'