from roboclaw import Roboclaw
from serial import Serial
import time
import serial.tools.list_ports

def find_motor_com_port(unique_identifier):
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in ports:
        if unique_identifier.lower() in hwid.lower():
            return port
    return None

def read_encoders(rc):
    encoder1 = rc.ReadEncM1(address)
    encoder2 = rc.ReadEncM2(address)
    print(f"Encoder M1: {encoder1}, Encoder M2: {encoder2}")
    return encoder1, encoder2

if __name__ == "__main__":
    motor_com_port = find_motor_com_port("roboclaw_controller")
    if motor_com_port:
        print(f"Motor COM port found: {motor_com_port}")
    else:
        print("Motor COM port not found.")
        exit()

    serial_obj = Serial(motor_com_port, 38400)  # default baudrate is 38400
    rc = Roboclaw(serial_obj)
    address = 0x80  # Default Roboclaw address

    rc.Open()
    rc.forward_backward_mixed(address, 64)  # stops both motors

    timing = 10
    power_rating = 32
    stop = 0

    # Simple loop to demonstrate encoder reading
    try:
        while True:
            rc.ForwardM1(address, power_rating)  # 1/4 power forward M1
            rc.BackwardM2(address, power_rating)  # 1/4 power backward M2
            time.sleep(timing)
            read_encoders(rc)

            rc.BackwardM1(address, power_rating)  # 1/4 power backward M1
            time.sleep(timing)
            read_encoders(rc)

            # Stopping motors
            rc.ForwardM1(address, stop)
            rc.BackwardM2(address, stop)
            time.sleep(timing)
            read_encoders(rc)

            # More movements can be added here along with encoder readings

    except KeyboardInterrupt:
        rc.ForwardM1(address, stop)  # Ensure motors are stopped on script exit
        rc.BackwardM2(address, stop)
        print("Stopped by user.")
