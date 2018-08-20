import pigpio


class Motors():
    def __init__(self):
        # set debugmode
        self.debug = True
        
        # establish connection with the rpi
        self.pi = pigpio.pi()

        # pins for motors
        self.motors = {
            "M_FL" : 17,
            "M_FR" : 18,
            "M_BL" : 22,
            "M_BR" : 27
        }
        
        for motor in self.motors:
            self.pi.set_PWM_frequency(self.motors[motor], 1600)
    
    # motor: M_xx ; speed: 0-100
    def set_speed(self, motor, speed):
        # convert speed % to PWM dutycycle
        # pwm range: 0 - 255
        
        cycle = 255 * (speed / 100.0)

        print("setting speed of motor {} on pin {} to {} cycles inorder to reach {}% Thrust".format(motor, self.motors[motor], cycle, speed))
        if not self.debug:
            self.pi.set_PWM_dutycycle(self.motors[motor], speed) # set PWM

    # stop all motors, and cut conection
    def clean_up(self):
        # set speed to 0
        for motor in self.motors:
            self.pi.set_PWM_dutycycle(self.motors[motor], 0)
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


