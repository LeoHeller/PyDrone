import struct


commands = {}
def command(*, name=None):
    def deco(f):
        commands[name or f.__name__] = f
        return f
    return deco

@command(name=15)
def move(b):
    motorID = struct.unpack('<h', b[2:4])[0]
    speed = struct.unpack('<h', b[4:6])[0]

    print(motorID, speed)
    # do whatever with the motors




def pack_input_move_command(motorID, speed):
    '''
    Args match types and descriptions in table below

    Command created is 8 bytes:

    bytes   type    desc
    1-2     <h      int (C.short) command ID
    3       <?      bool motor left/right (right is true)
    4       <?      bool motor front/back (front is true)
    5-6     <h      int (C.short) motor speed in percent
    7-8     null    padding is ok here to make it an exponent of 2 for reasons

    Returns bytes
    '''

    output = struct.pack('<h', 15)  # 15 is our 'move' command
    output += struct.pack('<h', motorID)
    output += struct.pack('<h', speed)

    return output


def handle_input(b):
    '''
    This happend on drone

    b (bytes): input from controller

    Simply calls correct method to handle the rest of the command data

    Returns whatever you need it to bro
    '''

    call = struct.unpack('<h', b[:2])[0]

    commands[call](b)



handle_input(pack_input_move_command(1,25))