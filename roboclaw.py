from roboclaw import Roboclaw
from serial import Serial
import time

motor_com_port = 'COM18'

serial_obj = Serial(motor_com_port, 38400) # default baudrate is 38400
rc = Roboclaw(serial_obj)

timing = 10
speed = 64
stop = 0
rc.forward_backward_mixed(64) # stops both motors

while 1:
    rc.forward_m1((speed))  # 1/4 power forward

    rc.backward_m1((speed))  # 1/4 power backward
    time.sleep((timing))

    #stops motor
    rc.forward_backward_mixed(64)
    time.sleep((timing))
