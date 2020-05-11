#Author Puneet Mathur
#Free to distribute with this header
# https://www.pmauthor.com/raspbian/

#Light Dependant Resistor Module Initialization
from gpiozero import LightSensor

#importing Sqlite3 python library to connect with database
import sqlite3

from datetime import datetime

#GPIO LDR Signal Pin initialization
ldr = LightSensor(25)

#Read value infinitely in a loop
while True:
	print(ldr.value)
	ldval=float(ldr.value)
	if(ldval>0.0):
		print("It is Night time now")
	else:
		print("It is Day time")
	
	conn = sqlite3.connect('iotsensor.db')
	curr=conn.cursor()
	query="INSERT INTO ldrvalues(date,time,ldrvalue) VALUES(" +"'" + str(datetime.date(datetime.now())) + "'" +"," + "'" + 		str(datetime.time(datetime.now())) + "'" + "," + "'" + str(ldval) + "'" + ")"   
	print(query)
	curr.execute(query)
	conn.commit()
