#Author Puneet Mathur
#Free to distribute with this header
# https://www.pmauthor.com/raspbian/



#Initializing python libraries
from gpiozero import CPUTemperature
import time
from datetime import datetime
import pandas as pd
import psutil
import platform
from gpiozero import LED
import time

#Initializing Audio for RED status play
import pygame
pygame.mixer.init()
pygame.mixer.music.load("example.mp3")


#intializing LED at pin numberf 18
redled= LED(18)
greenled= LED(22)    
yellowled= LED(17)    

#Initializing Light Sensitive Module
from gpiozero import LightSensor
ldr = LightSensor(25)


tempstatus=""

#Columns for pandas dataframe
columns=['date','time','temperature','tempstatus','cpupercent','diskpercent','memorypercent']
#Creating a pandas dataframe to store values from Raspberry Pi hardware
df=pd.DataFrame(columns=columns)
df['date']=datetime.date(datetime.now())
df['time']=datetime.time(datetime.now())
df['temperature']=0
df['tempstatus']=""
df["ldrval"]=0
cpu = CPUTemperature()
counter=0
while True:
	#print(cpu.temperature)
	time.sleep(1)
	tem=cpu.temperature
	if(tem>60):
		print("RED ALERT CPU EXCEEDING HIGH TEMPERATURE")
		tempstatus="RED"
                redled.on()
		greenled.off()
		yellowled.off()
 		pygame.mixer.music.play()
               
	elif(tem>55 and tem<60):
		print("YELLOW ALERT CPU NEARING HIGH TEMPERATURE THRESHOLD")
		tempstatus="ORANGE"
		redled.off()
		greenled.off()
		yellowled.on()

	else:
		print("TEMPERATURE IS NORMAL")
		tempstatus="GREEN"
		#time.sleep(1)
		greenled.on()
                redled.off()
		yellowled.off()
	df['date'].loc[counter]=datetime.date(datetime.now())
	print(datetime.date(datetime.now()))
	df['time'].loc[counter]=datetime.time(datetime.now())
	df['temperature'].loc[counter]=tem
	df['tempstatus'].loc[counter]=tempstatus
	#print(df['date'].values)
	#print(df['time'].values)
	#print(df['temperature'].values)
	#print(df['tempstatus'].values)
        #Now write data in database sqlite3 temperature.db
        #print("Connected to MACHINEMON Database")
        import sqlite3
        conn = sqlite3.connect('machinemon.db')
        #df.to_sql(name='tempdata', con=conn)
        curr=conn.cursor()
        #get machine data

        os, name, version, _, _, _ = platform.uname()
        version = version.split('-')[0]
        cores = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory()[2]
        disk_percent = psutil.disk_usage('/')[3]
	#Getting Light Sensor Data to determine day or night values 0 means Day and 1 means Night 
	#print(ldr.value)
        ldrval=ldr.value
	#boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        #running_since = boot_time.strftime("%A %d. %B %Y")
        #query="INSERT INTO TEMPERATURE VALUES(" +"'" + str(datetime.date(datetime.now())) + "'" +"," + "'" + str(datetime.time(datetime.now())) + "'"+ "," + "'" + str(tem) +  "'" + "," + "'" + tempstatus +"'" + ")"   
        query="INSERT INTO machinedata(date,time,temperature,tempstatus,cpupercent,diskpercent,memorypercent,ldrval) VALUES(" +"'" + str(datetime.date(datetime.now())) + "'" +"," + "'" + str(datetime.time(datetime.now())) + "'"+ "," + "'" + str(tem) +  "'" + "," + "'" + tempstatus + "'" + "," + "'" + str(cpu_percent) + "'" + "," + "'" + str(disk_percent) + "'" + "," + "'" + str(memory_percent) + "'" "," + "'" + str(ldrval) + "'" + ")"   
        print(query)
        curr.execute(query)
        conn.commit()
        #Increment counter to parse to next record number in the dataframee
        counter=counter+1
