import RPi.GPIO as GPIO
import config_file

class Esc:
    def __init__(self):
        pass

    def init(self, BCM_PORT, FREQ, init_pwr):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(BCM_PORT, GPIO.OUT)
            self.esc = GPIO.PWM(BCM_PORT, FREQ)
            self.esc.start(config_file.ESC_PWR2DUTY(0))
            return 1
        except:
            return 0

    def change_pwr(self, pwr):
        self.esc.ChangeDutyCycle(config_file.ESC_PWR2DUTY(pwr))

    def __del__(self):
        self.esc.stop()
        GPIO.cleanup()