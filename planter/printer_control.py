"""API for controlling 3D printer with Marlin firmware.

Commands are sent to the printer using G-code and Serial.
Full list of Marlin GCode commands can be found here:
https://marlinfw.org/meta/gcode/ 

Attributes:
    baud: (int) baud rate
    addr: (str) USB address
    ser: serial interface.  set using connect.
"""
import serial
import time
import binascii

from point import Point


class Printer(object):
  def __init__(self,addr="ACM0",baud=115200, timeout=1,print_output=False):
    self.addr = addr
    self.baud = baud
    self.timeout = timeout
    self.print_output = print_output
    
    self.ser = None
    self.connect()
    self.pos = None


  def connect(self,):
    """Opens serial comm to printer."""
    if self.ser is not None:
      print("""Serial connection already open.  
                 Please close the current connection and try again.""")
      return
    self.ser = serial.Serial(self.addr,
                             baudrate=self.baud,
                             timeout=self.timeout)
    self.ser.write("\r\n\r\n".encode())
    self.sleep(2)
    input_message = self.ser.read(self.ser.in_waiting)
    print(input_message.decode('ascii'))

    self.ser.flushInput()
    print(f"Device name: {self.ser.name}")


  def sleep(self,amount):
    """Sleeps for amount seconds."""
    time.sleep(amount)


  def disconnect(self):
    """Closes serial comm from printer."""
    self.ser.close()
    self.ser = None


  def command(self,mess):
    """Writes a message over serial to the printer.

    Waits for the command to finish."""
    self.ser.reset_input_buffer()

    mess += " \n" # marlin commands must end with newline character
    self.ser.write(mess.encode())
    self.ser.flush()

    # wait for ok message from machine
    rec_mess = ''
    while rec_mess != 'ok\n':
      rec_mess = self.ser.readline().decode('ascii')
      if self.print_output:
        print(rec_mess)

  def pred_time_move(self,x,y,z):
    """Give an estimate for the amount of time to move.


    Data was collected manually and parameters 
    were fit to assume a linear model in each dimension.
    Since the axes move at the same time, the slowest move 
    is returned.    
    """
    return max([x*.04,y*.04,z*.21])

  def move(self,x=None,y=None,z=None):
    """Moves to an X,Y,Z location"""
    mess = "G00"
  
    if x is not None:
      mess += f" X{x}"

    if y is not None:
      mess += f" Y{y}"

    if z is not None:
      mess += f" Z{z}"

    print(mess)

    self.command(mess)

    # we don't know when the printer is done with this command,
    # so we have to guess.  
    t_ = self.pred_time_move(x,y,z)
    print(f"Pred: {t_}")
    self.sleep(2*t_)


  def home(self):
    """Returns the arm to the home location."""
    self.command("G28")

    self.pos = Point(x=0,y=0,z=0)


  def list_sd_card(self):
    prev_state = self.print_output
    self.print_output = True

    self.ser.reset_input_buffer()
    self.command("M20")
    self.print_output = prev_state


