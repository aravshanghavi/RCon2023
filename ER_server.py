import socket
import RPi.GPIO as GPIO
HOST = '192.168.166.145'
PORT = 10000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(1)
comm_socket, client_add = server.accept()
print(f"Connected to:  {client_add}")

if __name__=='__main__':
	vel=[float(0), float(0), float(0)]
	GPIO.setmode(GPIO.BOARD)
	direcs = [True, False, True]
	dirs = [11, 13, 15]
	pwms = [16, 18, 22]
	myPWM =[]
	
	for i in range(3):
		GPIO.setup(dirs[i], GPIO.OUT)
		GPIO.setup(pwms[i], GPIO.OUT)
		myPWM.append(GPIO.PWM(pwms[i], 10000))
		
	while True:
		index1=float(-1)
		index2=float(-1)
		message = comm_socket.recv(8192).decode('utf-8', 'ignore')
		for i in range(len(message)):
			if(index1==-1):
				if(message[i]=='['):
					index1=int(i)
			if(index1!=float(-1) and index2==float(-1) and i!=index1):
				if(message[i]==']'):
					index2=int(i)
					break
		if(index1==-1 or index2==-1):
			continue
		
		message=message[index1+1:index2]
		string_vels=message.split(',')
		vel1=int(string_vels[0])
		vel2=int(string_vels[1])
		vel3=int(string_vels[2])
		
		if(vel1<0):
			vel1=vel1*int(-1)
			GPIO.output(dirs[0], GPIO.LOW)
			myPWM[0].start(vel1)
		
		elif(vel1>0):
			GPIO.output(dirs[0], GPIO.HIGH)
			myPWM[0].start(vel1)
		
		else:
			myPWM[0].start(0)
			
		if(vel2<0):
			vel2=vel2*int(-1)
			GPIO.output(dirs[1], GPIO.LOW)
			myPWM[1].start(vel2)
		
		elif(vel2>0):
			GPIO.output(dirs[1], GPIO.HIGH)
			myPWM[1].start(vel2)
		
		else:
			myPWM[1].start(0)
			
		if(vel3<0):
			vel3=vel3*int(-1)
			GPIO.output(dirs[2], GPIO.LOW)
			myPWM[2].start(vel3)
		
		elif(vel3>0):
			GPIO.output(dirs[2], GPIO.HIGH)
			myPWM[2].start(vel3)
			
		else:
			myPWM[2].start(0)

		
		
		
		
    



