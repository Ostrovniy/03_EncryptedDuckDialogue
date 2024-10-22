import re
import socket
import ipaddress
import tkinter as tk
from tkinter import ttk
from dblocal import add_connection
from postgresql import check_connection
from tkinter.messagebox import showerror, showinfo


class AddNewConnectionParameters(tk.LabelFrame):
    """Класс для создания фрейма 'Добавить новое содинения БД'."""

    def __init__(self, parent, connection, cursor):
        """Инициализация окна."""
        super().__init__(parent, text="Add connection", bd=1, relief="groove", bg='#0e1621', fg='#ffefe1') 
        self.pack(fill="both", expand=True, ipadx=2, ipady=2)

        # Данные для работы с БД локальной
        self.cursor = cursor
        self.connection = connection

        # Стиль - Поля ввода, Выпадающий список, Кнопки
        entry_style = ttk.Style()
        entry_style.configure("MyEntry.TLabel", foreground="#ffefe1", background="#17212b", padding=5, insertcolor="#ffefe1")
        styleCombobox = ttk.Style()
        styleCombobox.configure('TCombobox.TLabel', fieldbackground='#17212b', background='#17212b', foreground='#ffefe1', selectbackground='#17212b', selectforeground='#ffefe1', padding=5)
        сheck_connection_style = ttk.Style()
        сheck_connection_style.configure("CheckConnectionStyle.TLabel", foreground="#17212b", background="#fcd535", relief='flat', font=("Arial", 10, "bold"))

        # Заголовок host
        host_label = ttk.Label(self, text="Host", background='#0e1621', foreground='#ffefe1')
        host_label.pack(anchor='w', pady=(10, 0), padx=(10, 0))

        # Поле ввода host
        self.host_entry = ttk.Entry(self, style="MyEntry.TLabel", width=40)
        self.host_entry.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Заголовок port
        port_label = ttk.Label(self, text="Port", background='#0e1621', foreground='#ffefe1')
        port_label.pack(anchor='w', pady=(5, 0), padx=(10, 0))

        # Поле ввода port
        self.port_entry = ttk.Entry(self, style="MyEntry.TLabel", width=40)
        self.port_entry.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Заголовок username
        username_label = ttk.Label(self, text="User Name", background='#0e1621', foreground='#ffefe1')
        username_label.pack(anchor='w', pady=(5, 0), padx=(10, 0))

        # Поле ввода username
        self.username_entry = ttk.Entry(self, style="MyEntry.TLabel", width=40)
        self.username_entry.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Заголовок password
        password_label = ttk.Label(self, text="Password", background='#0e1621', foreground='#ffefe1')
        password_label.pack(anchor='w', pady=(5, 0), padx=(10, 0))

        # Поле ввода password
        self.password_entry = ttk.Entry(self, style="MyEntry.TLabel", width=40)
        self.password_entry.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Заголовок database_name
        database_name_label = ttk.Label(self, text="Database Name", background='#0e1621', foreground='#ffefe1')
        database_name_label.pack(anchor='w', pady=(5, 0), padx=(10, 0))

        # Поле ввода database_name
        self.database_name_entry = ttk.Entry(self, style="MyEntry.TLabel", width=40)
        self.database_name_entry.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Заголовок table_name
        table_name_label = ttk.Label(self, text="Table Name", background='#0e1621', foreground='#ffefe1')
        table_name_label.pack(anchor='w', pady=(5, 0), padx=(10, 0))

        # Поле ввода table_name
        self.table_name_entry = ttk.Entry(self, style="MyEntry.TLabel", width=40)
        self.table_name_entry.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Заголовок type_db
        type_db_label = ttk.Label(self, text="Type Database", background='#0e1621', foreground='#ffefe1')
        type_db_label.pack(anchor='w', pady=(5, 0), padx=(10, 0))

        # Поле выбора table_name
        list_type_db = ["PostgreSQL"]
        self.type_db_combobox = ttk.Combobox(self, style='TCombobox.TLabel', values=list_type_db, state='readonly', width=40) # Запрет редактирования
        self.type_db_combobox.set(list_type_db[0])  # Установка значения по умолчанию
        self.type_db_combobox.pack(anchor='w', pady=(1, 0), padx=(10, 0))

        # Кнопка "Проверить соидинения"
        self.сheck_connection = ttk.Button(self, style='CheckConnectionStyle.TLabel', text="Check connections", padding=5, command=self.checking_connection)
        self.сheck_connection.pack(anchor='w',  pady=(20, 5), padx=(10, 0))
        
        # Кнопка "Сохранить"
        self.save_button = ttk.Button(self, style='CheckConnectionStyle.TLabel', text="Save", padding=5, command=self.save_connection)
        self.save_button.pack(anchor='w',  pady=(0, 5), padx=(10, 0))

    # Получить данные с формы
    def get_form_data(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        database_name = self.database_name_entry.get()
        table_name = self.table_name_entry.get()
        type_db = self.type_db_combobox.get()

        return host, port, username, password, database_name, table_name, type_db
    
    # Обработка кнопки "Проверить соидинения"
    def checking_connection(self):
        host, port, username, password, database_name, table_name, type_db = self.get_form_data()
        res_valid = self.valid_main(host, port, username, password, database_name, table_name)

        if res_valid:
            if check_connection(host, port, username, password, database_name):
                showinfo(title="Ready", message="Connections successful")
            else:
                showerror(title="Error", message="Connection failed")
        else:
            not_valid = self.get_list_not_valid(host, port, username, password, database_name, table_name)
            showerror(title="Error", message=not_valid)
            self.claer_not_valid_inputs(host, port, username, password, database_name, table_name)

    # Обработка нажатия кнопки "Сохранить"
    def save_connection(self):
        host, port, username, password, database_name, table_name, type_db = self.get_form_data()
        res_valid = self.valid_main(host, port, username, password, database_name, table_name)

        if res_valid:
            answer = add_connection(self.connection, self.cursor, host, port, username, password, database_name, table_name, type_db, '')
            if not answer:
                showerror(title="Error", message="The combination of host, database_name, table_name: must be unique within the list of entries")
            else:
                showinfo(title="Ready", message='New connection added to DB')
                self.clear_form() 
        else:
            not_valid = self.get_list_not_valid(host, port, username, password, database_name, table_name)
            self.open_error(not_valid)
            self.claer_not_valid_inputs(host, port, username, password, database_name, table_name)

    # Валидатор Хоста
    def valid_host(self, host: str):
        try:
        # Попробуем распознать как IPv4 или IPv6
            ipaddress.ip_address(host)
            return True
        except ValueError:
            # Если это не IP, проверим, является ли это допустимым доменным именем
            try:
                socket.gethostbyname(host)
                return True
            except socket.error:
                return False
            
    # Валидатор Порта
    def valid_port(self, port: str):
        # Проверяем, что строка состоит только из цифр
        if port.isdigit():
            # Преобразуем в целое число и проверим диапазон
            port_number = int(port)
            if 0 <= port_number <= 65535:
                return True
        return False
    
    # Валидатор Имени пользователя
    def valid_username(self, username: str):
        if username and re.match(r'^[a-zA-Z0-9_\.]{1,63}$', username):
            return True
        return False
    
    # Валидатор пароля
    def valid_password(self, password: str):
        if password and len(password) >= 3:
            return True
        return False
    
    # Валидатор Имени базы данных
    def valid_database_name(self, database_name: str):
        if database_name and re.match(r'^[a-zA-Z0-9_]{1,63}$', database_name):
            return True
        return False

    # Валидатор Имени Таблицы
    def valid_table_name(self, table_name: str):
        if table_name and re.match(r'^[a-zA-Z0-9_]{1,63}$', table_name):
            return True
        return False
    
    # Валидатор Формы
    def valid_main(self, host, port, username, password, database_name, table_name):
        # Результат вылидации всех полей
        valid_host = self.valid_host(host)
        valid_port = self.valid_port(port)
        valid_username = self.valid_username(username)
        valid_password = self.valid_password(password)
        valid_database_name = self.valid_database_name(database_name)
        valid_table_name = self.valid_table_name(table_name)

        # Проверить что все True
        return all([valid_host, valid_port, valid_username, valid_password, valid_database_name, valid_table_name])

    # Очистить форму
    def clear_form(self):
        self.host_entry.delete(0, tk.END) 
        self.port_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.database_name_entry.delete(0, tk.END)
        self.table_name_entry.delete(0, tk.END)

    # Получить список не Валидные полей ввода
    def get_list_not_valid(self, host, port, username, password, database_name, table_name):
        not_valid = {
            'Host:': 'Success' if self.valid_host(host) else 'Error',
            'Port:': 'Success' if self.valid_port(port) else 'Error',
            'Username:': 'Success' if self.valid_username(username) else 'Error',
            'Password:': 'Success' if self.valid_password(password) else 'Error',
            'Database name:': 'Success' if self.valid_database_name(database_name) else 'Error',
            'Table name:': 'Success' if self.valid_table_name(table_name) else 'Error',
        }
        # Преобразование словаря в текст с переносом строки
        return '\n'.join(f"{key} {value}" for key, value in not_valid.items())
    

    # Очистить поля для ввода, котоыре не прошли валидацию
    def claer_not_valid_inputs(self, host, port, username, password, database_name, table_name):
        if not self.valid_host(host):
            self.host_entry.delete(0, tk.END)

        if not self.valid_port(port):
            self.port_entry.delete(0, tk.END)

        if not self.valid_username(username):
            self.username_entry.delete(0, tk.END)

        if not self.valid_password(password):
            self.password_entry.delete(0, tk.END)

        if not self.valid_database_name(database_name):
            self.database_name_entry.delete(0, tk.END)

        if not self.valid_table_name(table_name):
            self.table_name_entry.delete(0, tk.END)