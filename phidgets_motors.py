import sys
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time

# Handler for voltage change events
def onVoltageChange(self, voltage):
    print(f"Voltage: {voltage}")

# Handler for attachment of the sensor
def onAttach(self):
    print("Voltage Input Attached")

# Handler for detachment of the sensor
def onDetach(self):
    print("Voltage Input Detached")

try:
    # Create a VoltageInput object
    voltageInput = VoltageInput()

    # Set event handlers
    voltageInput.setOnVoltageChangeHandler(onVoltageChange)
    voltageInput.setOnAttachHandler(onAttach)
    voltageInput.setOnDetachHandler(onDetach)

    # Open the device and wait for attachment
    voltageInput.openWaitForAttachment(5000)

    # Set the runtime duration in seconds
    runtime = 5
    start_time = time.time()  # Capture the start time

    # Max force represented by the voltage (this value might need adjustment based on your sensor calibration)
    max_force_voltage = 10

    # Poll the sensor and process the data within the runtime duration
    while time.time() - start_time < runtime:
        voltage = voltageInput.getVoltage()  # Get the voltage reading from the sensor
        if voltage > max_force_voltage:
            print(f"Force threshold of {max_force_voltage} exceeded at {voltage}V.")
            break
        time.sleep(0.1)  # Sampling delay

except PhidgetException as e:
    print(f"Phidget Exception {e.code} ({e.details}): {e.description}")
    exit(1)

finally:
    # Close the device
    voltageInput.close()
