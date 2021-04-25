# в этом файле хранятся карусели

import json
import sqlite3
import mpu

places = []

con = sqlite3.connect('places.db')
cur = con.cursor()

result = cur.execute(
    """SELECT id, title, description, photo, lat, lon FROM places""").fetchall()  # достаем места из БД

for i in result:
    places.append(dict())
    places[-1]['id'] = i[0]
    places[-1]['title'] = i[1]
    places[-1]['description'] = i[2]
    places[-1]['photo'] = i[3]
    places[-1]['lat'] = i[4]
    places[-1]['lon'] = i[5]


def carousel1(page, fav, geo):
    for i in places:
        if str(i[
                   'id']) in fav:  # выводим разные кнопки в зависимости от наличия места в коллекции пользователя
            places[places.index(i)]['added'] = ('Убрать из коллекции', 'negative')
        else:
            places[places.index(i)]['added'] = ('Добавить в коллекцию', 'secondary')

        places[places.index(i)]['distance'] = round(
            mpu.haversine_distance((geo['latitude'], geo['longitude']),
                                   (places[places.index(i)]['lat'], places[places.index(i)]['lon'])), 1)
    #  вычисляем расстояние каждого места до пользователя и сортируем по нему список
    places.sort(key=lambda x: x['distance'])

    carousel = {
        "type": "carousel",
        "elements": []
    }

    for i in range(10):  # в этом цикле по одному будем добавлять места
        try:
            carousel['elements'].insert(0, {
                "photo_id": places[(page - 1) * 10 + i]['photo'],
                # ниже отдельно достаем фотки, названия и тд
                "title": places[(page - 1) * 10 + i]['title'],
                "description": places[(page - 1) * 10 + i][
                                   'description'] + '\n' + f'Находится в {places[(page - 1) * 10 + i]["distance"]} км от вас',
                "action": {
                    "type": "open_photo"
                },
                "buttons": [{
                    "action": {
                        "type": "text",
                        "label": places[(page - 1) * 10 + i]['added'][0],
                        "payload": '{' + f"\"id\":\"{places[(page - 1) * 10 + i]['id']}\"" + '}'
                        # специальный payload для отличия мест друг от друга
                    },
                    "color": places[(page - 1) * 10 + i]['added'][1]
                }, {
                    "action": {
                        "type": "open_link",
                        "label": 'Открыть в Яндекс.картах',  # ссылочка на яндекс карты
                        "link": f"https://yandex.ru/maps/?pt={places[(page - 1) * 10 + i]['lon']},{places[(page - 1) * 10 + i]['lat']}&z=12&l=map",
                        "payload": "{}"
                    }
                }
                ]
            }
                                        )
        except IndexError:  # если мест окажется < 10
            break
    carousel['elements'].reverse()  # развернем список кнопок для корректного отображения

    carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
    carousel = str(carousel.decode('utf-8'))
    return carousel


def carousel2(page, fav,
              geo):  # повторение функции выше, за исключением того, что здесь мы работаем со списком fav (коллекция)
    fav = list(map(lambda x: int(x), fav))
    fav_list = []
    for i in fav:
        for j in places:
            if j['id'] == i:
                fav_list.append(j)
                fav_list[fav_list.index(j)]['distance'] = round(
                    mpu.haversine_distance((geo['latitude'], geo['longitude']), (
                    fav_list[fav_list.index(j)]['lat'], fav_list[fav_list.index(j)]['lon'])), 1)
    fav_list.sort(key=lambda x: x['distance'])
    carousel = {
        "type": "carousel",
        "elements": []
    }

    for i in range(10):
        try:
            carousel['elements'].insert(0, {
                "photo_id": fav_list[(page - 1) * 10 + i]['photo'],
                "title": fav_list[(page - 1) * 10 + i]['title'],
                "description": fav_list[(page - 1) * 10 + i][
                                   'description'] + '\n' + f'Находится в {fav_list[(page - 1) * 10 + i]["distance"]} км от вас',
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
        except IndexError:
            break

        carousel['elements'].reverse()

    carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
    carousel = str(carousel.decode('utf-8'))
    return carousel


def places_len():  # два функциональных метода для подсчета максимума страниц
    return len(places)


def fav_len(fav):
    return len(fav)
