from threading import Thread
from motion import Motion
# auto pilot
class autoPilot:
    def __init__(self):
        self.alt_on = False
        self.hdg_on = False
        self.vel_on = False

        self.alt_tar = None
        self.alt_vs = None

        self.hdg_tar = None
        self.vel_tar = None

    def init(self):
        self.MOTION = Motion()
        self.MOTION.init()
        
        pass

    def run(self):
        t = Thread(target = self._service, args = ())
        t.start()

    def _service(self):
        pass

    def operate(operation):
        

    def __del__(self):
        pass