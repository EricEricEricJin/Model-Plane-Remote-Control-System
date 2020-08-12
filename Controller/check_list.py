class checkList:
    check_list = {
        "TO": 
        """
            CONTROL ... TEST
            ENG ... TEST
            COM ... CHECK

            FLAP ... 30
            A/T THR ... ON

            ATC ... ACK
            RUNWAY ... CLEAR
        """,

        "CLIMB":
        """
            POST RATE ... CHECK
                IF NOT
                    ENG ... TO/GA
                    FLAP ... 30
                    NOSE DOWN
            GEAR ... UP
            SPD TO 30KT
                FLAP ... 0
            AP_ALT_TAR ... SET
            AP_ALT ... ON
        """
    }
    def query(self, cmd):
        pass