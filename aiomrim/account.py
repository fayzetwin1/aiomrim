"""
Working with account-related functionalities (not API implementation)
"""
import aiomysql
from typing import Any, List, Tuple
import hashlib

async def register_account(
    login: str, nickname: str, firstname: str, sex: int, password: str, # default values
    host: str, port: int, user = "root", db_password = "", database = "mrimdb", # mysql connection
    last_name = None, birthday = None, zodiac = None, phone = None, avatar = None,
    create_default_groups: bool = True) -> int: # optional value
    
    DEFAULT_GROUPS: List[str] = [
        " ^t ^` ^c    ^l ^o",
        "        ^k  ",
        " ^z            ",
        " ^~ ^a ^b     ^l    ^k  ",
    ]

    hash = hashlib.md5(password.encode("utf-8")).hexdigest()
    db = {"host": host, "port": port, "user": user, "password": db_password, "db": database}
    user_data = {
        "login": login, "nick": nickname, "f_name": firstname, "l_name": last_name, 
        "sex": sex, "passwd": hash, "birthday": birthday, "zodiac": zodiac, "phone": phone, "avatar": avatar}
    
    fields, values, placeholders = [], [], []

    for k, v in user_data.items():
        if v is not None:
            fields.append(k)
            values.append(v)
            placeholders.append("%s")

    sql_user = f"INSERT INTO user ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"

    values_tuple = tuple(values)

    user_id: int = -1
    pool = None

    try:
        pool = await aiomysql.create_pool(**db)
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql_user, values_tuple)
                user_id = cursor.lastrowid
                
                if not user_id:
                    raise Exception("failed to retrieve user_id after insertion")
                
                if create_default_groups:
                    sql_group = "INSERT INTO contact_group (user_id, name, idx) VALUES (%s, %s, %s)"
                    group_data: List[Tuple[int, str, int]] = [
                        (user_id, name, idx) 
                        for idx, name in enumerate(DEFAULT_GROUPS)
                    ]
                    print(f'sql_group: {sql_group}, group_data: {group_data}')
                    await cursor.executemany(sql_group, group_data)

                await conn.commit()
        return user_id
    except Exception as e:
        raise e
    finally:
        if pool:
            pool.close()
            await pool.wait_closed()
    
    
    