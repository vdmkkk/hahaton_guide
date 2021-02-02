import json


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
                    "label": "Любимые места"
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Добавить свое место"
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
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Прислать геопозицию"
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Использовать предыдущую"
                },
                "color": "secondary"
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


def sending_geo_kbd():
    keyboard = {
        "one_time": False,
        "buttons": [
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


def nearby_kbd():
    keyboard = {
        "one_time": False,
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Место 1"
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Место 2"
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Место 3"
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Место 4"
                },
                "color": "secondary"
            }, ],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Место 5"
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
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard
