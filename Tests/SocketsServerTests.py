import Sockets
import signals


def on_message(data):
    print(f"\r{data}\n > ", end="")


server = Sockets.HandleSockets("localhost", 1337, "pwd", on_message, mode="s")
server.start()

while 1:
    inp = input("> ")
    if inp == "q" or inp == b"":
        server.close_all()
    else:
        server.send(inp)
