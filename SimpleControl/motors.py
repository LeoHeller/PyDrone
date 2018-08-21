import pigpio, time, os


class Motors():
    def __init__(self):
        # set debugmode
        self.debug = False
        if not self.debug:
            if not os.path.isfile("/var/run/pigpio.pid"):
                # start pigpio daemon 
                os.system("sudo pigpiod -s 1")
                time.sleep(2)

            # establish connection with the rpi
            self.pi = pigpio.pi()

        # pins for motors
        self.motors = {
            "M_FL" : 17,
            "M_FR" : 18,
            "M_BL" : 22,
            "M_BR" : 27
        }
        
    
    # motor: M_xx ; speed: 0-100
    def set_speed(self, motor, speed):
        # convert speed % to servo pulsewidth
        
        #pulsewidth range: 0; 500 - 2500
        
        if speed != 0:
            pulsewidth = 2000 * (speed / 100) + 500
        else:
            pulsewidth = 0

        print("setting speed of motor {} on pin {} to pulsewidth: {} inorder to reach {}% Thrust".format(motor, self.motors[motor], pulsewidth, speed))
        if not self.debug:
            self.pi.set_servo_pulsewidth(self.motors[motor], pulsewidth) # set Pulsewidth

    # stop all motors, and cut conection
    def clean_up(self):
        if not self.debug:
            # set speed to 0
            for motor in self.motors:
                self.pi.set_servo_pulsewidth(self.motors[motor], 0)
            # disconnect from rpi
            self.pi.stop()
        
user_input = ""      
myMotors = Motors()


def parse(instr):
    # m_fl 100
    motor, speed = instr.upper().split(" ")
    if motor in myMotors.motors and int(speed) in range(100):
        return motor, int(speed)



while True:
    user_input = input(" -> ")
    if user_input == "q":
        myMotors.clean_up()
        break
    parsed = parse(user_input)
    if parse(user_input):
        myMotors.set_speed(parsed[0],parsed[1]) 


