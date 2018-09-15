import server, time, os

Server = server.HandleSockets("127.0.0.1", 1337, "admin")
Server.isDaemon = True
Server.start()

try:
    while True:
        i = input("-> ")
        if i == "q":
            Server.close_all()
            os._exit(1)
        else:
            Server.send(i)
except:
    Server.close_all()
    os._exit(1)