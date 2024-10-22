import sqlite3


db_name = 'user_settings.db'


""" Открытие и закрытие базы данных """

# Установить соидинения с БД
def connect_to_db(db_name):
    """
    Устанавливает соединение с базой данных и возвращает объекты соединения и курсора.
    
    Аргументы:
    db_name -- имя базы данных
    
    Возвращает:
    connection -- объект соединения SQLite
    cursor -- объект курсора SQLite
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return connection, cursor

# Закрыть соидинения с БД
def close_db_connection(connection):
    """
    Закрывает соединение с базой данных.
    
    Аргументы:
    connection -- объект соединения SQLite
    """
    connection.commit()
    connection.close()



""" Таблица: Друзья (Список друзей для чата) """

# Создать таблицу с Друзьями (Список чатов)
def create_friends_table(cursor):
    """
    Создает таблицу 'Friends' в базе данных, если она еще не существует.

    Аргументы:
    cursor -- объект курсора SQLite
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Уникальный инкремент
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,  -- Дата и время добавления записи, не пустое
            username TEXT NOT NULL UNIQUE CHECK(length(username) = 20),  -- Имя пользователя, текст ровно 20 символов, уникальное, не пустое
            nickname TEXT NOT NULL UNIQUE,  -- Псевдоним пользователя, строка, не пустая
            public_key TEXT NOT NULL  -- Публичный ключ RSA, строка в формате PEM, не пустая
        )
    ''')

# Добавить нового дурга в таблицу
def add_friend(connection, cursor, friend_data):
    """
    Добавляет друга в таблицу 'Friends'.

    Аргументы:
    cursor -- объект курсора SQLite
    friend_data -- словарь с данными о друге
    """
    query = '''
        INSERT INTO Friends (username, nickname, public_key)
        VALUES (?, ?, ?)
    '''
    try:
        cursor.execute(query, (friend_data['username'], friend_data['nickname'], friend_data['public_key']))
        connection.commit()
        return True
    except Exception as e:
        return False

# Удалить друга по его айдишнику
def delete_friend_by_id(connection, cursor, friend_id):
    """
    Удаляет друга из таблицы 'Friends' по его ID.

    Аргументы:
    cursor -- объект курсора SQLite
    friend_id -- ID друга, которого нужно удалить
    """
    query = 'DELETE FROM Friends WHERE id = ?'
    cursor.execute(query, (friend_id,))
    connection.commit()

# Получить спиоск всех друзей
def fetch_all_friends(cursor):
    """
    Возвращает список всех друзей из таблицы 'Friends'.

    Аргументы:
    cursor -- объект курсора SQLite

    Возвращает:
    Список словарей с данными о друзьях.
    """
    query = 'SELECT id, date_added, username, nickname, public_key FROM Friends'
    cursor.execute(query)
    rows = cursor.fetchall()

    friends_list = []
    for row in rows:
        friend = {
            'id': row[0],
            'date_added': row[1],
            'username': row[2],
            'nickname': row[3],
            'public_key': row[4]
        }
        friends_list.append(friend)
    
    return friends_list

# Получить список никнеймов Друзей
def get_friends_nicknames(cursor):
    """
    Возвращает список значений из колонки 'nickname' в таблице 'Friends'.
    
    Аргументы:
    cursor -- объект курсора SQLite
    
    Возвращает:
    Список никнеймов (может быть пустым).
    """
    try:
        # Выполняем запрос для выбора всех значений из колонки 'nickname'
        cursor.execute("SELECT nickname FROM Friends")
        
        # Извлекаем все результаты запроса
        rows = cursor.fetchall()
        
        # Проверяем, есть ли данные, и формируем список никнеймов
        if rows:
            nicknames = [row[0] for row in rows]
        else:
            nicknames = []  # Возвращаем пустой список, если данных нет
        
        return nicknames
    
    except Exception as e:
        print(f"Ошибка при извлечении никнеймов: {e}")
        return []

# Получить друга по никнейму
def get_friend_by_nickname(cursor, nickname):
    """
    Возвращает строку из таблицы 'Friends' по значению nickname.

    Аргументы:
    cursor -- объект курсора SQLite
    nickname -- псевдоним пользователя для поиска

    Возвращает:
    Словарь с данными пользователя или None, если пользователь не найден.
    """
    # SQL-запрос для поиска строки по nickname
    cursor.execute("SELECT * FROM Friends WHERE nickname = ?", (nickname,))
    
    # Получаем результат запроса
    row = cursor.fetchone()

    # Если запись найдена, возвращаем её как словарь
    if row:
        return {
            'id': row[0],
            'date_added': row[1],
            'username': row[2],
            'nickname': row[3],
            'public_key': row[4]
        }
    else:
        return None  # Если запись не найдена, возвращаем None


""" Таблица: Соидинения (Список БД для подключения) """

# Создание таблицы Соидинений, храниться список доступных баз для использования
def create_connection_table(cursor):
    # SQL-запрос для создания таблицы connections
    create_table_query = """
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_added DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        host TEXT NOT NULL,
        port TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        database_name TEXT NOT NULL,
        table_name TEXT NOT NULL,
        type_db TEXT NOT NULL,
        status TEXT NOT NULL,
        UNIQUE (host, database_name, table_name)  -- Уникальный индекс для комбинации полей
    );
    """
    # Выполняем запрос для создания таблицы
    cursor.execute(create_table_query)

# Добавить новую БД в таблицу
def add_connection(connection, cursor, host, port, username, password, database_name, table_name, type_db, status):
    """
    Добавляет запись в таблицу connections.

    :param cursor: Объект курсора SQLite
    :param host: Хост
    :param port: Порт
    :param username: Имя пользователя
    :param password: Пароль пользователя
    :param database_name: Название базы данных
    :param table_name: Название таблицы
    :param type_db: Тип базы данных
    :param status: Статус
    """
    insert_query = """
    INSERT INTO connections (host, port, username, password, database_name, table_name, type_db, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    try:
        cursor.execute(insert_query, (host, port, username, password, database_name, table_name, type_db, status))
        connection.commit()
        return True
    except sqlite3.IntegrityError as e:
        # Обработка ошибки уникальности
        return False

# Удаления Бд с таблицы
def delete_connection_by_id(connection, cursor, connection_id):
    """
    Удаляет запись из таблицы connections по id.

    :param cursor: Объект курсора SQLite
    :param connection_id: ID записи, которую нужно удалить
    """
    delete_query = "DELETE FROM connections WHERE id = ?;"
    cursor.execute(delete_query, (connection_id,))
    connection.commit()

# Список всех соидинений
def fetch_all_connections(cursor):
    """
    Возвращает список всех соединений из таблицы 'connections'.

    Аргументы:
    cursor -- объект курсора SQLite

    Возвращает:
    Список словарей с данными о соединениях.
    """
    query = 'SELECT id, date_added, host, port, username, password, database_name, table_name, type_db, status FROM connections'
    cursor.execute(query)
    rows = cursor.fetchall()

    connections_list = []
    for row in rows:
        connection = {
            'id': row[0],
            'date_added': row[1],
            'host': row[2],
            'port': row[3],
            'username': row[4],
            'password': row[5],
            'database_name': row[6],
            'table_name': row[7],
            'type_db': row[8],
            'status': row[9]
        }
        connections_list.append(connection)
    
    return connections_list

# Список доступных соидинений
def fetch_connection_info(cursor):
    """
    Получает данные из таблицы 'connections' и возвращает список строк, 
    где значения колонок 'host', 'database_name' и 'table_name' склеены 
    с использованием точки с запятой и пробела.

    Аргументы:
    cursor -- объект курсора SQLite

    Возвращает:
    Список строк с объединенными данными или пустой список, если таблица пуста.
    """
    try:
        # Выполняем запрос для выбора необходимых данных
        cursor.execute("""
            SELECT id, host, database_name, table_name
            FROM connections
        """)
        
        # Извлекаем все результаты запроса
        rows = cursor.fetchall()
        
        # Формируем список строк, объединяя данные с использованием точки с запятой и пробела
        if rows:
            connection_info_list = [
                f"{row[0]}/{row[1]}/{row[2]}/{row[3]}" for row in rows
            ]
        else:
            connection_info_list = []  # Возвращаем пустой список, если данных нет
        
        return connection_info_list
    
    except Exception as e:
        print(f"Ошибка при извлечении данных соединений: {e}")
        return []

# Получить соидинения по айдишнику
def get_connection_by_id(cursor, connection_id):
    """
    Находит и возвращает запись из таблицы 'connections' по заданному ID.

    Аргументы:
    cursor -- объект курсора SQLite
    connection_id -- ID соединения для поиска

    Возвращает:
    Словарь с данными соединения или None, если не найдено.
    """
    query = """
    SELECT id, date_added, host, port, username, password, database_name, table_name, type_db, status 
    FROM connections 
    WHERE id = ?
    """
    cursor.execute(query, (connection_id,))
    row = cursor.fetchone()

    if row:
        # Возвращаем данные в виде словаря
        connection = {
            'id': row[0],
            'date_added': row[1],
            'host': row[2],
            'port': row[3],
            'username': row[4],
            'password': row[5],
            'database_name': row[6],
            'table_name': row[7],
            'type_db': row[8],
            'status': row[9]
        }
        return connection
    else:
        return None



""" Таблица: Аккаунты """

# Мои аккаунты
def create_accounts_table(cursor):
    """
    Создает таблицу Accounts в базе данных, если она еще не существует.
    
    Аргументы:
    cursor -- объект курсора SQLite
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,                           -- ID: автоинкремент, уникальное
        date_added DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,         -- Дата добавления аккаунта
        username TEXT NOT NULL UNIQUE CHECK(length(username) = 20),     -- Имя пользователя, текст ровно 20 символов, уникальное, не пустое
        nickname TEXT NOT NULL UNIQUE,                                         -- Псевдоним пользователя: строка, не пустая
        private_key_rsa TEXT NOT NULL,                                  -- Приватный ключ RSA: строка в формате PEM, не пустая
        public_key_rsa TEXT NOT NULL                                    -- Публичный ключ RSA: строка в формате PEM, не пустая
        
    );
    ''')

