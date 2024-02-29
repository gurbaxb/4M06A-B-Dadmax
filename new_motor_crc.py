from roboclaw import Roboclaw
import time
import PyCRC.CRC16 as CRC16

# Open serial port
address = 0x80  # Default address
roboclaw = Roboclaw("COM13", 9600)  # Use COM13 with baud rate of 9600
roboclaw.Open()

def calculate_crc(command):
    """
    Calculate the CRC for a given command using PyCRC.
    """
    return CRC16.CRC16().calculate(command)

def send_command_with_crc(command):
    """
    Append CRC to command and send it to the Roboclaw.
    Note: This function is for demonstration and might not directly apply to the roboclaw module.
    """
    crc = calculate_crc(command)
    full_command = command + crc.to_bytes(2, 'little')
    roboclaw._port.write(full_command)  # Assuming roboclaw has a '_port' attribute for direct access

# Example usage
def ramp_motor_speed(motor, max_speed, ramp_duration):
    # This function remains unchanged as it uses high-level roboclaw module functions
    # For direct command sending, you would replace these with send_command_with_crc or similar

    try:
        # Ramp up motor 1 speed slowly to 50 over 10 seconds
        ramp_motor_speed(1, 50, 10)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the serial port
        roboclaw.Close()
