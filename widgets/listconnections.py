import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesnocancel
from tkinter.messagebox import showerror, showinfo
from dblocal import fetch_all_connections, delete_connection_by_id
from postgresql import drop_messages_table, connect_to_db, close_db_connection

class ListConnections(tk.LabelFrame):
    """Класс для создания фрейма 'Список соидинений'."""

    def __init__(self, parent, connection, cursor):
        """Инициализация окна."""
        super().__init__(parent, text="List of connections", bd=1, relief="groove", bg='#0e1621', fg='#ffefe1')
        self.pack(fill=tk.BOTH, expand=True, ipadx=2, ipady=2)

        # Данные для работы с БД локальной
        self.cursor = cursor
        self.connection = connection

        # Стиль - Кнопка удалить, Скопировать имя пользователя, таблица и заголовок таблицы
        delete_button_style = ttk.Style()
        delete_button_style.configure("Delete_button_style.TLabel", foreground="#ffffff", background="#d9534f",  relief='flat', font=("Arial", 10, "bold"))
        copy_connection_data_btn_style = ttk.Style()
        copy_connection_data_btn_style.configure("Private_button_style.TLabel", foreground="#17212b", background="#fcd535", relief='flat', font=("Arial", 10, "bold"))
        tree_style = ttk.Style() # Определяем стиль для Treeview
        tree_style.configure("Custom.Treeview",background="#0e1621",  fieldbackground="#0e1621", foreground="#ffefe1",borderwidth=0,rowheight=40)  
        # Настроить стиль для заголовка Treeview
        tree_style.configure("Custom.Treeview.Heading",background="#17212b",foreground="#ffefe1",font=("Arial", 10, "bold"),borderwidth=0,padding=5)  
        # Настроить стиль для заголовков при выделении
        tree_style.map("Custom.Treeview.Heading", background=[('selected', '#0f151c')])

        # Фрейм: Первая строка, список действий с таблицей
        self.buttons_frame = tk.Frame(self, bg='#0e1621')
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Фрейм: Вторая строка, таблица
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(10, 0))  # Добавлен отступ сверху

        # Кнопка "Удалить"
        self.dell_btn = ttk.Button(self.buttons_frame, style='Delete_button_style.TLabel', text='Delete',  padding=5, state='disabled')
        self.dell_btn.pack(side=tk.LEFT, padx=5)  # отступы слева и справа

        # Кнопка "Очистить переписку"
        self.dell_mes_btn = ttk.Button(self.buttons_frame, style='Delete_button_style.TLabel', text='Clear Dialogue',  padding=5, state='disabled')
        self.dell_mes_btn.pack(side=tk.LEFT, padx=5)  # отступы слева и справа

        # Кнопка "Скопировать имя пользователя"
        self.copy_connection_data_btn = ttk.Button(self.buttons_frame, style='Private_button_style.TLabel', text='Copy connection data', padding=5, state='disabled')
        self.copy_connection_data_btn.pack(side=tk.LEFT, padx=5)

        # Определяем столбцы таблицы
        self.columns = ("id", "date_added", "host", "port", "username", "password", "database_name", "table_name", "type_db", "status")

        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings", selectmode="browse", style="Custom.Treeview")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Определяем заголовки + сортировка
        self.tree.heading("id", text="№", command=lambda: self.sort(0, False))
        self.tree.heading("date_added", text="Added", command=lambda:  self.sort(1, False))
        self.tree.heading("host", text="Host", command=lambda:  self.sort(2, False))
        self.tree.heading("port", text="Port", command=lambda:  self.sort(3, False))
        self.tree.heading("username", text="Username", command=lambda:  self.sort(4, False))
        self.tree.heading("password", text="Password", command=lambda:  self.sort(5, False))
        self.tree.heading("database_name", text="Database", command=lambda:  self.sort(6, False))
        self.tree.heading("table_name", text="Table name", command=lambda:  self.sort(7, False))
        self.tree.heading("type_db", text="Type", command=lambda:  self.sort(8, False))
        self.tree.heading("status", text="Status", command=lambda:  self.sort(9, False))

        # Настройка столбцов таблицы
        self.tree.column('#1', stretch=False, width=40)
        self.tree.column('#2', stretch=False, width=140)
        self.tree.column('#3', stretch=False, width=100)
        self.tree.column('#4', stretch=False, width=50)
        self.tree.column('#5', stretch=False, width=140)
        self.tree.column('#6', stretch=False, width=140)
        self.tree.column('#7', stretch=False, width=140)
        self.tree.column('#8', stretch=False, width=140)
        self.tree.column('#9', stretch=True)

        self.db_connections = self.get_connections_db() # list[Tuple] Список, соидинений с бд

        # Отрисровка данных в таблицу
        for f in self.db_connections:
            input_data = (f['id'], f['date_added'], f['host'], f['port'], f['username'], f['password'], f['database_name'], f['table_name'], f['type_db'], f['status'])
            self.tree.insert('', tk.END, values=input_data)

        # Связать событие и метод
        self.tree.bind("<<TreeviewSelect>>", self.item_selected)

    # Получить сипоск соидинений
    def get_connections_db(self):
        return fetch_all_connections(self.cursor)
    
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
        self.copy_connection_data_btn['state'] = 'normal'
        self.dell_mes_btn['state'] = 'normal'

        # Передать кнопкам обработчики события с параметрами
        if len(res) != 0:
            self.dell_btn['command'] = lambda: self.delete_and_update(res[0][0])
            self.copy_connection_data_btn['command'] = lambda: self.copy_connection(res[0])
            self.dell_mes_btn['command'] = lambda: self.delete_mes_table(res[0])

    # Обновить данные с таблице
    def refresh_treeview(self):
        # Очистите текущие данные в treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Отрисовать данные с таблице (взять с бд)
        self.new_con_tuole = self.get_connections_db() # list[Tuple] Список, друзей с бд
        for f in self.new_con_tuole:
            input_data = (f['id'], f['date_added'], f['host'], f['port'], f['username'], f['password'], f['database_name'], f['table_name'], f['type_db'], f['status'])
            self.tree.insert('', tk.END, values=input_data)

    # Обработка кнопки "Удалить" с подтверждением
    def delete_and_update(self, acc_id):
        res = askyesnocancel(title='Confirm the operation', message='Are you sure you want to delete your connection?')
        if res:
            delete_connection_by_id(self.connection, self.cursor, acc_id)
            self.dell_btn['state'] = 'disabled'
            self.refresh_treeview()

    # Обработка кнопки "Очистить переписку" с подтверждением
    def delete_mes_table(self, c):
        res = askyesnocancel(title='Confirm the operation', message='Are you sure all messages will be deleted from the table?')
        if res:
            # Открыть соидинения с пост грес БД, в нужную таблицу
            connection_postgres, cursor_postgres = connect_to_db(c[6], c[4], c[5], c[2], c[3])

            # Проверка на то что мы подключились к бд
            if connection_postgres is None or cursor_postgres is None:
                showerror('No connection', 'Failed to establish connection to database')
                return
        
            res2 = drop_messages_table(connection_postgres, cursor_postgres, c[7]) # Удалить таблицу

            if not res2:
                showerror('Error', 'Failed to delete/clear table')
            
            close_db_connection(connection_postgres, cursor_postgres) # Закрыть соидинения
            self.dell_mes_btn['state'] = 'disabled'
            self.refresh_treeview()

    # Обработка кнопки "Скопировать данные для подключения"
    def copy_connection(self, c):
        self.clipboard_clear()
        self.clipboard_append(f"host: {c[2]}\nport: {c[3]}\nusername: {c[4]}\npassword: {c[5]}\ndatabase_name: {c[6]}\ntable_name: {c[7]}\ntype_db: {c[8]}")
        self.copy_connection_data_btn['state'] = 'disabled'
        self.update()    