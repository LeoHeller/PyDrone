import server

Server = server.Handle_Sockets("127.0.0.1", 1337, "admin")

def mon_message(message):
    print(message.decode())

Server.on_message = mon_message
