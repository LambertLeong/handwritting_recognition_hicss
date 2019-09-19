'''
This code records the output printed to the screen by the arduino hardware code

by Lambert Leong
'''
################################################################
## Script listens to serial port and writes contents into a file
################################################################
### requires pySerial to be installed 
################################################################

import serial  # sudo pip install pyserial should work
import os
import argparse
from argparse import RawTextHelpFormatter

serial_port = "/dev/ttyUSB0"
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)

def parse_arguments():
	parser = argparse.ArgumentParser(epilog="""""",formatter_class=RawTextHelpFormatter)
	parser.add_argument('-n', '--num',  action='store', type=int, dest='num', metavar='<digit to record>', required=True, help='number/digit recording')
	return parser.parse_args()

if __name__ == '__main__':
	argv = parse_arguments()
	to_dir = "data/"
	out_dir = ""
	if argv.num == 0:
		out_dir = to_dir+str(argv.num)+"/"
	else:
		out_dir = to_dir+str(argv.num)+"/"
	print"\n\n File writting to "+ out_dir+"\n\n"	
	num_files = len([f for f in os.walk(out_dir).next()[2] if f[-4:] == ".csv"])
	count = num_files+1
	exit = 0
	listen = 0
	ser = serial.Serial(serial_port, baud_rate)
	while exit < 1:
		print "Ready to record!!!"
		out_line = ""
		line = ser.readline()
		line = line.decode("utf-8") #ser.readline returns a binary, convert to string
		if "START" in line:	
			listen = 1	
			print "Start writing digit "+str(argv.num)
		while listen > 0:
			line = ser.readline()
			line = line.decode("utf-8") #ser.readline returns a binary, convert to string
			if "STOP" in line:
				listen = 0
				print "writing file "+out_dir+str(count)
				print "\n"+out_line[-40:]+"\n"
				file = open(out_dir+str(count)+"l.csv",'w+')
				file.write(out_line)
				file.close()
				count+=1
			out_line+=line
