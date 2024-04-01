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
    # Create a VoltageInput object for voltage measurement
    voltageInput = VoltageInput()
    
    # Assuming another VoltageInput object or similar for the FSR pressure value
    fsrInput = VoltageInput()  

    # Set event handlers for voltage
    voltageInput.setOnVoltageChangeHandler(onVoltageChange)
    voltageInput.setOnAttachHandler(onAttach)
    voltageInput.setOnDetachHandler(onDetach)

    # Open the voltage device and wait for attachment
    voltageInput.openWaitForAttachment(5000)

    # Set the runtime duration in seconds
    runtime = 5
    start_time = time.time()  # Capture the start time

    # Max force represented by the voltage 
    max_force_voltage = 10
    # Max FSR pressure value threshold 
    max_fsr_pressure = 1000  

    # Poll the sensor and process the data within the runtime duration
    while time.time() - start_time < runtime:
        voltage = voltageInput.getVoltage()  
        fsrPressureValue = fsrInput.getVoltage()  # Placeholder for actual FSR reading logic

        if voltage > max_force_voltage:
            print(f"Force threshold of {max_force_voltage}V exceeded at {voltage}V.")
            break
        if fsrPressureValue > max_fsr_pressure:  # Check if FSR pressure exceeds threshold
            print(f"FSR pressure threshold of {max_fsr_pressure} exceeded at {fsrPressureValue}.")
            break
        
        time.sleep(0.1)  # Sampling delay

except PhidgetException as e:
    print(f"Phidget Exception {e.code} ({e.details}): {e.description}")
    exit(1)

finally:
    # Close the device
    voltageInput.close()
