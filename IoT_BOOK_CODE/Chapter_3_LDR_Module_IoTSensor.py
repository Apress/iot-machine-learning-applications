#Author Puneet Mathur
#Free to distribute with this header
# https://www.pmauthor.com/raspbian/

#Turn on Light Sensor
from gpiozero import LightSensor
ldr = LightSensor(25)
while True:
	print(ldr.value)
	ldval=float(ldr.value)
	#print(ldval)
	#print("done deal")
	if(ldval>0.0):
		print("It is Night time now")
	else:
		print("It is Day time")