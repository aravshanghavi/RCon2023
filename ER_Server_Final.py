import RPi.GPIO as GPIO
from time import sleep
import socket
import serial
import math

if __name__=='__main__':
	
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.flush()
	HOST = '192.168.154.102'
	PORT = 10000
	c=0
  wheel_angles = [120, 240, 90]
  velocities = []
  speedd = 50
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((HOST, PORT))
  overall_message = []
  prev_button_value="1111111111111"
  leadscrew = "NULL"
  single_leadscrew="NULL"
  while True:
    c = c+1
    ser.flush()

    if(ser.in_waiting>0):
        values = ser.readLine().decode('utf-8', 'ignore')

    message = values.split(";")
    buttons = message[0]
    joystick_ang = -800
    
    leadscrew="NULL"
    single_leadscrew="NULL"
    positive_ang = 0
    negative_ang = 0
    c_positive = 0
    c_negative = 0
    desired_ang = 0
    servo = "NULL"
    only_one_hit = "NULL"
    multiple_hits = "NULL"
    flybelt_duty = 0
    rotate = "NO"
    
    try:
        joystick_ang = int(message[1])
    except ValueError:
        continue
    except:
        continue
        
    if(len(buttons)!=13):
		continue
    
    vx = speedd*math.cos(joystick_ang*(math.pi/180))
    vy = speedd*math.sin(joystick_ang*(math.pi/180))
    for i in range(3):
        velocities[0] = vx*math.cos(wheel_angles[i]*(math.pi/180)) + vy*math.sin(wheel_angles[i]*(math.pi/180))

    if(buttons.find("01")==0):
        leadscrew="UP"
    elif(buttons.find("01")==1):
        leadscrew="DOWN"
    else:
        leadscrew="NULL"

    if(buttons.find("01")==2):
        single_leadscrew = "LEFT"
    elif(buttons.find("01")==3):
        single_leadscrew = "RIGHT"
    else:
        single_leadscrew = "NULL"

    if(buttons.find("01")==4 and prev_button_value != buttons and prev_button_value.find("01")!=4):
        c_negative=c_negative+1
        c_positive = 0
        if(c_negative%4==0):
            desired_ang = 0
        elif(c_negative%4==1):
            desired_ang = -45
        elif(c_negative%4==2):
            desired_ang = -90
        elif(c_negative%4==3):
            desired_ang = -179

        prev_button_value = buttons

    elif(buttons.find("01")==5 and prev_button_value != buttons and prev_button_value.find("01")!=5):
        c_positive=c_positive+1
        c_negative = 0
        if(c_positive%4==0):
            desired_ang = 0
        elif(c_positive%4==1):
            desired_ang = 45
        elif(c_positive%4==2):
            desired_ang = 90
        elif(c_positive%4==3):
            desired_ang = 179

        prev_button_value = buttons

    if(buttons.find("01")==6):
        servo = "OUT"
    else:
        servo = "NULL"
    
    if(buttons.find("01")==7 and prev_button_value.find("01")!=7 and prev_button_value!=buttons):
        only_one_hit = "FWD"
        prev_button_value = buttons
    else:
        only_one_hit = "NULL"

    if(buttons.find("01")==8 and prev_button_value.find("01")!=8 and prev_button_value!=buttons):
        multiple_hits = "FWDN"
        prev_button_value = buttons
    else:
        multiple_hits = "NULL"

    if(only_one_hit=="FWD" and multiple_hits=="FWDN"):
        only_one_hit="NULL"

    if(buttons.find("01")==9 and prev_button_value.find("01")!=9 and prev_button_value!=buttons):
        flybelt_duty = flybelt_duty + 1
        flybelt_duty = flybelt_duty%4
        prev_button_value = buttons

    if(buttons.find("01")==11):
        rotate = "LEFT"
    elif(buttons.find("0")==12):
        rotate = "RIGHT"
    else:
        rotate = "NULL"

    for i in range(3):
        overall_message.append(velocities[i])
    overall_message.append(leadscrew)
    overall_message.append(single_leadscrew)
    overall_message.append(desired_ang)
    overall_message.append(servo)
    overall_message.append(only_one_hit)
    overall_message.append(multiple_hits)
    overall_message.append(flybelt_duty)
    overall_message.append(rotate)

    client.send(str(overall_message).encode('utf-8'))
    overall_message=[]
    prev_button_value = buttons