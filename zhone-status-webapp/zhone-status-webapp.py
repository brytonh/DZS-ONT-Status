#!/usr/bin/python3

# Bryton Herdes, 7.18.2021

import getpass
import sys
import telnetlib
import time
import sys
from datetime import datetime
startTime = datetime.now()
from flask import Flask, render_template, request, Markup

app = Flask(__name__)

@app.route('/')
def app_run():
	return render_template('form.html')

@app.route('/', methods=['POST'])
def form_post():
	text = request.form['text']
	processed_text = text.upper()

	# Replace the values within the HOST list with your IP addresses of the OLTs
	HOST = ["100.64.1.1", "100.64.1.2" ]
	user = b"admin"
	password = b"zhone"

	# Receive string in the form of 00:11:22:33:63:8c:d2
	hex_serno = processed_text

	#Need to convert into a hex serial number like 3638cd2
	hex_serno = hex_serno.replace(':','')
	hex_serno = "3" + hex_serno[-6] + hex_serno[-5] + hex_serno[-4] + hex_serno[-3] + hex_serno[-2] + hex_serno[-1]
	print(hex_serno)
	output1 = hex_serno + "\n\n\n"
	dec_serno = int(hex_serno, 16)
	print(dec_serno)
	temp = str(dec_serno)
	output2 = temp + "\n\n\n"
	dec_serno = str(dec_serno)
	dec_serno = dec_serno.encode()

	#For each OLT IP in list... 
	for i in HOST:
		print ("Running script with host = " + i)
		output3 = "Running script with host = " + i + "\n"
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

		#Sleep and get all output and print it out ASCII
		time.sleep(2)
		tn_read = tn.read_until(b"profiles")

		temp = tn_read.decode('ascii')

		trigger = 1
		fail = "No"
		if fail in temp: 
			continue
		else:
			print ("Found " + hex_serno + " on host " + i + "\n")
			output4 = "Found " + hex_serno + " on host " + i + "\n\n\n"
			trigger = 0
			break

	if trigger == 1:
		print ("Did not find the following ONT on any OLT -  ", processed_text)
		output_total = "Did not find the following ont on any OLT -  " + processed_text
		return render_template('results.html', output_total=output_total)

	#Filter out output besides specific ONU number details, in the format x/y/z
	print(tn_read.decode('ascii') + "\n")
	output5 = tn_read.decode('ascii') + "\n\n\n"
	a,output5 = output5.split('Interface',1)
	tn_read = tn_read.decode('ascii')

	tn_read = tn_read[tn_read.find("/")-1] + "/" + tn_read[tn_read.find("/")+1] + tn_read[tn_read.find("/")+2] + tn_read[tn_read.find("/")+3] + tn_read[tn_read.find("/")+4] + tn_read[tn_read.find("/")+5]

	print (tn_read)
	output6 = tn_read + "\n\n\n"

	#Run onu status x/y/z
	tn_read = tn_read.encode()
	tn.write(b"onu status " + (tn_read) + b"\r\n")
	time.sleep(2)

	tn.write(b"cpe show " + (tn_read) + b"\r\n")
	time.sleep(4)

	tn_read = tn_read.strip()
	tn.write(b"bridge show 1/" + (tn_read) + b"/gpononu" + b"\r\n")
	time.sleep(2)

	tn.write(b"exit\r\n")

	#Read all output from onu status x/y/z command
	tn_read = tn.read_all()
	print (tn_read.decode('ascii'))
	print (datetime.now() - startTime)
	output7 = tn_read.decode('ascii') + "\n\n\n"
	output_total = output1 + output2 + output3 + output3 + output4 + output5 + output6 + output7

	output_total = output_total.splitlines()
	return render_template('results_template.html', output_total=output_total)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")