# Добавления аккаунта
def add_account(connection, cursor, username, nickname, private_key_rsa, public_key_rsa):
    """
    Добавляет новый аккаунт в таблицу 'UserSettings'.
    
    Аргументы:
    cursor -- объект курсора SQLite.
    username -- строка, имя пользователя (ровно 20 символов).
    nickname -- строка, псевдоним пользователя.
    private_key_rsa -- строка, приватный ключ RSA в формате PEM.
    public_key_rsa -- строка, публичный ключ RSA в формате PEM.
    """
    query = '''
    INSERT INTO Accounts (username, nickname, private_key_rsa, public_key_rsa) 
    VALUES (?, ?, ?, ?)
    '''
    try:
        cursor.execute(query, (username, nickname, private_key_rsa, public_key_rsa))
        connection.commit()
        return True
    except Exception as e:
        return False

# Удаления аккаунта по айдишнику
def delete_account_by_id(connection, cursor, account_id):
    """
    Удаляет аккаунт из таблицы 'UserSettings' по ID.
    
    Аргументы:
    cursor -- объект курсора SQLite.
    account_id -- целое число, ID аккаунта, который нужно удалить.
    """
    query = 'DELETE FROM Accounts WHERE id = ?'
    try:
        cursor.execute(query, (account_id,))
        connection.commit()
        print(f"Аккаунт с ID {account_id} успешно удален.")
    except Exception as e:
        print(f"Ошибка при удалении аккаунта: {e}")

