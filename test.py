from roboclaw import Roboclaw
from serial import Serial
import time

motor_com_port = 'COM18'

serial_obj = Serial(motor_com_port, 38400) # default baudrate is 38400
rc = Roboclaw(serial_obj)
rc.forward_backward_mixed(64) # stops both motors

timing = 10
power_rating = 32
stop = 0

while 1:
    rc.forward_m1((power_rating))  # 1/4 power forward
    rc.backward_m2((power_rating))  # 1/4 power backward
    time.sleep((timing))

    rc.backward_m1((power_rating))  # 1/4 power backward
    time.sleep((timing))

    rc.backward_m1((stop))  # Stopped
    rc.forward_m2((stop))  # Stopped
    time.sleep((timing))

    m1duty = 16
    m2duty = -16
    rc.forward_backward_m1(64+m1duty)  # 1/4 power forward
    rc.forward_backward_m2(64+m2duty)  # 1/4 power backward
    time.sleep((timing))

    m1duty = -16
    m2duty = 16
    rc.forward_backward_m1(64+m1duty)  # 1/4 power backward
    rc.forward_backward_m2(64+m2duty)  # 1/4 power forward
    time.sleep((timing))

    rc.forward_backward_m1(64)  # Stopped
    rc.forward_backward_m2(64)  # Stopped
    time.sleep((timing))


