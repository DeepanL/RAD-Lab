# enums are used to assign labels to a set of values
#allowing name based referencing of underlying value 
from enum import Enum
from array import array

import struct
import serial
import time
import sys
  

class HeaderCommand(Enum):
      SET_MOTOR_RPS = 0    # Header set motor1 rps

      REQ_ENCODER_DATA = 1  # Header request for encoder1 data

      REQ_WINDSPEED = 2     # Header request for wind sensor

class HeaderResponse(Enum):
      RPS = 0               # encoder data
      SPEED = 1             # Wind sensor data

def set_motor_rps( hardware, motor_no, speed_rps):
    set_packet = [
        HeaderCommand.SET_MOTOR_RPS.value, #header
        2,                                 #Payload length 1 + 4 
        motor_no,                          #Motor no.
        speed_rps,                          #Payload containing speed (4bytes)
        ]
    # send the packet [ 0, 5, 1/2, speed ] to arduino
    hardware.write(set_packet)
    print(set_packet)

encoder_data = []        
def get_sensors_value(serial):
    # wait for packet response from arduino which will send encoder data every 25 ms
    
    while serial.in_waiting < MIN_PACKET_SIZE:
       pass

    header = ord(serial.read())
##    header = HeaderResponse(header)
##    print(header)
    e_packet = []
##    packet_recv = []
##    e_packet.append(HeaderResponse(header)) #convert header byte to enum type
    e_packet.append(header)
##    print(e_packet)
##    if e_packet[0] == HeaderResponse.RPS.value:
    if e_packet[0] == 0:    
        length = ord(serial.read())      # get length of payload
        e_packet.append(length)
##        print(e_packet)
        assert (length == 5)             # this packet payload length should = 5 bytes changed from assert to if 
        encoder_no = ord(serial.read())  # get encoder number
        e_packet.append(encoder_no)
##        print(e_packet)
        # wait for payload of encoder data
        while serial.in_waiting < 4:
            pass
        # read in payload
        for i in range (0,4):
            e_packet.append(ord(serial.read()))
        print(e_packet, end = "\n")
        ticks = struct.unpack_from('f', array('B', e_packet[3:7]))[0]
        print("encoder{} raw data".format(encoder_no))
        print(round(ticks,1))
    if e_packet[0] == 1:
       length = ord(serial.read())
       e_packet.append(length)
##       print(e_packet)
       assert(length == 8) # this packet should have 4 byte payload since
       
       while serial.in_waiting < length:
              pass

       for i in range( 0,8):
             e_packet.append(ord(serial.read()))       
       speed = struct.unpack_from('f', array('B', e_packet[2:6]))[0]
       direction = struct.unpack_from('f' , array('B', e_packet[6:10]))[0]
       print("Wind Sensor.raw data: speed{} and direction {} ".format(round(speed,1), round(direction,1)), end = "\n")
    return


MIN_PACKET_SIZE = 2
i = 0
packet_recv = []
time_data = []
motor_rps = 0

hardware = serial.Serial('/dev/ttyS0',115200)

##motor_rps = input("enter motor 1 rps set point")
##set_motor_rps(hardware, 1, int(motor_rps))
##motor2_rps = input("enter motor 2 rps set point")    
##set_motor_rps(hardware, 2, int(motor2_rps))
prev_time = 0
while True:
##    motor_rps = input("enter motor 1 rps set point")
##    set_motor_rps(hardware, 1, int(motor_rps))
##    motor2_rps = input("enter motor 2 rps set point")    
##    set_motor_rps(hardware, 2, int(motor2_rps))
##    time.sleep(5)
        now_time = time.time()
        if now_time - prev_time >= 20:
          motor_rps = input("enter motor 1 rps set point")
          set_motor_rps(hardware, 1, int(motor_rps))
          motor2_rps = input("enter motor 2 rps set point")    
          set_motor_rps(hardware, 2, int(motor2_rps))
          prev_time = now_time
          
        get_sensors_value(hardware)
##          time.sleep(5)
   