# Получить список аккаунтов
def fetch_all_accounts(cursor):
    """
    Возвращает список всех аккаунтов из таблицы 'UserSettings'.
    
    Аргументы:
    cursor -- объект курсора SQLite.

    Возвращает:
    Список словарей с данными об аккаунтах.
    """
    query = 'SELECT id, date_added, username, nickname, private_key_rsa, public_key_rsa FROM Accounts'
    cursor.execute(query)
    rows = cursor.fetchall()

    accounts_list = []
    for row in rows:
        account = {
            'id': row[0],
            'date_added': row[1],
            'username': row[2],
            'nickname': row[3],
            'private_key_rsa': row[4],
            'public_key_rsa': row[5]
        }
        accounts_list.append(account)
    
    return accounts_list

# Получить список никнеймов аккаунта 
def get_accounts_nicknames(cursor):
    """
    Возвращает список значений из колонки 'nickname' в таблице 'Accounts'.
    
    Аргументы:
    cursor -- объект курсора SQLite
    
    Возвращает:
    Список никнеймов (может быть пустым).
    """
    try:
        # Выполняем запрос для выбора всех значений из колонки 'nickname'
        cursor.execute("SELECT nickname FROM Accounts")
        
        # Извлекаем все результаты запроса
        rows = cursor.fetchall()
        
        # Проверяем, есть ли данные, и формируем список никнеймов
        if rows:
            nicknames = [row[0] for row in rows]
        else:
            nicknames = []  # Возвращаем пустой список, если данных нет
        
        return nicknames
    
    except Exception as e:
        print(f"Ошибка при извлечении никнеймов: {e}")
        return []

# Получить аккаунт по никнейму
def get_account_by_nickname(cursor, nickname):
    """
    Находит и возвращает запись из таблицы 'Accounts' по заданному псевдониму (nickname).

    Аргументы:
    cursor -- объект курсора SQLite
    nickname -- псевдоним пользователя для поиска

    Возвращает:
    Словарь с данными аккаунта или None, если не найдено.
    """
    query = "SELECT id, date_added, username, nickname, private_key_rsa, public_key_rsa FROM Accounts WHERE nickname = ?"
    cursor.execute(query, (nickname,))
    row = cursor.fetchone()

    if row:
        # Возвращаем данные в виде словаря
        account = {
            'id': row[0],
            'date_added': row[1],
            'username': row[2],
            'nickname': row[3],
            'private_key': row[4],
            'public_key': row[5]
        }
        return account
    else:
        return None



