# Документация Aiomrim

Содержание:

[Начало](#Начало)

[Основные методы](#основные-методы)

[Примеры](#примеры)

## Начало

В первую очередь, стоит начать с того, что библиотека Aiomrim является асинхронной, и ее следует использовать, соотвественно, в асинхронных проектах на Python. 

Установить Aiomrim можно следующей командой:
    
    pip install aiomrim

## Основные методы

| Метод | Описание метода | Аргументы | API метод |
| ------ | ----------- | ----------- | ---------- |
| online.get_online  | получение информации о пользователях, их количество и список пользователей | url: string | (GET) /users/online
| online.get_raw_online | по сути то же самое что и online.get_online, но еще и с технической информацией, включая IP и версию протокола | url: string | (GET) /users/rawOnline
| check_connection.check_connection   | проверка подключения к серверу (грубо говоря, ping-pong) | url: string | его нет ¯\_(ツ)_/¯
| account.register_account | регистрация аккаунта на сервере | login: str, nickname: str, firstname: str, sex: int, password: str, host: str, port: int, user = "root", db_password = "", database = "mrimdb", last_name = None, birthday = None, zodiac = None, phone = None, avatar = None, create_default_groups: bool = True
| admin.send_announce | отправка сообщения от имени администратора всем пользователям инстанса (требует включенного админ-аккаунта в настройках самого MRIM-сервера) | url: str, message: str | /users/announce
| admin.send_mail_to_all | почти то же самое, что и admin.send_announce, но в виде пришедшего email. в большинстве случаев не имеет смысла, так как многие клиенты такое не обработают | url: str, message: str | /users/sendMailToAll

## Примеры

Рассмотрим основные примеры работы с Aiomrim. К примеру, получим информацию о пользователях через метод online.get_online:

```
from aiomrim.online import get_online 
import asyncio 

async def getonline():
    url = 'http://127.0.0.1:1862' # url от MRIM-сервера
    result = await get_online(url)
    print(f'online users: {result}')

asyncio.run(getonline())
```

или, создадим новый аккаунт на сервере:

```
from aiomrim.account import register_account
import asyncio 

async def reg_account():
    try:
        user_id = await register_account(
            login="fayzetwin10", 
            nickname="fayzetwin", 
            firstname="fayzetwin",
            sex=1,
            password="my_great_password",
            
            host="localhost",
            port=3306,
            user="root",
            db_password="my_password",
            database="mrimdb",
            
            last_name="User",
            birthday="1970-01-01",
            zodiac=8, # capricorn
            phone="88005553555",
            
            create_default_groups=False,
        )
        print(f"Registered user ID: {user_id}")
    except Exception as e:
        print(f"Error registering account: {e}")

asyncio.run(reg_account())
```