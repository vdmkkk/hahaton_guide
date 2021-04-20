import json
import sqlite3
import mpu

PLACES = []

con = sqlite3.connect('places.db')
cur = con.cursor()

result = cur.execute("""SELECT id, title, description, photo, lat, lon FROM places""").fetchall()

for i in result:
    PLACES.append(dict())
    PLACES[-1]['id'] = i[0]
    PLACES[-1]['title'] = i[1]
    PLACES[-1]['description'] = i[2]
    PLACES[-1]['photo'] = i[3]
    PLACES[-1]['lat'] = i[4]
    PLACES[-1]['lon'] = i[5]


def carousel1(page, fav, geo):
    for i in PLACES:
        if str(i['id']) in fav:
            PLACES[PLACES.index(i)]['added'] = ('Убрать из коллекции', 'negative')
        else:
            PLACES[PLACES.index(i)]['added'] = ('Добавить в коллекцию', 'secondary')

        PLACES[PLACES.index(i)]['distance'] = round(mpu.haversine_distance((geo['latitude'], geo['longitude']), (PLACES[PLACES.index(i)]['lat'], PLACES[PLACES.index(i)]['lon'])), 1)

    PLACES.sort(key=lambda x: x['distance'])

    carousel = {
        "type": "carousel",
        "elements": []
    }

    for i in range(len(PLACES) - 1, -1, -1):

        carousel['elements'].insert(0, {
            "photo_id": PLACES[(page - 1) * 10 + i]['photo'],
            "title": PLACES[(page - 1) * 10 + i]['title'],
            "description": PLACES[(page - 1) * 10 + i]['description'] + '\n' + f'Находится в {PLACES[(page - 1) * 10 + i]["distance"]} км от вас',
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": PLACES[(page - 1) * 10 + i]['added'][0],
                    "payload": '{' + f"\"id\":\"{PLACES[(page - 1) * 10 + i]['id']}\"" + '}'
                },
                "color": PLACES[(page - 1) * 10 + i]['added'][1]
            }, {
                "action": {
                    "type": "open_link",
                    "label": 'Открыть в Яндекс.картах',
                    "link": f"https://yandex.ru/maps/?pt={PLACES[(page - 1) * 10 + i]['lon']},{PLACES[(page - 1) * 10 + i]['lat']}&z=12&l=map",
                    "payload": "{}"
                }
            }
            ]
        }
                                    )

        if len(carousel['elements']) == 10:
            break

    carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
    carousel = str(carousel.decode('utf-8'))
    return carousel

# я не знаю как это комментировать


def carousel2(page, fav, geo):
    fav = list(map(lambda x: int(x), fav))
    fav_list = []
    for i in fav:
        for j in PLACES:
            if j['id'] == i:
                fav_list.append(j)
                fav_list[fav_list.index(j)]['distance'] = round(mpu.haversine_distance((geo['latitude'], geo['longitude']), (fav_list[fav_list.index(j)]['lat'], fav_list[fav_list.index(j)]['lon'])), 1)
    carousel = {
        "type": "carousel",
        "elements": []
    }

    for i in range(len(fav_list) - 1, -1, -1):

        carousel['elements'].insert(0, {
            "photo_id": fav_list[(page - 1) * 10 + i]['photo'],
            "title": fav_list[(page - 1) * 10 + i]['title'],
            "description": fav_list[(page - 1) * 10 + i]['description'] + '\n' + f'Находится в {fav_list[(page - 1) * 10 + i]["distance"]} км от вас',
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": 'Убрать из коллекции',
                    "payload": '{' + f"\"id\":\"{fav_list[(page - 1) * 10 + i]['id']}\"" + '}'
                },
                "color": 'negative'
            }, {
                "action": {
                    "type": "open_link",
                    "label": 'Открыть в Яндекс.картах',
                    "link": f"https://yandex.ru/maps/?pt={fav_list[(page - 1) * 10 + i]['lon']},{fav_list[(page - 1) * 10 + i]['lat']}&z=12&l=map",
                    "payload": "{}"
                }
            }
            ]
        }
                                    )

        if len(carousel['elements']) == 10:
            break

    carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
    carousel = str(carousel.decode('utf-8'))
    return carousel