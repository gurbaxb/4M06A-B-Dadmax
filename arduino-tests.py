import pyfirmata
import time

port = 'COM14'
board = pyfirmata.Arduino(port)

it = pyfirmata.util.Iterator(board)
it.start()

anal = board.get_pin('a:0:i')
#inputPin = board.get_pin('d:3:o')

max_iter = 100  
inter_count = 0  

while True:
    #inputPin.write(True)
    analV = anal.read()
    print(analV)
    time.sleep(0.1)
    
    inter_count += 1  
    if inter_count >= max_iter:
        print(f"Ending after max interation: {max_iter}")
        break  

board.exit() 
