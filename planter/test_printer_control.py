"""Script for testing the printer controls."""
from printer_control import Printer
import time

p = Printer("/dev/ttyUSB0",print_output=True)
print("Testing home.\n")
p.home()

# print("Testing sd card read.\n")
# p.list_sd_card()

print("Testing coordinate move.\n")
time.sleep(2)
p.move(x=20,y=20,z=30)

time.sleep(0)

print("Disconnecting printer.")
p.disconnect()
