import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesnocancel
from dblocal import fetch_all_accounts, delete_account_by_id

class ListAccounts(tk.LabelFrame):
    """Класс для создания фрейма 'Список достпный аккаунтов'."""

    def __init__(self, parent, connection, cursor):
        """Инициализация окна."""
        super().__init__(parent, text="List of accounts", bd=1, relief="groove", bg='#0e1621', fg='#ffefe1')
        self.pack(fill=tk.BOTH, expand=True, ipadx=2, ipady=2)

        # Данные для работы с БД локальной
        self.cursor = cursor
        self.connection = connection

        # Стиль - Кнопка удалить, Скопировать имя пользователя, таблица, заголовок таблицы
        delete_button_style = ttk.Style()
        delete_button_style.configure("Delete_button_style.TLabel", foreground="#ffffff", background="#d9534f",  relief='flat', font=("Arial", 10, "bold"))
        private_button_style = ttk.Style()
        private_button_style.configure("Private_button_style.TLabel", foreground="#17212b", background="#fcd535", relief='flat', font=("Arial", 10, "bold"))
        tree_style = ttk.Style() # Определяем стиль для Treeview
        tree_style.configure("Custom.Treeview",background="#0e1621", fieldbackground="#0e1621",foreground="#ffefe1",borderwidth=0,rowheight=40) 
        # Настроить стиль для заголовка Treeview
        tree_style.configure("Custom.Treeview.Heading",background="#17212b",foreground="#ffefe1",font=("Arial", 10, "bold"),borderwidth=0,padding=5)  
        # Настроить стиль для заголовков при выделении
        tree_style.map("Custom.Treeview.Heading",background=[('selected', '#0f151c')])

        # Фрейм: Первая строка, список действий с таблицей
        self.buttons_frame = tk.Frame(self, bg='#0e1621')
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Фрейм: Вторая строка, таблица
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(10, 0))

        # Кнопка "Удалить"
        self.dell_btn = ttk.Button(self.buttons_frame, style='Delete_button_style.TLabel', text='Delete',  padding=5, state='disabled')
        self.dell_btn.pack(side=tk.LEFT, padx=5)  # отступы слева и справа

        # Кнопка "Скопировать имя пользователя"
        self.copy_username_btn = ttk.Button(self.buttons_frame, style='Private_button_style.TLabel', text='Copy Username', padding=5, state='disabled')
        self.copy_username_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка "Скопировать публичный ключ пользователя"
        self.copy_public_key_btn = ttk.Button(self.buttons_frame, style='Private_button_style.TLabel', text='Copy public key', padding=5, state='disabled')
        self.copy_public_key_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка "Скопировать приватный ключ пользователя"
        self.copy_private_key_btn = ttk.Button(self.buttons_frame, style='Private_button_style.TLabel', text='Copy private key', padding=5, state='disabled')
        self.copy_private_key_btn.pack(side=tk.LEFT, padx=5)

        # Определяем столбцы таблицы
        self.columns = ("id", "date_added", "username", "nickname", "private_key_rsa", "public_key_rsa")

        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings", selectmode="browse", style="Custom.Treeview")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Определяем заголовки + сортировка
        self.tree.heading("id", text="№", command=lambda: self.sort(0, False))
        self.tree.heading("date_added", text="Added", command=lambda:  self.sort(1, False))
        self.tree.heading("username", text="Username", command=lambda:  self.sort(2, False))
        self.tree.heading("nickname", text="Nickname", command=lambda:  self.sort(3, False))
        self.tree.heading("private_key_rsa", text="Private key", command=lambda:  self.sort(4, False))
        self.tree.heading("public_key_rsa", text="Public key", command=lambda:  self.sort(5, False))

        # Настройка столбцов таблицы
        self.tree.column('#1', stretch=False, width=40)
        self.tree.column('#2', stretch=False, width=140)
        self.tree.column('#3', stretch=False, width=200)
        self.tree.column('#4', stretch=False, width=140)
        self.tree.column('#5', stretch=False, width=375)
        self.tree.column('#6', stretch=True)

        self.db_accounts = self.get_accounts_db() # list[Tuple] Список, аккаунтов с бд

        # Отрисровка данных в таблицу
        for f in self.db_accounts:
            input_data = (f['id'], f['date_added'], f['username'], f['nickname'],  f['private_key_rsa'], f['public_key_rsa'])
            self.tree.insert('', tk.END, values=input_data)

        # Связать событие и метод
        self.tree.bind("<<TreeviewSelect>>", self.item_selected)

    # Получить список аккаунтов
    def get_accounts_db(self):
        return fetch_all_accounts(self.cursor)
    
    # Сортировка таблицы по нажатию на заголовок (Скопировал с сайта)
    def sort(self, col, reverse):
        # получаем все значения столбцов в виде отдельного списка
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        # сортируем список
        l.sort(reverse=reverse)
        # переупорядочиваем значения в отсортированном порядке
        for index,  (_, k) in enumerate(l):
            self.tree.move(k, "", index)
        # в следующий раз выполняем сортировку в обратном порядке
        self.tree.heading(col, command=lambda: self.sort(col, not reverse))

    # Обработка события: Выделения елемента в таблицы
    def item_selected(self, event):
        selected_people = ""
        res = []
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            person = item["values"]
            res.append(item["values"]) # мое, добавления елементов строки в список [[id, data...]]
            selected_people = f"{selected_people}{person}\n"

        # Разблокировать кнопки
        self.dell_btn['state'] = 'normal'
        self.copy_username_btn['state'] = 'normal'
        self.copy_public_key_btn['state'] = 'normal'
        self.copy_private_key_btn['state'] = 'normal'

        # Передать кнопкам обработчики события с параметрами
        if len(res) != 0:
            self.dell_btn['command'] = lambda: self.delete_and_update(res[0][0])
            self.copy_username_btn['command'] = lambda: self.copy_username(res[0][2])
            self.copy_public_key_btn['command'] = lambda: self.copy_public_key(res[0][5])
            self.copy_private_key_btn['command'] = lambda: self.copy_private_key(res[0][4])

    # Обновить данные с таблице
    def refresh_treeview(self):
        # Очистите текущие данные в treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Отрисовать данные с таблице (взять с бд)
        self.friends = self.get_accounts_db() # list[Tuple] Список, друзей с бд
        for f in self.friends:
            input_data = (f['id'], f['date_added'], f['username'], f['nickname'], f['private_key_rsa'], f['public_key_rsa'])
            self.tree.insert('', tk.END, values=input_data)

    # Обработка кнопки "Удалить" с подтверждением
    def delete_and_update(self, acc_id):
        res = askyesnocancel(title='Confirm the operation', message='Are you sure you want to delete your account?')
        if res:
            delete_account_by_id(self.connection, self.cursor, acc_id)  # Удаляем запись из базы данных
            self.dell_btn['state'] = 'disabled'                         # Деактивировать кнопку
            self.refresh_treeview()                                     # Обновить таблицу

    # Обработка кнопки "Скопировать имя пользователя"
    def copy_username(self, username):
        self.clipboard_clear()                          # Очистить буфер обмена
        self.clipboard_append(username)                 # Вставить данные в буфер обмена
        self.copy_username_btn['state'] = 'disabled'    # Деактивировать кнопку
        self.update()                                   # Сообщаем системе, что данные в буфере обмена изменились

    # Обработка кнопки "Скопировать Публичный ключ"
    def copy_public_key(self, public_key):
        self.clipboard_clear()
        self.clipboard_append(public_key)
        self.copy_public_key_btn['state'] = 'disabled'
        self.update()    
    
    # Обработка кнопки "Скопировать Приватный ключ"
    def copy_private_key(self, private_key):
        self.clipboard_clear()
        self.clipboard_append(private_key)
        self.copy_private_key_btn['state'] = 'disabled'
        self.update()          