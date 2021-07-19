#!/usr/bin/python3

## Bryton Herdes, 7.18.2021

import getpass
import sys
import telnetlib
import time
import sys
from datetime import datetime
startTime = datetime.now()

#change from a static host list to something more dynamic. Replace the two IP addresses in list with your OLT IP's/DNS names. 
HOST = ["100.64.1.1", "100.64.1.2" ]
user = b"admin"
password = b"zhone"

# Receive string in the form of 00:11:22:33:63:8c:d2
hex_serno = input ("Please enter the MAC Address of the Zhone ONT:\n")

#Need to convert into a hex serial number
hex_serno = hex_serno.replace(':','')
hex_serno = "3" + hex_serno[-6] + hex_serno[-5] + hex_serno[-4] + hex_serno[-3] + hex_serno[-2] + hex_serno[-1]
print(hex_serno)
dec_serno = int(hex_serno, 16)
print(dec_serno)
dec_serno = str(dec_serno)
dec_serno = dec_serno.encode()

#For each OLT IP in dictionary... 
for i in HOST:
	print ("Running script with host = " + i)

	tn = telnetlib.Telnet(i,23,timeout = 3)

	tn.read_until(b"login: ")
	time.sleep(1)
	tn.write(user + b"\n\r")
	time.sleep(1)

	if password:
		tn.read_until(b"password: ")
		tn.write(password + b"\r\n")

	#Sleep and run desired command
	time.sleep(3)
	tn.write(b"gpononu find serno " + (dec_serno) + b"\r\n")
	#Sleep and write exit to close Telnet

	#Sleep and get all output and print it out ASCII
	time.sleep(2)
	#tn_read = tn.read_all()
	tn_read = tn.read_until(b"profiles")

	temp = tn_read.decode('ascii')
	#print (temp)

	fail = "No"
	if fail in temp: 
		continue
	else:
		print ("Found " + hex_serno + " on host " + i + "\n")
		break	

#Filter out output besides specific ONU number details, in the format x/y/z
print(tn_read.decode('ascii') + "\n")
tn_read = tn_read.decode('ascii')

tn_read = tn_read[tn_read.find("/")-1] + "/" + tn_read[tn_read.find("/")+1] + tn_read[tn_read.find("/")+2] + tn_read[tn_read.find("/")+3] + tn_read[tn_read.find("/")+4] + tn_read[tn_read.find("/")+5]

print (tn_read)

#Run onu status x/y/z
tn_read = tn_read.encode()
tn.write(b"onu status " + (tn_read) + b"\r\n")
time.sleep(2)

tn.write(b"cpe show " + (tn_read) + b"\r\n")
time.sleep(4)

tn_read = tn_read.strip()
tn.write(b"bridge show 1/" + (tn_read) + b"/gpononu" + b"\r\n")
time.sleep(2)

#Exit telnet session
tn.write(b"exit\r\n")

#Read all output from onu status x/y/z command
tn_read = tn.read_all()
print (tn_read.decode('ascii'))
print (datetime.now() - startTime) 
