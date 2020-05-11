#Author Puneet Mathur
#Free to distribute with this header
# https://www.pmauthor.com/raspbian/

#!/usr/bin/python
#Loading modbus library
import minimalmodbus
from datetime import datetime

#Initializing searial communication on the modbus library
sdm630 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
sdm630.serial.baudrate = 9600
sdm630.serial.bytesize = 8
sdm630.serial.parity = minimalmodbus.serial.PARITY_NONE
sdm630.serial.stopbits = 1
sdm630.serial.timeout = 1
sdm630.debug = False
sdm630.mode = minimalmodbus.MODE_RTU
print(sdm630)

while 1:
	Volts = sdm630.read_float(0, functioncode=4)
	Current = sdm630.read_float(6, functioncode=4)
	Active_Power = sdm630.read_float(12, functioncode=4)
	Apparent_Power = sdm630.read_float(18, functioncode=4)
	Reactive_Power = sdm630.read_float(24, functioncode=4)
	Power_Factor = sdm630.read_float(30, functioncode=4)
	Phase_Angle = sdm630.read_float(36, functioncode=4)
	Frequency = sdm630.read_float(70, functioncode=4)
	Import_Active_Energy = sdm630.read_float(72, functioncode=4) 
	Export_Active_Energy = sdm630.read_float(74, functioncode=4)
	Import_Reactive_Energy = sdm630.read_float(76, functioncode=4)
	Export_Reactive_Energy = sdm630.read_float(78, functioncode=4)
	Total_Active_Energy = sdm630.read_float(342, functioncode=4)
	Total_Reactive_Energy = sdm630.read_float(344, functioncode=4)

	print('Voltage: {0:.1f} Volts'.format(Volts))
	print('Current: {0:.1f} Amps'.format(Current))
	print('Active power: {0:.1f} Watts'.format(Active_Power))
	print('Apparent power: {0:.1f} VoltAmps'.format(Apparent_Power))
	print('Reactive power: {0:.1f} VAr'.format(Reactive_Power))
	print('Power factor: {0:.1f}'.format(Power_Factor))
	print('Phase angle: {0:.1f} Degree'.format(Phase_Angle))
	print('Frequency: {0:.1f} Hz'.format(Frequency))
	print('Import active energy: {0:.3f} Kwh'.format(Import_Active_Energy))
	print('Export active energy: {0:.3f} kwh'.format(Export_Active_Energy))
	print('Import reactive energy: {0:.3f} kvarh'.format(Import_Reactive_Energy))
	print('Export reactive energy: {0:.3f} kvarh'.format(Export_Reactive_Energy))
	print('Total active energy: {0:.3f} kwh'.format(Total_Active_Energy))
	print('Total reactive energy: {0:.3f} kvarh'.format(Total_Reactive_Energy))
	print('Current Yield (V*A): {0:.1f} Watt'.format(Volts * Current))
	import sqlite3
        conn = sqlite3.connect('/home/pi/IoTBook/Chapter6/energymeter.db')
        #df.to_sql(name='tempdata', con=conn)
        curr=conn.cursor()
	query="INSERT INTO sdm630data(timestamp, voltage , current ,activepow ,apparentpow ,reactivepow ,powerfactor ,phaseangle , frequency , impactiveng , expactiveeng ,impreactiveeng , expreactiveeng ,totalactiveeng ,totalreactiveeng ,currentyield, device ) VALUES(" + "'" + str(datetime.now()) + "'" + "," + "'" + str(Volts) + "'" + "," +  "'" + str(Current) + "'" + "," +  "'" + str(Active_Power) + "'" + "," +  "'"  + str(Apparent_Power) + "'" + "," +  "'" + str(Reactive_Power) +  "'" + "," +  "'" + str(Power_Factor) + "'" + "," +  "'" +  str(Phase_Angle) + "'" + "," +  "'" + str(Frequency) + "'" + "," +  "'" +  str(Import_Active_Energy) + "'" + "," +  "'" + str(Export_Active_Energy) + "'" + "," +  "'" + str(Import_Reactive_Energy) + "'" + "," +  "'" + str(Export_Reactive_Energy) + "'" + "," +  "'" + str(Total_Active_Energy) + "'" + "," +  "'" + str(Total_Reactive_Energy) + "'" + "," +  "'" + str((Volts * Current)) + "'" + "," + "'" + str("millmachine")+ "'" + ")"   
        print(query)
        curr.execute(query)
        conn.commit()
