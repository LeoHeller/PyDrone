import sys

sys.path.insert(0, '../modules/')
import Sockets
import sensors
import signals
import flight_maneuvers
import Controller
from utils import DoEvery


class Drone:
    def __init__(self, address, port, password):
        self.address = address
        self.port = port
        self.password = password

        self.Server = Sockets.HandleSockets(self.address, self.port, self.password, mode="s",
                                            on_message=self.on_message)
        self.Server.start()

        self.Sensors = sensors.Sensors()

        self.controller = Controller.SimpleController()

        self.loop = DoEvery(1 / 50, self.update())
        self.loop.start()

        self.input_loop()

    def input_loop(self):
        while Sockets.should_be_running:
            i = input("\r-> ")
            # parse for commands
            if i == "q":
                self.Server.close_all()
                Sockets.should_be_running = False
                exit()
            elif not Sockets.no_connection:
                self.Server.send(i)

    def update(self):
        heading = self.Sensors.read()
        next_action = self.controller.on_update(heading, flight_maneuvers.motorspeeds)
        flight_maneuvers.set_motor_speeds(next_action)

    def on_message(self, data):
        """Quit if the other side quit, otherwise have the input handled."""
        # other side quit
        if data == signals.Signals.QUIT or data == b'':
            Sockets.no_connection = True
            flight_maneuvers.land()
        elif data == signals.Signals.ARM:
            flight_maneuvers.arm()
        elif data == signals.Signals.TEL_REQUEST:
            self.Server.send(signals.Send.telemetry(*self.Sensors.read()))
        else:
            signals.Receive.handle_input(data)

    def send_tel(self, x, y, z):
        self.Server.send(signals.Send.telemetry(x, y, z))


drone = Drone("192.168.2.236", 1337, "admin")
