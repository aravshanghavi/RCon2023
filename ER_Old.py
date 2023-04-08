import RPi.GPIO as GPIO
from time import sleep
import socket
import serial
import math

		
if __name__=='__main__':
	global vel
	global wheel_angles
	
	vel = [0, 0, 0, 0]
	wheel_angles=[45, 135, 225, 315]
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	line=' 0 ; 0 ; 0 '
	ser.flush()
	HOST = '192.168.124.145'
	PORT = 10000
	
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((HOST, PORT))

	
	while True:
		new_message = ""
		ser.flush()
		if (ser.in_waiting > 0):
			line = ser.readline().decode('utf-8', 'ignore').rstrip()
		if line.find(';')==-1:
			line=' 0 ; 0 ; 0 '
		coordinates = line.split(';')
		if coordinates[0]=='':
			coordinates[0]='0'
		if coordinates[1]=='':
			coordinates[1]='0'
		if coordinates[0].find('-')>0:
			coordinates[0]=(coordinates[0])[0:coordinates[0].find('-')]
		if coordinates[1].find('-')>0:
			coordinates[1]=(coordinates[1])[0:coordinates[1].find('-')]
		x = float(coordinates[0])
		y = float(coordinates[1])
		y=y*float(-1)
		
		
		ang = find_angle(x, y)
		
		speedd = float(math.sqrt((x**2)+(y**2)))
		vel_x = speedd*math.cos(ang*math.pi/float(180))
		vel_y = speedd*math.sin(ang*math.pi/float(180))
		
		for i in range(4):
			vel[i]=vel_x*math.cos(wheel_angles[i]) + vel_y*math.sin(wheel_angles[i])
			new_message = new_message+str(vel[i])+"; "
		client.send(new_message.encode('utf-8'))
		new_message=""

