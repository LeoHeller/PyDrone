import Sockets
import signals


def on_message(data):
    if data == signals.Signals.PWD_REQUEST:
        client.send(client.password)
        print("sent password")
    elif data == b"":
        client.close_all()
    else:
        print(f"\r{data}\n > ", end="")


client = Sockets.HandleSockets("192.168.10.1", 1337, "admin", on_message, mode="c")
client.start()

while 1:
    inp = input("> ")
    if inp == "q":
        client.close_all()
    else:
        client.send(inp)
