from Phidget22.Devices.Stepper import Stepper
from Phidget22.Devices.BLDCMotor import BLDCMotor
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import *
from pynput.keyboard import Key, Listener
from roboclaw import Roboclaw
import serial
from serial.tools import list_ports
import time

def find_roboclaw():
    ports = list_ports.comports()
    for port in ports:
        try:
            serial_obj = serial.Serial(port.device, 38400, timeout=1)
            rc = Roboclaw(serial_obj)
            rc.Open()
            version = rc.ReadVersion(0x80)
            if version[0]:
                print(f"Roboclaw found at {port.device}")
                return rc, serial_obj
            else:
                serial_obj.close()
        except (serial.SerialException, OSError) as e:
            print(f"Error opening port {port.device}: {e}")
    raise IOError("Roboclaw not found")

# Initialize Phidget devices
stepper0 = Stepper()
elbowMotor = BLDCMotor()
shoulderMotor = BLDCMotor()

# Try to find and connect to Roboclaw
try:
    rc, serial_obj = find_roboclaw()
except IOError as e:
    print(e)
    exit()

def control_stepper(key):
    try:
        if key == 'w':  # Move stepper up
            stepper0.setTargetPosition(stepper0.getTargetPosition() + 10000)
        elif key == 's':  # Move stepper down
            stepper0.setTargetPosition(stepper0.getTargetPosition() - 10000)
    except Exception as e:
        print(f"Stepper control error: {e}")

def control_bldc(motor, velocity):
    try:
        motor.setTargetVelocity(velocity)
    except Exception as e:
        print(f"BLDC control error: {e}")

def control_claw(action):
    if action == 'open':
        rc.ForwardM1(0x80, 64)  # Adjust address and speed as needed
    elif action == 'close':
        rc.BackwardM1(0x80, 64)  # Adjust address and speed as needed
    else:
        rc.ForwardBackwardM1(0x80, 64)  # Stop the claw

def on_press(key):
    try:
        if key.char == 'w' or key.char == 's':
            control_stepper(key.char)
        elif key.char == 'd':
            control_bldc(shoulderMotor, 1)  # Positive velocity for one direction
        elif key.char == 'a':
            control_bldc(elbowMotor, -1)  # Negative velocity for the opposite direction
        elif key.char == 'f':
            control_claw('close')  # Activate the claw
    except AttributeError:
        pass

def on_release(key):
    if key == Key.enter:
        # Reset everything to original position and stop script
        stepper0.setEngaged(False)
        control_bldc(elbowMotor, 0)
        control_bldc(shoulderMotor, 0)
        control_claw('stop')
        serial_obj.close()
        return False  # Stop listener

def main():
    global stepper0, elbowMotor, shoulderMotor

    try:
        # Stepper motor setup
        stepper0.openWaitForAttachment(5000)
        stepper0.setEngaged(True)

        # BLDC motor setup
        elbowMotor.setDeviceSerialNumber(708023)
        shoulderMotor.setDeviceSerialNumber(708023)
        elbowMotor.setHubPort(3)
        shoulderMotor.setHubPort(4)
        elbowMotor.openWaitForAttachment(5000)
        shoulderMotor.openWaitForAttachment(5000)

        # Listen for keyboard input
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    except PhidgetException as e:
        print(f"Phidget Exception: {e.description}")
    finally:
        # Cleanup
        stepper0.close()
        elbowMotor.close()
        shoulderMotor.close()
        serial_obj.close()

if __name__ == "__main__":
    main()