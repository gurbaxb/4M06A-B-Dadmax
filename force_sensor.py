from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time

def onVoltageChange(self, voltage):
    # Placeholder for conversion logic
    # For now, just print the voltage, as the conversion requires calibration
    print(f"Sensor Voltage: {voltage:.2f}V")

def main():
    # Create a VoltageInput object
    voltageInput = VoltageInput()

    # Set up event handler for voltage changes
    voltageInput.setOnVoltageChangeHandler(onVoltageChange)

    # Open and wait for the attachment of the device
    voltageInput.openWaitForAttachment(5000)

    try:
        # Keep the program running to continuously monitor voltage changes
        print("Reading sensor data. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Gracefully exit the program
        print("Exiting...")
    finally:
        # Close the device
        voltageInput.close()

if __name__ == "__main__":
    main()
