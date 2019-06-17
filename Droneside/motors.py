"""Controll the motors."""


class Motors():
    """class for controlling motors."""

    def __init__(self, debug=True):
        """Initialize the pigpio deamon."""

        import time
        import os
        from subprocess import Popen, PIPE


        # set debugmode
        self.debug = debug
        if not self.debug:
            import pigpio
            if not os.path.isfile("/var/run/pigpio.pid"):
                # start pigpio daemon
                Popen(['sudo', 'pigpiod', '-s', '1'],
                      stdout=PIPE, stderr=PIPE)
                print("pigpiod started")
                time.sleep(2)

            # establish connection with the rpi
            self.pi = pigpio.pi()

        # pins for motors
        self.motors = {
            0: 17,  # "M_FL"
            1: 18,  # "M_FR"
            2: 22,  # "M_BL"
            3: 27   # "M_BR"
        }
        print(self.debug)
    # motor: M_xx ; speed: 0-100

    def set_speed(self, motor, speed):
        """Set the speed of a motor.

        First converts the speed to servo pulsewidth.

        Arguments:
            motor {int} -- motorID of 0-3
            speed {int} -- speed percentage 0-100
        """
        # pulsewidth range: 0; 700 - 2000
        if speed < 0:
            speed = 0
        else:
            pulsewidth = (speed/100.0) * 1300 + 700

        if not self.debug:
            try:
                self.pi.set_servo_pulsewidth(
                    self.motors[motor], pulsewidth)  # set Pulsewidth
            except Exception as e:
                print(e)
        else:
            print("setting speed of motor {} on pin {} to pulsewidth: {} inorder to reach {}% Thrust$
                  motor, self.motors[motor], pulsewidth, speed))


    def clean_up(self):
        """Stop all motors and cut conection"""
        if not self.debug:
            # set speed to 0
            for motor in self.motors:
                self.pi.set_servo_pulsewidth(self.motors[motor], 0)
            # disconnect from rpi
            self.pi.stop()
