from flask import Flask, render_template, request, Response
import RPI.GPIO as GPIO
import time
import io
import threading 
import picamera

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

RIGHT_FORWARD = 26
RIGHT_BACKWARD = 19
RIGHT_PWM = 13
LEFT_FORWARD = 21
LEFT_BACKWARD = 20
LEFT_PWM = 16

GPIO.setup(RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(RIGHT_BACKWARD, GPIO.OUT)
GPIO.setup(RIGHT_PWM, 0)
GPIO.output(LEFT_PWM, 0)
RIGHT_MOTOR = GPIO.PWM(RIGHT_PWM, 100)
RIGHT_MOTOR.start(0)
RIGHT_MOTOR.ChangeDutyCycle(0)

GPIO.setup(LEFT_FORWARD, GPIO.OUT)
GPIO.setup(LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(LEFT_PWM, 0)
GPIO.output(LEFT_PWM, 0)
LEFT_MOTOR = GPIO.PWM(LEFT_PWM, 100)
LEFT_MOTOR.start(0)
LEFT_MOTOR.ChangeDutyCycle(0)

def getDistance():
	GPIO.output(TRIG, GPIO.LOW)
	time.sleep(1)

	GPIO.output(TRIG, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(TRIG, GPIO.LEFT_FORWARD)

	while GPIO.input(ECHO) == 0:
		pulse_start = time.time()

	while GPIO.input(ECHO) == 1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)

	return distance

def rightMotor(forward, backward, pwm):
	GPIO.output(RIGHT_FORWARD, forward)
	GPIO.output(RIGHT_BACKWARD, backward)
	RIGHT_MOTOR.ChangeDutyCycle(pwm)

def leftMotor(forward, backward, pwm):
	GPIO.output(LEFT_FORWARD, forward)
	GPIO.output(LEFT_BACKWARD, backward)
	LEFT_MOTOR.ChangeDutyCycle(pwm)

def forward():
	rightMotor(1, 0, 70)
	leftMotor(1, 0, 70)
	time.sleep(1)

def left():
	rightMotor(1, 0, 70)
	leftMotor(1, 0, 70)
	time.sleep(0.3)

def right():
	rightMotor(1, 0, 70)
	leftMotor(0, 0, 0)
	time.sleep(0.3)

def stop():
	rightMotor(0, 0, 0)
	leftMotor(0, 0, 0)

def backward():
	rightMotor(0, 1, 70)
	leftMotor(0, 1, 70)
	time.sleep(0.3)

"""
@app.route("/<command>")
def action(command):
	distance_value = getDistance()
	
	if command == "W":
		forward()
		message = "Forwarding"
	elif command == "A":
		left()
		message = "Lefting"
	elif command == "D":
		right()
		message = "Righting"
	elif command == "S":
		backward()
		message = "Backwarding"
	else:
		stop()
		meesage = "Unknown Command [" + command + "]"

	msg = {
		'message' : message,
		'distance' : str(distance_value)
	}

	retun render_template('video.html', **msg)
"""

if __name__ == '__main__':
	try:
		while True:
			distance_value = getDistance()
			if distance_value > 50:
				print("Forward " + str(distance_value))
				rightMotor(1, 0, 70)
				leftMotor(1, 0, 70)
				time.sleep(1)
			else:
				print("Left " + str(distance_value))
				rightMotor(0, 0, 0)
				leftMotor(1, 0, 70)
				time.sleep(1)

	except KeyboardInterrupt:
		print("키보드인터럽트로 인해 종료됨")
		GPIO.cleanup()
