#Author Puneet Mathur
#Free to distribute with this header
# https://www.pmauthor.com/raspbian/

**THIS IS A PYTHON VERSION 3.6 COMPATIBLE CODE
import tkinter as tk
import tkinter.font
from gpiozero import LED
import smtplib

win= tk.Tk()
win.title("LED Monitoring Agent Application")
myfont= tkinter.font.Font(family= 'Helvetica', size=30, weight='bold')
redled=LED(18)
yellowled=LED(22)
greenled=LED(17)


def ledstatus():
    while(1):
        if(redled.value==1):
            print("RED ON")
	   sender = 'newsletter@machinelearningcasestudies.com'
	    receivers = ['newsletter@machinelearningcasestudies.com']

	    message = """From: From Person 	        
             <mmagent@machinemon.py>
	    To: To Person <administrator@machinemon.py>
	     Subject: SMTP e-mail CRITICAL ALERT

	     This is a Critical Message alert the CPU Temperature of Raspberry 	      Pi has crossed Threshold value.
	     """

		try:
   			smtpObj = 						 						smtplib.SMTP('mail.machinelearningcasestudies.com')
   			smtpObj.sendmail(sender, receivers, message)         
   			print("Successfully sent email")
		except smtplib.SMTPException:
   			print("Error: unable to send email")
        			if(yellowled.value==1):
            		print("YELLOW ON")
        			if(greenled.value==1):
            		print("GREEN ON")


def exitprog():
	win.quit()

#command=ledstatus
statusButton= tk.Button(win, text='',command=ledstatus,font=myfont ,bg='green', height=1, width=24)
statusButton.grid(row=0,sticky=tk.NSEW)
exitButton= tk.Button(win, text='EXIT', font=myfont , command=exitprog,bg='green', height=1, width=24) 
exitButton.grid(row=30,sticky=tk.NSEW)

tk.mainloop()
