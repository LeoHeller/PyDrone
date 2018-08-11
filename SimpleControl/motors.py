import pigpio


class Motors():
    def __init__(self):
        # set debugmode
        self.debug = True
        
        # establish connection with the rpi
        self.pi = pigpio.pi()

        # pins for motors
        self.motors = {
            "M_FL" : 0,
            "M_FR" : 1,
            "M_BL" : 2,
            "M_BR" : 3
        }
        
    # motor: M_xx ; speed: 0-100
    def set_speed(self, motor, speed):
        # convert speed % to PWM dutycycle
        # pwm range: 0 - 255
        
        cycle = 255 * (speed / 100)

        print("setting speed of motor {} on pin {} to {} cycles inorder to reach {}% Thrust".format(motor, self.motors[motor], cycle, speed))
        if not self.debug:
            pi.set_PWM_dutycycle(self.motors[motor], speed) # set PWM

    # stop all motors, and cut conection
    def clean_up(self):
        # set speed to 0
        for motor in self.motors:
            pi.set_PWM_dutycycle(self.motors[motor], 0)
        # disconnect from rpi
        pi.stop()
        
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
        break
    parsed = parse(user_input)
    if parse(user_input):
        myMotors.set_speed(parsed[0],parsed[1]) 


