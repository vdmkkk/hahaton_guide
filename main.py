import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from requests.exceptions import ReadTimeout
from keyboards import *

token = 'f0da5a6fccf45e7b213805f79c9c0c2eaf962bcccaee6bb210a5b6d756015839690c5652b06d859ab6253'
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

users = eval(open('users.txt', mode='r+', encoding='utf-8').read())

while True:
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.from_user and not event.from_me:
                        msg = event.text.lower()
                        full_msg = vk_session.method('messages.getById', {'message_ids': event.message_id, 'preview_length': 0})

                        if event.user_id not in list(users.keys()):
                            users[event.user_id] = {'act': 'menu', 'fav': [], 'geo': ('0', '0')}
                            vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Главное меню Hahaton Guide:', 'keyboard': menu_kbd(), 'random_id': 0})

                        else:
                            if users[event.user_id]['act'] == 'menu':
                                if msg == 'места поблизости':
                                    users[event.user_id]['act'] = 'places_menu'
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Мне нужно знать, где ты находишься', 'keyboard': places_menu_kbd(), 'random_id': 0})

                            elif users[event.user_id]['act'] == 'places_menu':
                                if msg == 'прислать геопозицию':
                                    users[event.user_id]['act'] = 'sending_geo'
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Жду <3', 'keyboard': sending_geo_kbd(), 'random_id': 0})
                                elif msg == 'использовать предыдущую':
                                    if users[event.user_id]['geo'] == ('0', '0'):
                                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'У вас нет предыдущей геопозиции', 'keyboard': places_menu_kbd(), 'random_id': 0})
                                    else:
                                        users[event.user_id]['act'] = 'nearby'
                                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Список мест поблизости:', 'keyboard': nearby_kbd(), 'random_id': 0})
                                elif msg == 'назад':
                                    users[event.user_id]['act'] = 'menu'
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Меню:', 'keyboard': menu_kbd(), 'random_id': 0})

                            elif users[event.user_id]['act'] == 'sending_geo':
                                if 'geo' in list(full_msg['items'][0].keys()):
                                    users[event.user_id]['geo'] = full_msg['items'][0]['geo']['coordinates']
                                    users[event.user_id]['act'] = 'nearby'
                                    print(full_msg['items'][0])
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Список мест поблизости:', 'keyboard': nearby_kbd(), 'random_id': 0})
                                elif msg == 'назад':
                                    users[event.user_id]['act'] = 'places_menu'
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Мне нужно знать, где ты находишься', 'keyboard': places_menu_kbd(), 'random_id': 0})

                            elif users[event.user_id]['act'] == 'nearby':
                                if msg == 'назад':
                                    users[event.user_id]['act'] = 'menu'
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Меню:', 'keyboard': menu_kbd(), 'random_id': 0})

                        save = open('users.txt', mode='w', encoding='utf-8').write(str(users))
        except ReadTimeout:
            break