from motions.esc import Esc
import config_file

class Engine:
    def __init__(self):
        pass

    def init(self):
        self.eng_1 = Esc()
        self.eng_2 = Esc()
        if self.eng_1.init(config_file.ENGINE_1_BCM, config_file.ESC_FREQ, 0) != 1:
            return 0
        
        if self.eng_2.init(config_file.ENGINE_2_BCM, config_file.ESC_FREQ, 0) != 1:
            return 0

        return 1

    def change_pwr(self, pwr): # [0 - 100, 0 - 100]
        self.eng_1.change_pwr(pwr[0])
        self.eng_2.change_pwr(pwr[1])

    def __del__(self):
        del(self.eng_1)
        del(self.eng_2)