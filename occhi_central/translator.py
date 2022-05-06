def translate_message():
    """
    Translates a message from BLE to MQTT
    """

    message = {
        "forward": False,
        "backward": False,
        "left": False,
        "right": False,
        "stop": False,
        "turn": False,
    }

    initials_list = [
        {"FW": "foward"},
        {"BW": "backward"},
        {"LT": "left"},
        {"RT": "right"},
        {"ST": "stop"},
        {"TR": "turn"},
    ]

    for initial, translated_command in initials_list:
        if command == initial:
            message[translated_command] = True
            print("Recebido comando, {}".format(translated_command))

    return message
