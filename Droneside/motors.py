import pigpio, time, os, utils
from subprocess import Popen, PIPE


class Motors():
    def __init__(self):
        utils.setupdate()
        utils.head()
        # set debugmode
        self.debug = True
        if not self.debug:
            if not os.path.isfile("/var/run/pigpio.pid"):
                # start pigpio daemon 
                process = Popen(['sudo', 'pigpiod', '-s', '1'], stdout=PIPE, stderr=PIPE)
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
            pulsewidth = 58 * (speed / 100) + 1601
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
        






def main():
    while True:
        user_input = ""      
        user_input = input(" -> ")
        if user_input == "q":
            myMotors.clean_up()
            break
        if user_input == "test":
            for i in range(100):
                myMotors.set_speed("M_BL", i)
            time.sleep(0.1)
        parsed = parse(user_input)
        if parsed:
            myMotors.set_speed(parsed[0],parsed[1]) 

def parse(instr):
    # m_fl 100
    motor, speed = instr.upper().split(" ")
    if motor in myMotors.motors and float(speed) in range(100):
        return motor, int(speed)
if __name__ == '__main__':
    myMotors = Motors()
    main()


