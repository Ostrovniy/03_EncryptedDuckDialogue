import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from dblocal import get_accounts_nicknames, fetch_connection_info, get_friends_nicknames, get_friend_by_nickname, get_account_by_nickname, get_connection_by_id
from cripto import data_to_encryptdata, decrypt_with_pem_private_key, get_hesh
from postgresql import connect_to_db, close_db_connection, create_messages_table, add_message, fetch_messages

class Message(tk.Frame):
    """Класс для создания фрейма 'переписка'."""

    def __init__(self, parent, connection, cursor):
        """Инициализация окна."""
        super().__init__(parent) # Создаем дочернее окно по отношению к родительскому

        # Данные для работы с БД локальной
        self.cursor = cursor
        self.connection = connection

        # Стили - Комбо бокс
        styleCombobox = ttk.Style()
        styleCombobox.configure('TCombobox.TLabel', fieldbackground='#17212b', background='#17212b', foreground='#ffefe1', selectbackground='#17212b', selectforeground='#ffefe1', padding=5)
        private_button_style = ttk.Style()
        private_button_style.configure("Private_button_style.TLabel", foreground="#17212b", background="#fcd535", relief='flat', font=("Arial", 10, "normal"))
        # Определяем стиль для Treeview
        tree_style = ttk.Style()
        tree_style.configure("Custom.Treeview",background="#0e1621",fieldbackground="#0e1621",foreground="#ffefe1",borderwidth=0,rowheight=40,padding=5)
        # Настроить стиль для заголовка Treeview
        tree_style.configure("Custom.Treeview.Heading",background="#17212b",foreground="#ffefe1",font=("Arial", 10, "bold"),borderwidth=0,padding=5)  
        # Настроить стиль для заголовков при выделении
        tree_style.map("Custom.Treeview.Heading",background=[('selected', '#0f151c')])

        # Первая строка: Блок для выбора Аккаунта, Соидинения, Друга и загрузки переписки
        self.frame_top = tk.Frame(self, bg='#0e1621')
        self.frame_top.pack(side=tk.TOP, fill=tk.X, ipady=5)

        # 1-й блок: Аккаунт
        self.block1 = tk.Frame(self.frame_top, bg='#0e1621')
        self.block1.pack(side=tk.LEFT, padx=10, anchor=tk.S)  

        # 2-й блок: Соидинения
        self.block2 = tk.Frame(self.frame_top, bg='#0e1621')
        self.block2.pack(side=tk.LEFT, padx=10, anchor=tk.S)

        # 3-й блок: Друг
        self.block3 = tk.Frame(self.frame_top, bg='#0e1621')
        self.block3.pack(side=tk.LEFT, padx=10, anchor=tk.S)  

        # 4-й блок: Кнопка загрузить переписку
        self.block4 = tk.Frame(self.frame_top, bg='#0e1621')
        self.block4.pack(side=tk.LEFT, padx=10, anchor=tk.S)

        # Вторая строка: Таблица с перепиской
        self.frame_middle = tk.Frame(self, bg='#0e1621')
        self.frame_middle.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Третья строка: Написать сообщения и отпраивть
        self.frame_bottom = tk.Frame(self, bg='#0e1621')
        self.frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, ipady=5)  # Прижата к низу и отступы

        # Заголовое Account
        label1 = tk.Label(self.block1, text="Account", anchor="w", background='#0e1621', foreground='#ffefe1')
        label1.pack(fill=tk.X)  # Выравнивание заголовка по левому краю

        # Поле ввода Account
        self.list_accounts = get_accounts_nicknames(self.cursor)
        # Дефолтное значения, для ситуации когда список пустой
        self.account_defolt = self.list_accounts[0] if self.list_accounts else []
        self.accounts_combobox = ttk.Combobox(self.block1, style='TCombobox.TLabel', values=self.list_accounts, state='readonly')
        self.accounts_combobox.set(self.account_defolt)  # Установка значения по умолчанию
        self.accounts_combobox.pack(pady=(0, 5))  # Прижатие к низу и добавление отступа сверху

        # Заголовок Connections
        label2 = tk.Label(self.block2, text="Connections", anchor="w", background='#0e1621', foreground='#ffefe1')
        label2.pack(fill=tk.X)  # Выравнивание заголовка по левому краю

        # Поле ввода Connections
        self.list_connection = fetch_connection_info(self.cursor) # Список доступных соиинений
        self.connection_defolt = self.list_connection[0] if self.list_connection else []
        self.connection_combobox = ttk.Combobox(self.block2, style='TCombobox.TLabel', values=self.list_connection, state='readonly', width=35)
        self.connection_combobox.set(self.connection_defolt)
        self.connection_combobox.pack(pady=(0, 5))  # Прижатие к низу и добавление отступа сверху

        # Заголовок Friend
        self.label3 = tk.Label(self.block3, text="Friend", anchor="w", background='#0e1621', foreground='#ffefe1')
        self.label3.pack(fill=tk.X)  # Выравнивание заголовка по левому краю

        # Поле ввода Friend
        self.list_friends = get_friends_nicknames(self.cursor) # Список никнеймов друзей с локал БД
        self.friend_defolt = self.list_friends[0] if self.list_friends else [] # Дефолтное значения, для ситуации когда список пустой
        self.friends_combobox = ttk.Combobox(self.block3, style='TCombobox.TLabel', values=self.list_friends, state='readonly')
        self.friends_combobox.set(self.friend_defolt)  # Установка значения по умолчанию
        self.friends_combobox.pack(pady=(0, 5))  # Прижатие к низу и добавление отступа сверху

        # Кнопка "Загрузить всю переписку"
        self.load_message_from_db = ttk.Button(self.block4, style='Private_button_style.TLabel', text="Get all messages", padding=5, command=self.get_all_message)
        self.load_message_from_db.pack(pady=(20, 5))  # Прижатие к низу и выравнивание на уровне комбобоксов

        # Определяем столбцы
        self.columns = ("date_added", "sender", "receiver", "text", "check_hesh")

        self.tree = ttk.Treeview(self.frame_middle, columns=self.columns, show="headings", selectmode="browse", style="Custom.Treeview")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5)

        # Определяем заголовки + сортировка
        self.tree.heading("date_added", text="Added")
        self.tree.heading("sender", text="Sender")
        self.tree.heading("receiver", text="Receiver")
        self.tree.heading("text", text="Message")
        self.tree.heading("check_hesh", text="Check hesh")

        # Настройка столбцов таблицы
        self.tree.column('#1', stretch=False, width=140)
        self.tree.column('#2', stretch=False, width=80)
        self.tree.column('#3', stretch=False, width=80)
        self.tree.column('#4', stretch=True)
        self.tree.column('#5', stretch=False, width=140)
        
        # Поле ввода Сообщения для отправки
        self.text_message_input = tk.Text(self.frame_bottom, height=2, bg='#17212b', fg='#ffefe1', borderwidth=0, insertbackground='#ffefe1')
        self.text_message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5) #padx=10, pady=5

        # Кнопка "Отправить сообщение"
        self.send_message_button = ttk.Button(self.frame_bottom, style='Private_button_style.TLabel', text=" Send ", padding=7, command=self.send_message)
        self.send_message_button.pack(side=tk.LEFT, padx=10, pady=5)

    # Получить вводимые данные (Аккаунт, Соидинения, Друг)
    def get_input_data(self):
        acc = self.accounts_combobox.get()
        con = self.connection_combobox.get()
        fri = self.friends_combobox.get()

        return acc, con, fri

    # Обработка кнопки "Отправить сообщения"
    def send_message(self):
        acc, con, fri = self.get_input_data()
        send_text = self.text_message_input.get('1.0', 'end').strip()  # Используем .strip() чтобы удалить лишние пробелы и символы новой строки

        # результат и текст валидации
        valid_answe, valid_text = self.valid_main(acc, con, fri)

        # Если валидация не продейна выход с метода
        if not valid_answe:
            showerror('Error', valid_text)
            return

        # Проверка что сообщения не пустое выход с метода
        if not send_text:
            showerror('Error', "You can't send an empty message")
            return
        
        if len(send_text) > 180:
            showerror('Error', 'You cannot send a message longer than 180 characters.')
            return
        
        # Данные для переписки, словари "Аккаунт, Друг, Соидинения"
        acc_tuple, con_tuple, fri_tuple = self.get_inputdata_from_db(acc, con, fri)
        # зашыфровать переписку Текст - Текст + хеш зашыфрованные
        send_text_encrypt, send_text_encrypt_hesh = data_to_encryptdata(send_text, fri_tuple['public_key'])
        # зашыфровать сообщение своим публичным ключем с меткой ноте copy
        send_text_encrypt_copy, send_text_encrypt_hesh_copy = data_to_encryptdata(send_text, acc_tuple['public_key'])

        # Открыть соидинения с пост грес БД, в нужную таблицу
        connection_postgres, cursor_postgres = connect_to_db(con_tuple['database_name'], con_tuple['username'], con_tuple['password'], con_tuple['host'], con_tuple['port'])

        # Проверка на то что мы подключились к бд
        if connection_postgres is None or cursor_postgres is None:
            showerror('No connection', 'Failed to establish connection to database')
            return
        
        # Создать таблицу если она не создана
        create_messages_table(connection_postgres, con_tuple['table_name'])

        # Отправить сообщения зашыфровеннок публичным ключем друга
        res_send1 = add_message(connection_postgres, cursor_postgres, con_tuple['table_name'], acc_tuple['username'], fri_tuple['username'], send_text_encrypt, send_text_encrypt_hesh)
        # Отправить копию сообщения, но уже зашыфрованное публичнм ключем отправителя
        res_send2 = add_message(connection_postgres, cursor_postgres, con_tuple['table_name'], acc_tuple['username'], fri_tuple['username'], send_text_encrypt_copy, send_text_encrypt_hesh_copy, 'copy')

        # Проверка получилось отправить сообщение или нет
        if not res_send1 or not res_send2:
            showerror('No connection', 'Failed to send messages')
            return
        
        showinfo('Success', "Messages sent")

        # Закрыть соидинения с пост грес
        close_db_connection(connection_postgres, cursor_postgres)

        self.text_message_input.delete('1.0', tk.END)
        self.get_all_message()

    # Обработка кнопки "Загрузить переписку"
    def get_all_message(self):
        acc, con, fri = self.get_input_data()
        valid_answe, valid_text = self.valid_main(acc, con, fri)

        # Если валидация н продейна
        if not valid_answe:
            showerror('Validation error', valid_text)
        else:
            # Данные для переписки, словари "Аккаунт, Друг, Соидинения"
            self.done_messages = self.formating_all_message()

            if not self.done_messages:
                showerror('Empty', 'The table with the dialogue is empty')
                return 

            # Очистите текущие данные в treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Заполнение таблицы
            for f in self.done_messages:
                input_data = (f['date_added'], f['sender_id'], f['receiver_id'], f['text'], f['hash'])
                self.tree.insert('', tk.END, values=input_data)

    # Главный валидатор
    def valid_main(self, acc, con, fri):
        answer_text = ''
        answer = True
        if acc == '':
            answer_text += 'Create an account!!\n'
            answer = False
        if con == '':
            answer_text += 'Create connections!!\n'
            answer = False
        if fri == '':
            answer_text += 'Add a friend!!\n'
            answer = False
        return answer, answer_text

    # Информация с БД по трем полням (Аккаунт, Соидинения, Друга)
    def get_inputdata_from_db(self, nik_acc, con, nik_fr):
        id_con = con.split('/')[0]
        acc_tuple = get_account_by_nickname(self.cursor, nik_acc)
        fri_tuple = get_friend_by_nickname(self.cursor, nik_fr)
        con_tuple = get_connection_by_id(self.cursor, id_con)
        return acc_tuple, con_tuple, fri_tuple
    
    # Получить имя пользователя по никнейму (Для друга и Аккаунта) что бы определить кто кому писал
    def get_nikname_by_username(self, username, acc_tuple, fri_tuple):
        if username == acc_tuple['username']:
            return acc_tuple['nickname']
        if username == fri_tuple['username']:
            return fri_tuple['nickname']

    # Проверка Хеша
    def check_hesh(self, private_key, hesh, text):
        # рассыфровать хеш приватным ключем
        try:
            decrypt_hesh = decrypt_with_pem_private_key(private_key, hesh)
        except ValueError:
            # Decryption failed
            return False
        # Хешыровать рассыфрованый текст
        new_hesh = get_hesh(text)
        # сравнить две хеша на равенстко
        return decrypt_hesh == new_hesh
        
    # Получить сообщения и расшыфровать их
    def formating_all_message(self):
        acc, con, fri = self.get_input_data()
        valid_answe, valid_text = self.valid_main(acc, con, fri)

        # Если валидация не продейна выход с метода
        if not valid_answe:
            showerror('Error', valid_text)
            return False
        
        # Данные для переписки, словари "Аккаунт, Друг, Соидинения"
        acc_tuple, con_tuple, fri_tuple = self.get_inputdata_from_db(acc, con, fri)

        # Открыть соидинения с пост грес БД, в нужную таблицу
        connection_postgres, cursor_postgres = connect_to_db(con_tuple['database_name'], con_tuple['username'], con_tuple['password'], con_tuple['host'], con_tuple['port'])

        # Получить все сообщения в зашыфрованом виде
        all_mes = fetch_messages(cursor_postgres, con_tuple['table_name'], acc_tuple['username'], fri_tuple['username'])

        # Закрыть соидинения с пост грес
        close_db_connection(connection_postgres, cursor_postgres)

        if not all_mes:
            return False

        # метод определения кто отправитель
        transformed_messages = []  # Список для хранения преобразованных сообщений
        
        # Преобразования зашыфрованных данных в рассыфрованные
        for message in all_mes:
            # Преобразуем дату в формат 'День.Месяц.Год Часы: минуты'
            formatted_date = message['date_added'].strftime('%d.%m.%Y %H:%M')

            # Получаем никнеймы для sender_id и receiver_id
            sender_nickname = self.get_nikname_by_username(message['sender_id'], acc_tuple, fri_tuple)
            receiver_nickname = self.get_nikname_by_username(message['receiver_id'], acc_tuple, fri_tuple)

            # Расшифровываем текст сообщения
            decrypted_text = decrypt_with_pem_private_key(acc_tuple['private_key'], message['text'])

            # Проверяем хеш
            hash_result = self.check_hesh(acc_tuple['private_key'], message['hash'], decrypted_text)

            # Создаем новый словарь с преобразованными значениями
            new_message = {
                'date_added': formatted_date,
                'sender_id': sender_nickname,
                'receiver_id': receiver_nickname,
                'text': decrypted_text,
                'hash': hash_result
            }

            # Добавляем новый словарь в список
            transformed_messages.append(new_message)
        return transformed_messages



