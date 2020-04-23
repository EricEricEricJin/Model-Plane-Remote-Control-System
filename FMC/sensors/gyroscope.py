from global_var import data_list
from time import sleep
from threading import Thread

class Gyroscope:
    KEY = "GYROSCOPE"
    def __init__(self):
        self.serve = True
        pass

    def init(self):
        pass

    def run(self):
        t = Thread(target = self._service, args = ())
        t.start()

    def _service(self):
        while self.serve:
            pass

    def is_broken(self):
        pass

    def __del__(self):
        self.serve = False
        pass