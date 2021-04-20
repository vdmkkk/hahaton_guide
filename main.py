import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from requests.exceptions import ReadTimeout
from keyboards import *
from templates import *

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
                        msg_extra = event.extra_values
                        print(msg_extra)

                        if event.user_id not in list(users.keys()):
                            users[event.user_id] = {'act': 'menu', 'fav': [], 'geo': ('0', '0'), 'page': 1}
                            vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Главное меню Hahaton Guide:', 'keyboard': menu_kbd(), 'random_id': 0})

                        else:
                            if users[event.user_id]['act'] == 'menu':
                                if msg == 'места поблизости':
                                    users[event.user_id]['act'] = 'places_menu'
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Мне нужно знать, где ты находишься', 'keyboard': places_menu_kbd(), 'random_id': 0})

                                elif msg == 'коллекция':
                                    if users[event.user_id]['fav']:
                                        users[event.user_id]['act'] = 'collection'
                                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Коллекция ваших мест:', 'template': carousel2(users[event.user_id]['page'], users[event.user_id]['fav'], users[event.user_id]['geo']), 'random_id': 0})
                                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': f'Страница {1}:', 'keyboard': nearby_kbd(), 'random_id': 0})
                                    else:
                                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'У вас пока нет мест в коллекции.\nМеню:', 'keyboard': menu_kbd(), 'random_id': 0})

                            elif users[event.user_id]['act'] == 'places_menu':
                                if 'geo' in full_msg['items'][0].keys():
                                    users[event.user_id]['act'] = 'nearby'
                                    users[event.user_id]['page'] = 1
                                    users[event.user_id]['geo'] = full_msg['items'][0]['geo']['coordinates']
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Список мест поблизости:',   'template': carousel1(users[event.user_id]['page'], users[event.user_id]['fav'], users[event.user_id]['geo']), 'random_id': 0})
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': f'Страница {1}:', 'keyboard': nearby_kbd(), 'random_id': 0})
                                else:
                                    if msg == 'назад':
                                        users[event.user_id]['act'] = 'menu'
                                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Меню:', 'keyboard': menu_kbd(), 'random_id': 0})
                                    else:
                                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'умоляю тебя пришли геолокацию 😭😭😭😭', 'keyboard': places_menu_kbd(), 'random_id': 0})

                            elif users[event.user_id]['act'] == 'nearby':
                                if msg == '&gt;':
                                    page = users[event.user_id]['page']
                                    if page != 3:
                                        page += 1
                                    else:
                                        page = 1

                                    users[event.user_id]['page'] = page
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': '&#12288;', 'template': carousel1(page, users[event.user_id]['fav'], users[event.user_id]['geo']),'random_id': 0})
                                    #  vk_session.method('messages.send', {'user_id': event.user_id, 'message': f'Страница {page}:', 'keyboard': nearby_kbd(), 'random_id': 0})
                                if msg == '&lt;':
                                    page = users[event.user_id]['page']
                                    if page != 1:
                                        page -= 1
                                    else:
                                        page = 3
                                    users[event.user_id]['page'] = page
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': '&#12288;', 'template': carousel1(page, users[event.user_id]['fav'], users[event.user_id]['geo']), 'random_id': 0})
                                    #  vk_session.method('messages.send', {'user_id': event.user_id, 'message': f'Страница {page}:', 'keyboard': nearby_kbd(), 'random_id': 0})

                                elif msg == 'назад':
                                    users[event.user_id]['act'] = 'menu'
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Меню:', 'keyboard': menu_kbd(), 'random_id': 0})

                                else:
                                    if 'payload' in msg_extra.keys():
                                        id = eval(msg_extra['payload'])['id']
                                        if id not in users[event.user_id]['fav']:
                                            users[event.user_id]['fav'].append(id)
                                            vk_session.method('messages.send',  {'user_id': event.user_id, 'message': 'Место добавлено в коллецию!\n\n\n', 'template': carousel1(users[event.user_id]['page'], users[event.user_id]['fav'], users[event.user_id]['geo']), 'random_id': 0})
                                            # vk_session.method('messages.send', {'user_id': event.user_id, 'message': f'Страница {users[event.user_id]["page"]}:', 'keyboard': nearby_kbd(), 'random_id': 0})
                                        else:
                                            del(users[event.user_id]['fav'][users[event.user_id]['fav'].index(id)])
                                            vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Место было удалено из коллекции\n\n\n', 'template': carousel1(users[event.user_id]['page'], users[event.user_id]['fav'], users[event.user_id]['geo']), 'random_id': 0})
                                            # vk_session.method('messages.send', {'user_id': event.user_id, 'message': f'Страница {users[event.user_id]["page"]}:', 'random_id': 0})
                            elif users[event.user_id]['act'] == 'collection':
                                if msg == 'назад':
                                    users[event.user_id]['act'] = 'menu'
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Меню:', 'keyboard': menu_kbd(), 'random_id': 0})
                                else:
                                    if 'payload' in msg_extra.keys():
                                        if 'id' in eval(msg_extra['payload']).keys():
                                            id = eval(msg_extra['payload'])['id']
                                            del(users[event.user_id]['fav'][users[event.user_id]['fav'].index(id)])
                                            if users[event.user_id]['fav']:
                                                vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Коллекция ваших мест:', 'template': carousel2(users[event.user_id]['page'], users[event.user_id]['fav'], users[event.user_id]['geo']), 'random_id': 0})
                                                vk_session.method('messages.send', {'user_id': event.user_id, 'message': f'Страница {1}:', 'keyboard': nearby_kbd(), 'random_id': 0})
                                            else:
                                                users[event.user_id]['act'] = 'menu'
                                                vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'У вас пока нет мест в коллекции.\nМеню:', 'keyboard': menu_kbd(), 'random_id': 0})
                        save = open('users.txt', mode='w', encoding='utf-8').write(str(users))
        except ReadTimeout:
            break
