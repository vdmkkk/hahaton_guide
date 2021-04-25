# файл с клавиатурами кнопок

import json
from math import fabs


PLACES = ['Место 1', 'Место 2', 'Место 3', 'Место 4', 'Место 5', 'Место 6', 'Место 7', 'Место 8', 'Место 9', 'Место 10', 'Место 11', 'Место 12']
TOTAL_PLACES = 12


def menu_kbd():
    keyboard = {
        "one_time": False,
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Места поблизости"
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Коллекция"
                },
                "color": "secondary"
            }, ]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def places_menu_kbd():
    keyboard = {
        "one_time": False,
        "buttons": [
            [{
                "action": {
                    "type": "location",
                    "payload": "{\"button\": \"1\"}"
                }
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Назад"
                },
                "color": "negative"
            }, ]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def nearby_kbd_old(page):
    keyboard = {
        "one_time": False,
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": PLACES[0]
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": PLACES[1]
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": PLACES[2]
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": PLACES[3]
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": PLACES[4]
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"7\"}",
                    "label": "<"
                },
                "color": "primary"
            },
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"2\"}",
                        "label": "Назад"
                    },
                    "color": "negative"
                },

                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"7\"}",
                        "label": ">"
                    },
                    "color": "primary"
                }
            ]
        ]
    }
    if (page - 1) * 5 + 5 > TOTAL_PLACES:
        diff = TOTAL_PLACES - (page - 1) * 5 - 5
        diff = int(fabs(diff))
        for i in range(diff):
            del(keyboard['buttons'][-2])
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def nearby_kbd():
    keyboard = {
        "one_time": False,
        "buttons": [
                [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"7\"}",
                    "label": "<"
                },
                "color": "primary"
            },
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"2\"}",
                        "label": "Назад"
                    },
                    "color": "negative"
                },

                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"7\"}",
                        "label": ">"
                    },
                    "color": "primary"
                }
            ]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard
