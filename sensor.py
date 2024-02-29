import pyfirmata
from pyfirmata import Arduino, util
import time

port = 'COM14'
board = pyfirmata.Arduino(port)

it = pyfirmata.util.Iterator(board)
it.start()

anal = board.get_pin('a:0:i')

# Set the runtime duration in seconds
runtime = 15
start_time = time.time()

# Set max force threshold correctly
max_force = 0.1

# Initialize scaled_force outside the while loop
scaled_force = 0

while True:
    analV = anal.read()
    if analV is not None:
        # For 10-bit ADC, scale by 1023 - TBD later
        scaled_force = analV
        # real_force = scaled_force
        print(scaled_force)

    # Check if the force exceeds max or 5 seconds have passed
    if (time.time() - start_time > runtime) or (scaled_force > max_force):
        if scaled_force > max_force:
            print(f"Force threshold of {max_force} exceeded. Output is {scaled_force}")
        else:
            print(f"Ending after {runtime} seconds.")
        break

    # Delay for a shorter period to allow more frequent readings
    time.sleep(0.1)

board.exit()
