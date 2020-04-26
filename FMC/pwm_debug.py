import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

port = int(input("port: "))
freq = int(input("freq: "))

GPIO.setup(port, GPIO.OUT)
pwm = GPIO.PWM(port, freq)
pwm.start(0)

while True:

    duty = int(input("duty: "))
    if duty == 114:
        break
    pwm.ChangeDutyCycle(duty)

pwm.stop()
GPIO.cleanup()