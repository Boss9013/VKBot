import vk_api
import configparser
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = vk_api.VkApi(token="moi token")
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, zachem?)

for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.object["message"]["text"]
            admin = event.object["message"]["from_id"]
            beseda=event.object["message"]["peer_id"]
            try:
                name=vk.users.get(user_ids=admin)[0]["first_name"]
                name3=f"@id{admin} ({name})"
            except vk_api.exceptions.ApiError:
                None
            trytext=["!try", "/try"]
            infotext=["!инфа", "/инфа"]
            ono=event.object["message"]["text"]
            message = str(event.object["message"]["text"])
            config = configparser.ConfigParser()
            config.read("settings.ini")
            try:
                    mutted = config["mutted"][str(beseda)]
                    if str(mutted) in str(admin):
                            vk.messages.delete(conversation_message_ids=event.object["message"]["conversation_message_id"], peer_id=beseda, delete_for_all=1);
            except KeyError:
                    None
            except vk_api.exceptions.ApiError:
                    None
            members=vk.messages.getConversationMembers(peer_id=beseda, fields="items")
            try:
                    banned = config["banned"][str(beseda)]
                    if event.object["message"]["action"]["type"] == "chat_invite_user":
                            if str(banned) in str(event.object["message"]["action"]["member_id"]):
                                    vk.messages.removeChatUser(chat_id=beseda-2000000000, user_id=str(event.object["message"]["action"]["member_id"]))
                                    vk.messages.send(peer_id=event.object["message"]["peer_id"], message=f"{name3}, данный пользователь находится в бане!",  random_id=0)
            except KeyError:
                    None

            try:
                    user=event.object["message"]["action"]["member_id"]
                    name4=vk.users.get(user_ids=user)[0]["first_name"]
                    if event.object["message"]["action"]["type"] == "chat_invite_user":
                        vk.messages.send(peer_id=event.object["message"]["peer_id"], message=f"Добро пожаловать в нашу беседу, @id{user} ({name4})", random_id=0)
                    if event.object["message"]["action"]["type"] == "chat_kick_user":
                        vk.messages.send(peer_id=event.object["message"]["peer_id"], message=f"Пока, @id{user} ({name4}), хотя ты это уже не услышишь(", random_id=0)
            except KeyError:
                    None
            except vk_api.exceptions.ApiError:
                    None
            if msg in ['!кик', '!выгнать', '!kick']:
                         for i in members["items"]:
                                 if i["member_id"] == admin:
                                       admin = i.get('is_admin', False)
                                       if admin == True:
                                          try:
                                                kicked = event.object["message"]["reply_message"]["from_id"]
                                                msgkicked = event.object["message"]["reply_message"]["text"]
                                                print(name3)
                                                vk.messages.removeChatUser(chat_id=beseda-2000000000, user_id=event.object["message"]["reply_message"]["from_id"])
                                          except vk_api.exceptions.ApiError:
                                                    vk.messages.send(peer_id=event.object["message"]["peer_id"], message=f"{name3}, Недостаточно прав чтобы кикнуть данного пользователя!",  random_id=0)
                                                    None
                                          except KeyError:
                                                    vk.messages.send(peer_id=event.object["message"]["peer_id"], message=f"{name3}, Ошибка! Ответьте на сообщение пользователя которого хотите кикнуть.",  random_id=0)
                                                    None
                                          else:
                                                    vk.messages.send(peer_id=event.object["message"]["peer_id"], message=f"{name3}, Пользователь: @id{kicked} был кикнут, его последние слова: {msgkicked}",  random_id=0)

            if msg in ['!открепить']:
                                         vk.messages.send(peer_id=beseda, message=f"{name3}, Сообщение успешно откреплено!", random_id=0)
                                         vk.messages.unpin(peer_id=beseda)
            for word in ono[0:4].lower().split():
                    if word in trytext:
                                         randomtextda = random.SystemRandom().choice(["сегодня явно ни твой день!", "Тебе повезло, ты везунчик!"])
                                         vk.messages.send(peer_id=beseda, message=f"{name3}, {randomtextda}", random_id=0)
            if msg in ['!информация', '/information' '!information']:
                                         try:
                                                 config.get("mutted", str(beseda))
                                         except configparser.NoOptionError:
                                                 config.set("mutted", str(beseda), "ни какой")
                                                 with open("settings.ini", 'w') as f:
                                                         config.write(f)
                                                 None
                                         try:
                                                 config.get("banned", str(beseda))
                                         except configparser.NoOptionError:
                                                 config.set("banned", str(beseda), "ни какой")
                                                 with open("settings.ini", 'w') as f:
                                                         config.write(f)
                                                 None
                                         muttedpeople=config.get("mutted", str(beseda))
                                         bannedpeople=config.get("banned", str(beseda))
                                         countmembers=vk.messages.getConversationMembers(peer_id=beseda, fields="count")["count"]
                                         vk.messages.send(peer_id=beseda, message=f"{name3}, информация беседы: \n Название: \n Участников в беседе: {countmembers}. \n В муте: @id{muttedpeople}(данный)  пользователь. \n В бане: @id{bannedpeople}(данный) пользователь.", random_id=0)
            if msg in ['!random1', '!рандом1', '/random1', '/рандом1']:
                                         randomintda=random.randint(1,6)
                                         vk.messages.send(peer_id=beseda, message=f"{name3}, Кручу 🎲 \n Выпадает число {randomintda}!", random_id=0)
            if msg in ['!random2', '!рандом2', '/random2', '/рандом2']:
                                         randomintda=random.randint(1,6)
                                         randomintda2=random.randint(1,6)
                                         vk.messages.send(peer_id=beseda, message=f"{name3}, Кручу два 🎲 \n У первого выпадает число {randomintda}, у второго {randomintda2}!", random_id=0)
            for word in ono[0:5].lower().split():
                    if word in infotext:
                        try:
                                         randomintda=random.randint(0,100)
                                         vk.messages.send(peer_id=beseda, message=f"{name3}, вероятность этого составляет: {randomintda}%", random_id=0)
                        except vk_api.exceptions.ApiHttpError:
                            None
            if msg in ['!команды', '!commands', '!списокоманд', '!помощь']:
                                         vk.messages.send(peer_id=beseda, message=f"{name3}, Помощь: \n Раздел: Администрирование: \n 1. !ban !бан !забанить - забанить пользователя. \n 2. !unban !разбанить !снятьбан - разбанить пользователя. \n 3. !кик !kick !выгнать - кикнуть пользователя. \n 4. !mute !мут !замутить - замутить пользователя. \n 5. !unmute !снятьмут - размутить пользователя. \n 6. !закрепить - закрепить сообщение. \n 7. !открепить - открепить сообщение. \n 8. !название - изменить название беседы. \n 9. !ссылка - проверить ссылку на хаки и т.п. \n Раздел: Мини-игры: \n 1. !random1&2 !рандом1&2 /random1&2 или 2 /рандом1&2 - рандомайзер, пишет число от 1 до 6, или же в двойном кол-во если напишите команду с 2. \n 2. !try /try - РП отыгровка действие. \n 3. !инфа /инфа - сообщает вероятность вашего высказывание.", random_id=0)
            if msg in ['!help']:
                                         vk.messages.send(peer_id=beseda, message=f"{name3}, Привет! \n я, бот ВК, помогаю администратором беседе следя за участниками беседы! Могу заблокировать, замутить, кикнуть пользователя! Проверить ссылку на вредоностные ПО, изменить название беседы, закрепить сообщение, или же открепить! \n Помощь по командам: !помощь", random_id=0)
            if msg in ['!закрепить']:
                                         try:
                                                 vk.messages.pin(peer_id=beseda, conversation_message_id=event.object["message"]["reply_message"]["conversation_message_id"])
                                         except KeyError:
                                                 vk.messages.send(peer_id=beseda, message=f"{name3}, Ошибка! Ответьте на сообщение пользователя чтобы закрепить его!", random_id=0)
                                                 None
                                         except vk_api.exceptions.ApiError:
                                                 vk.messages.send(peer_id=beseda, message=f"{name3}, Произошла неизвестная ошибка.", random_id=0)
                                                 None
                                         else:
                                                 vk.messages.send(peer_id=beseda, message=f"{name3}, Сообщение успешно закреплено!", random_id=0)
            if msg in ['!название']:
                                         try:
                                                 vk.messages.editChat(chat_id=beseda-2000000000, title=event.object["message"]["reply_message"]["text"])
                                         except KeyError:
                                                 vk.messages.send(peer_id=beseda, message=f"{name3}, Ошибка! Ответьте на сообщение пользователя чтобы изменить название беседы!", random_id=0)
                                                 None
                                         else:
                                                 vk.messages.send(peer_id=beseda, message=f"{name3}, Название беседы успешно изменено!", random_id=0)
            if msg in ['!ссылка']:
                                                 try:
                                                         url = event.object["message"]["reply_message"]["text"]
                                                         itog2 = vk.utils.checkLink(url=event.object["message"]["reply_message"]["text"])
                                                         itog = itog2.get("status")
                                                         vk.utils.checkLink(url=event.object["message"]["reply_message"]["text"])
                                                 except KeyError:
                                                         vk.messages.send(peer_id=beseda, message=f"{name3}, Ошибка! Ответьте на сообщение пользователя чтобы проверить ссылку!", random_id=0)
                                                         None
                                                 except vk_api.exceptions.ApiError:
                                                         vk.messages.send(peer_id=beseda, message=f"{name3}, Данное слово не является ссылкой!", random_id=0)
                                                         None
                                                 else:
                                                         vk.messages.send(peer_id=beseda, message=f"{name3}, Статус ссылки {url}: {itog}", random_id=0)
            if msg in['!замутить', "!mute", "!мут"]:
                         for i in members["items"]:
                                 if i["member_id"] == admin:
                                       admin = i.get('is_admin', False)
                                       if admin == True:
                                            try:
                                                     if str(event.object["message"]["reply_message"]["from_id"]) in str(-195336191):
                                                         vk.messages.send(peer_id=beseda, message=f"{name3}, вы не можете замутить данного пользователя!", random_id=0)
                                                         break
                                                     config.set("mutted", str(beseda), str(event.object["message"]["reply_message"]["from_id"]))
                                                     state = None
                                                     with open("settings.ini", 'w') as f:
                                                        config.write(f)
                                                     muttedpeople=event.object["message"]["reply_message"]["from_id"]
                                                     vk.messages.send(peer_id=beseda, message=f"{name3}, вы замутили @id{muttedpeople}(данного) пользователя.", random_id=0)
                                            except KeyError:
                                                 vk.messages.send(peer_id=beseda, message=f"{name3}, ответьте на сообщение пользователя чтобы замутить его!", random_id=0)
                                                 None
            if msg in['!снятьмут', "!unmute"]:
                         for i in members["items"]:
                                 if i["member_id"] == admin:
                                       admin = i.get('is_admin', False)
                                       if admin == True:
                                          try:
                                              muttedpeople=config.get("mutted", str(beseda))
                                              config.remove_option("mutted", str(beseda))
                                              state = None
                                              with open("settings.ini", 'w') as f:
                                                config.write(f)
                                              vk.messages.send(peer_id=beseda, message=f"{name3}, вы размутили @id{muttedpeople}(данного) пользователя.", random_id=0)
                                          except NameError:
                                            vk.messages.send(peer_id=beseda, message=f"{name3}, в данный момент никто ни находится в муте!", random_id=0)
                                            None
                                          except configparser.NoOptionError:
                                            vk.messages.send(peer_id=beseda, message=f"{name3}, в данный момент никто ни находится в муте!", random_id=0)
                                            None
            if msg in["!забанить", "!ban", "!бан"]:
                try:
                    if str(event.object["message"]["reply_message"]["from_id"]) in str(-195336191):
                        vk.messages.send(peer_id=beseda, message=f"{name3}, вы не можете забанить данного пользователя!", random_id=0)
                        break
                    vk.messages.removeChatUser(chat_id=beseda-2000000000, user_id=event.object["message"]["reply_message"]["from_id"])
                    config.set("banned", str(beseda), str(event.object["message"]["reply_message"]["from_id"]))
                    state = None
                    with open("settings.ini", 'w') as f:
                        config.write(f)
                    muttedpeople=event.object["message"]["reply_message"]["from_id"]
                    vk.messages.send(peer_id=beseda, message=f"{name3}, вы забанили @id{muttedpeople}(данного) пользователя.", random_id=0)
                except vk_api.exceptions.ApiError:
                    vk.messages.send(peer_id=beseda, message=f"{name3}, недостаточно прав чтобы забанить данного пользователя!", random_id=0)
                    None
                except KeyError:
                    vk.messages.send(peer_id=beseda, message=f"{name3}, ответьте на сообщение пользователя чтобы забанить его!", random_id=0)
                    None

            if msg in["!разбанить", "!unban", "!снятьбан"]:
                         for i in members["items"]:
                                 if i["member_id"] == admin:
                                       admin = i.get('is_admin', False)
                                       if admin == True:
                                             try:
                                                 muttedpeople=config.get("banned", str(beseda))
                                                 config.remove_option("banned", str(beseda))
                                                 state = None
                                                 with open("settings.ini", 'w') as f:
                                                     config.write(f)
                                                 vk.messages.send(peer_id=beseda, message=f"{name3}, вы разбанили @id{muttedpeople}(данного) пользователя.", random_id=0)
                                             except NameError:
                                                vk.messages.send(peer_id=beseda, message=f"{name3}, в данный момент никто ни находится в бане!", random_id=0)
                                                None
                                             except configparser.NoOptionError:
                                                 vk.messages.send(peer_id=beseda, message=f"{name3}, в данный момент никто ни находится в бане!", random_id=0)
                                                 None
