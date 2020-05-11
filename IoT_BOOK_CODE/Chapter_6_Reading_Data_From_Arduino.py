#Author Puneet Mathur
#Free to distribute with this header
# https://www.pmauthor.com/raspbian/


import serial
ser= serial.Serial('/dev/ttyACM0', 9600)
while 1:
    print("Reading...")
    print(ser.readline())
