import pyfirmata
from pyfirmata import Arduino, util
import time

port = 'COM14'
board = pyfirmata.Arduino(port)

it = pyfirmata.util.Iterator(board)
it.start()

anal = board.get_pin('a:0:i')

# Set the runtime duration in seconds
runtime = 5
start_time = time.time()  # Capture the start time
# Max force
max_force = 10

while True:
    analV = anal.read()
    if analV is not None:
        print(analV)

    # Check if the current time exceeds the start time by the runtime duration or force exceeds 0.1
    if (time.time() - start_time > runtime) or (analV is not None and analV > max_force):
        if analV > max_force:
            print(f"Force threshold of {max_force} exceeded.")
        else:
            print(f"Ending after {runtime} seconds.")
        break

    time.sleep(0.1)  # Delay for a bit before reading again

board.exit()
