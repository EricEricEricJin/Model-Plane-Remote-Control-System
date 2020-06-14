command_list = {
    """
        Write by communication
        Read by
            main
            AP
            MCAS
    """

    "AP_ALT_ON": None, "AP_ALT_VAL": None, "AP_VS_VAL": None,
    "AP_HDG_ON": None, "AP_HDG_VAL": None,
    "AP_VEL_ON": None, "AP_VEL_VAL": None,
    "LEVER_X": None, "LEVER_Y": None,
    "RUDDER": None,
    "GEAR_DOWN": None,
    "THRUST_1": None, "THRUST_2": None,
    "MCAS_ON": None,
    "INDIRECT": None
}

data_list = {
    """
        Write by sensors
        Read by
            communication
            AP
            MCAS
    """

    "PITCH": None, "YAW": None, "ROLL": None,
    "ALT": None, "RADIO_H": None,
    "AIR_V": None, "GROUND_V": None,

    """
        Write by motion
        Read by
            communication
    """


    "ENG_1": None, "ENG_2": None,
    "REV_1": None, "REV_2": None,
    "RUDDER": None,
    "ELEVATOR": None,
    "AILERON": None,
    "FLAPS": None,
    "GEAR_DOWN": None
}

video = None
