import psycopg2
from psycopg2 import OperationalError

# Подключения к БД, получения connection, cursor
def connect_to_db(db_name, user, password, host='localhost', port='5432'):
    """
    Устанавливает соединение с базой данных PostgreSQL и возвращает объекты соединения и курсора.
    
    Аргументы:
    db_name -- имя базы данных
    user -- имя пользователя PostgreSQL
    password -- пароль пользователя PostgreSQL
    host -- адрес хоста, по умолчанию 'localhost'
    port -- порт подключения, по умолчанию '5432'
    
    Возвращает:
    connection -- объект соединения PostgreSQL
    cursor -- объект курсора PostgreSQL
    """
    try:
        # Устанавливаем соединение с PostgreSQL
        connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        # Создаем курсор для выполнения SQL-запросов
        cursor = connection.cursor()
        print("Соединение с базой данных PostgreSQL установлено успешно.")
        return connection, cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при подключении к базе данных PostgreSQL: {error}")
        return None, None

# Закрыть соидинения с БД
def close_db_connection(connection, cursor):
    """
    Закрывает соединение и курсор с базой данных PostgreSQL.
    
    Аргументы:
    connection -- объект соединения PostgreSQL
    cursor -- объект курсора PostgreSQL
    """
    if cursor:
        cursor.close()
    if connection:
        connection.commit()
        connection.close()
        print("Соединение с базой данных PostgreSQL закрыто.")

# Проверка соидинения с базой данных
def check_connection(host, port, username, password, database_name, timeout=2):
    """
    Проверяет возможность подключения к базе данных PostgreSQL.

    :param host: Хост базы данных
    :param port: Порт базы данных
    :param username: Имя пользователя
    :param password: Пароль
    :param database_name: Название базы данных
    :return: True если подключение успешно, иначе False
    """
    try:
        # Устанавливаем соединение
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            dbname=database_name,
            connect_timeout=timeout
        )
        # Закрываем соединение
        conn.close()
        return True
    except OperationalError as e:
        # Ошибка подключения
        print(f"Error: {e}")
        return False
    
    except Exception as e:
        # Обработка других возможных исключений
        print(f"Unexpected error: {e}")
        return False

# Создание таблицы для переписки
def create_messages_table(connection, table_name):
    """
    Создает таблицу с заданным именем в базе данных PostgreSQL, если она еще не существует.
    
    Аргументы:
    connection -- объект подключения к базе данных PostgreSQL
    table_name -- имя создаваемой таблицы
    """
    try:
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,                                  -- Уникальный идентификатор сообщения, автоинкремент
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,-- Дата и время добавления сообщения
            sender_id TEXT NOT NULL,                                -- ID отправителя, текст, не пустой
            receiver_id TEXT NOT NULL,                              -- ID получателя, текст, не пустой
            text TEXT NOT NULL,                                     -- Текст сообщения, зашифрованный через RSA
            hash TEXT NOT NULL,                                     -- Хеш сообщения, полученный через hashlib.sha256().hexdigest()
            note TEXT                                               -- Метка копии для сообщений самому себе    
        );
        """
        
        # Выполняем запрос на создание таблицы
        cursor.execute(create_table_query)
        
        # Сохраняем изменения
        connection.commit()
        
        print(f"Таблица '{table_name}' успешно создана или уже существует.")
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при создании таблицы: {error}")
    
    finally:
        # Закрываем курсор
        cursor.close()

# Удаления таблицы по названию
def drop_messages_table(connection, cursor, table_name):
    """
    Удаляет таблицу с заданным именем из базы данных PostgreSQL, если она существует.
    
    Аргументы:
    connection -- объект подключения к базе данных PostgreSQL
    cursor -- курсор для выполнения SQL-запросов
    table_name -- имя удаляемой таблицы
    
    Возвращает:
    True -- если удаление прошло успешно
    False -- если произошла ошибка
    """
    try:
        # SQL-запрос для удаления таблицы, если она существует
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        
        # Выполняем запрос на удаление таблицы
        cursor.execute(drop_table_query)
        
        # Сохраняем изменения
        connection.commit()
        
        print(f"Таблица '{table_name}' успешно удалена или не существует.")
        return True
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при удалении таблицы: {error}")
        return False
    

# Добавления сообщения в БД
def add_message(connection, cursor, table_name, sender_id, receiver_id, text, hash, note=''):
    """
    Добавляет новое сообщение в указанную таблицу базы данных PostgreSQL.

    Аргументы:
    connection -- объект соединения с базой данных PostgreSQL
    cursor -- объект курсора PostgreSQL
    table_name -- имя таблицы для добавления сообщений
    sender_id -- ID отправителя сообщения
    receiver_id -- ID получателя сообщения
    text -- текст сообщения, зашифрованный
    hesh -- хеш сообщения
    note -- Заметка для дубликатов смс

    Возвращает:
    bool -- True, если сообщение успешно добавлено, иначе False.
    """
    try:
        # SQL-запрос для добавления нового сообщения в таблицу
        insert_query = f"""
        INSERT INTO {table_name} (sender_id, receiver_id, text, hash, note)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        # Выполняем запрос и передаем параметры
        cursor.execute(insert_query, (sender_id, receiver_id, text, hash, note))
        
        # Фиксируем изменения в базе данных
        connection.commit()

        print("Сообщение успешно добавлено в базу данных.")
        return True
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при добавлении сообщения в базу данных: {error}")
        return False

# Получить историю переписки двух человек
def fetch_messages(cursor, table_name, user1_id, user2_id):
    """
    Извлекает все сообщения из указанной таблицы, где sender_id и receiver_id соответствуют user1_id и user2_id в любом порядке
    и note соответствует указанному значению (для первого условия 'copy', для второго - пусто).
    Данные сортируются по столбцу date_added по возрастанию и возвращаются в виде списка словарей.

    Аргументы:
    cursor -- объект курсора PostgreSQL
    table_name -- имя таблицы для извлечения сообщений
    user1_id -- ID первого пользователя
    user2_id -- ID второго пользователя

    Возвращает:
    list -- список словарей с данными о сообщениях.
    """
    try:
        # SQL-запрос для извлечения данных с учетом двух условий
        select_query = f"""
        SELECT id, date_added, sender_id, receiver_id, text, hash, note
        FROM {table_name}
        WHERE 
            (sender_id = %s AND receiver_id = %s AND note = 'copy') 
            OR 
            (sender_id = %s AND receiver_id = %s AND note = '')
        ORDER BY date_added ASC;
        """
        
        # Выполнение запроса с переданными параметрами
        cursor.execute(select_query, (user1_id, user2_id, user2_id, user1_id))
        
        # Получение всех строк результата
        rows = cursor.fetchall()

        # Формирование списка словарей
        messages = []
        for row in rows:
            message = {
                'id': row[0],
                'date_added': row[1],
                'sender_id': row[2],
                'receiver_id': row[3],
                'text': row[4],
                'hash': row[5],
                'note': row[6]
            }
            messages.append(message)
        
        return messages

    except (Exception, psycopg2.DatabaseError) as error:
        return []


