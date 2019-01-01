"""Signals to be sent between the drone and client."""

import struct

import flight_maneuvers


class Signals:
    """Signals in byte form."""

    # comunicational commands
    OK          = (0).to_bytes(1, "big")
    QUIT        = (1).to_bytes(1, "big")

    # Postional commands
    LEFT        = (3).to_bytes(1, "big")
    RIGHT       = (4).to_bytes(1, "big")
    UP          = (5).to_bytes(1, "big")

    # Flight commands
    DOWN        = (6).to_bytes(1, "big")
    HOME        = (7).to_bytes(1, "big")
    ARM         = (8).to_bytes(1, "big")

    # special commands
    PWD_REQUEST = (9).to_bytes(1, "big")
    WRONG_PWD   = (10).to_bytes(1, "big")
    RIGHT_PWD   = (11).to_bytes(1, "big")
    PING_RQST   = (12).to_bytes(1, "big")
    PING        = (13).to_bytes(1, "big")

    # benchmark
    TIME        = (14).to_bytes(1, "big")


class Bcolors:
    """Color squences for printing."""

    OKBLUE = '\x1b[2;34m'
    OKGREEN = '\x1b[2;32m'
    WARNING = '\x1b[2;31m'
    FAIL = '\x1b[2;41m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[2:1m'
    UNDERLINE = '\x1b[4;m'


commands = {}


class Send():
    """Commands to be used when sending."""

    def move(motorID, speed, commandID=1):
        """Counterpart to Recive.move."""
        output = struct.pack('<h', commandID)
        output += struct.pack('<h', motorID)
        output += struct.pack('<h', speed)
        return output
    



class Recive():
    """Commands to be used when reciving."""

    def command(*, commandID=None):
        """Add commands using this Decorator.

        usage: @command(commandID = {ID})
        ID: int > 0

        Keyword Arguments:
            commandID {int} -- id by wich the command is then called (default: {None})
        """
        def deco(f):
            commands[commandID or f.__name__] = f
            return f
        return deco

    def handle_input(b):
        """Simply calls correct method to handle the rest of the command data.

        Arguments:
            b {bytes} -- input bytes
        """
        try:
            call = struct.unpack('<h', b[:2])[0]
            return commands[call](b)
        except Exception as e:
            print(Bcolors.WARNING + "\runexpected data: {} \n after the following error: {}".format(
                b, e) + Bcolors.ENDC, end="\n-> ")
            return None

    @command(commandID=1)
    def move(b):
        """Encode data for a move command."""
        motorID = struct.unpack('<h', b[2:4])[0]
        speed = struct.unpack('<h', b[4:6])[0]

        print(motorID, speed)  # replace this with actual motor controll method
        flight_maneuvers.set_speed(motorID, speed)
