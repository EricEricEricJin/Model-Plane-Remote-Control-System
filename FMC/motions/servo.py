import RPi.GPIO as GPIO
import config_file

class Servo:
    def __init__(self):
        pass
        
    def init(self, BCM_PORT, FREQ, init_deg):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(BCM_PORT, GPIO.OUT)
            self.servo = GPIO.PWM(BCM_PORT, FREQ)
            self.servo.start(config_file.SERVO_DEG2DUTY(init_deg))
            return 1
        except:
            return 0

    def change_deg(self, deg):
        self.servo.ChangeDutyCycle(config_file.SERVO_DEG2DUTY(deg))

    def __del__(self):
        self.servo.stop()
        GPIO.cleanup()